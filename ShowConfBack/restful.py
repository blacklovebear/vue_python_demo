# encoding:utf-8
from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin

from flask_restful import Api, Resource, reqparse

import MySQLdb
from  DBUtils.PooledDB import PooledDB

import util
import erl_terms

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
CORS(app, origins = "*", methods = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'])


pool = PooledDB(MySQLdb, 5, host="abj-elogic-test1.yunba.io",
                    user="yunba",
                    passwd="yunba321",
                    db="conf_show",
                    port=3306,
                    charset='utf8',
                    use_unicode=True)


class ConfList(Resource):
  """配置文件列表
  """
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('kw', type=str)
    self.parser.add_argument('group_id', type=int)
    super(ConfList, self).__init__()

  def get(self):
    args = self.parser.parse_args()
    sql = """select id, host_domain, host_ip, host_user_name, host_pass, ssh_key_path,
                    conf_file_path, service_name, DATE_FORMAT(last_ch_time, '%%Y-%%m-%%d %%H:%%i') AS last_ch_time, comment, group_id
               from conf_file_info where 1=1 """

    group_id = args.get('group_id')
    kw = args.get('kw')

    sql_param = []

    if group_id:
      sql += ' and group_id = %s '
      sql_param.append(group_id)
    if kw:
      sql += ' and conf_content like %s '
      sql_param.append( '%' + kw + '%' )

    result = util.db_fetchall(pool, sql, tuple(sql_param))
    return {'data':result}


class Conf(Resource):
  """操作单个配置文件
  """
  def __init__(self):
    self.parser = reqparse.RequestParser()

    self.parser.add_argument('host_domain', type=str, trim=True)
    self.parser.add_argument('host_ip', type=str, trim=True)
    self.parser.add_argument('host_user_name', type=str, trim=True)
    self.parser.add_argument('ssh_key_path', type=str, trim=True)
    self.parser.add_argument('host_pass', type=str, trim=True)
    self.parser.add_argument('conf_file_path', type=str, trim=True)
    self.parser.add_argument('service_name', type=str, trim=True)
    self.parser.add_argument('comment', type=str, trim=True)
    self.parser.add_argument('group_id', type=int)

    super(Conf, self).__init__()

  def _handle_group_id(self, args):
    group_id = args.get('group_id')
    # 如果 group_id 为空或者为0
    if not group_id:
      args['group_id'] = None

    return args

  def get(self, id):
    file_info = util.db_fetchone(pool,
        """select id, host_domain, host_ip, host_user_name, host_pass, ssh_key_path,
                  conf_file_path, conf_content, service_name, DATE_FORMAT(last_ch_time, '%%Y-%%m-%%d %%H:%%i') AS last_ch_time, comment, group_id
             from conf_file_info where id= %s""", (id, ))

    if file_info and not file_info.get('conf_content'):
      load_result = util.load_conf_info_to_db(file_info, pool)
    else:
      load_result = {}

    return {'data':file_info, 'load_result':load_result}

  def post(self, id):
    args = self.parser.parse_args()
    args = self._handle_group_id(args)
    sql = """
      insert into conf_file_info(host_domain, host_ip, host_user_name, ssh_key_path,
                            host_pass, conf_file_path, service_name, comment, last_ch_time, group_id)
      values(%(host_domain)s, %(host_ip)s, %(host_user_name)s, %(ssh_key_path)s,
                            %(host_pass)s, %(conf_file_path)s, %(service_name)s, %(comment)s, now(), %(group_id)s)
      """

    util.db_execute(pool, sql, args)

    final = util.get_return_info(True)
    return final

  def put(self, id):
    args = self.parser.parse_args()
    args = self._handle_group_id(args)
    args['id'] = id

    sql = """ update conf_file_info set host_domain = %(host_domain)s,
                                        host_ip = %(host_ip)s,
                                        host_user_name = %(host_user_name)s,
                                        ssh_key_path = %(ssh_key_path)s,
                                        host_pass = %(host_pass)s,
                                        conf_file_path = %(conf_file_path)s,
                                        service_name = %(service_name)s,
                                        comment = %(comment)s,
                                        last_ch_time = now(),
                                        group_id = %(group_id)s
              where id = %(id)s """

    util.db_execute(pool, sql, args)

    final = util.get_return_info(True)
    return final

  def delete(self, id):
    util.db_execute(pool, "delete from conf_file_info where id = %s", (id, ) )

    final = util.get_return_info(True)
    return final


class ParseConf(Resource):
  """将erl的配置文件信息解析成json格式
  """
  def get(self, id):
    final = {'json':{'data':u'文件为空'}, 'file_info':{}}

    file_info = util.db_fetchone(pool, 'select host_domain, conf_file_path, conf_content from conf_file_info where id = %s', (id, ) )
    if not file_info:
      return jsonify(final)

    # 文件内容还未加载
    if not file_info.get('conf_content'):
      util.load_conf_info_to_db(file_info, pool)
      # 重新获取一次
      file_info = util.db_fetchone(pool, 'select host_domain, conf_file_path, conf_content from conf_file_info where id = %s', (id, ) )

    conf_file_path = file_info.get('conf_file_path')
    # 是 erl文件才解析
    if conf_file_path and conf_file_path.endswith('.erl') and file_info.get('conf_content'):
      try:
        tuple_list = erl_terms.decode(file_info['conf_content'])
      except Exception, e:
        final = {'json':{'data':u'文件解析失败，请确定是标准的erl配置文件格式, err_info:%s' % str(e)},
                        'file_info':file_info}
        return jsonify(final)

      convert_result = util.convert_tuple_to_map(tuple_list, 'data')
      final = {'json':convert_result, 'file_info':file_info}
    else:
      final = {'json':{'data':u'文件不是erl格式，暂时不支持解析为json格式'}, 'file_info':file_info}

    return final


class LoadConf(Resource):
  def get(self, id):
    """从数据库获取配置文件的信息，并存放到mysql中
    """
    file_info = util.db_fetchone(pool, 'select * from conf_file_info where id = %s',(id, ) )
    final = util.load_conf_info_to_db(file_info, pool);
    return final


class GroupList(Resource):
  def get(self):
    result = util.db_fetchall(pool, "select * from conf_group")
    return {'data':result}


class Group(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('name', type=str)
    self.parser.add_argument('comment', type=str)
    super(Group, self).__init__()

  def get(self, id):
    pass

  def post(self, id):
    args = self.parser.parse_args()

    sql = 'insert into conf_group(name, comment) values(%(name)s, %(comment)s)'
    util.db_execute(pool, sql, args)

    final = util.get_return_info(True)
    return final

  def put(self, id):
    args = self.parser.parse_args()
    args['id'] = id

    sql = 'update conf_group set name = %(name)s, comment = %(comment)s where id = %(id)s'
    util.db_execute(pool, sql, args)

    final = util.get_return_info(True)
    return final

  def delete(self, id):
    try:
      util.db_execute(pool, "delete from conf_group where id = %s", (id, ) )
    except Exception, e:
      final = util.get_return_info(False, u'删除失败，此分组作为外键被关联')
      return final

    final = util.get_return_info(True)
    return final


# restful
api = Api(app)

api.add_resource(ConfList, '/confs', endpoint = 'conf_list')
api.add_resource(Conf, '/confs/<int:id>', endpoint = 'conf')

api.add_resource(ParseConf, '/parse/conf/<int:id>', endpoint = 'parse_conf')
api.add_resource(LoadConf, '/load/conf/<int:id>', endpoint = 'load_conf')

api.add_resource(GroupList, '/groups', endpoint = 'group_list')
api.add_resource(Group, '/groups/<int:id>', endpoint = 'group')



if __name__ == "__main__":
  app.run(host='192.168.2.121', port=8888, debug=True)