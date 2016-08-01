# encoding:utf-8
from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin

from flask_restful import Api, Resource, reqparse

import MySQLdb
from  DBUtils.PooledDB import PooledDB

import erl_terms
import util
import config

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
CORS(app, origins = "*", methods = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'])

# DB pool
pool = PooledDB(MySQLdb, 5,
                host = config.mysql['host'],
                user = config.mysql['user'],
                passwd = config.mysql['passwd'],
                db = config.mysql['db'],
                port = config.mysql['port'],
                charset = 'utf8',
                use_unicode = True)

common_sql = """ select a.id, a.host_domain, a.host_ip, a.host_user_name, a.host_pass, a.ssh_key_path,
                    IFNULL(a.conf_file_path, b.conf_file_path) as conf_file_path,
                    a.service_name, DATE_FORMAT(a.last_ch_time, '%%Y-%%m-%%d %%H:%%i') AS last_ch_time,
                    a.comment, a.group_id, b.name as group_name
               from conf_file_info a join conf_group b on a.group_id = b.id """

common_sql_content = """ select a.id, a.host_domain, a.host_ip, a.host_user_name, a.host_pass, a.ssh_key_path,
                    IFNULL(a.conf_file_path, b.conf_file_path) as conf_file_path,
                    a.service_name, DATE_FORMAT(a.last_ch_time, '%%Y-%%m-%%d %%H:%%i') AS last_ch_time,
                    a.comment, a.group_id, b.name as group_name a.conf_content
               from conf_file_info a join conf_group b on a.group_id = b.id """

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
    sql = common_sql + """ where 1=1 """

    group_id = args.get('group_id')
    kw = args.get('kw')

    sql_param = []

    if group_id:
      sql += ' and a.group_id = %s '
      sql_param.append(group_id)
    if kw:
      sql += ' and a.conf_content like %s '
      sql_param.append( '%' + kw + '%' )

    sql += ' order by a.host_domain'

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
    self.parser.add_argument('comment', type=str, trim=True)
    self.parser.add_argument('group_id', type=int, required = True)

    super(Conf, self).__init__()

  def get(self, id):
    file_info = util.db_fetchone(pool, common_sql_content + "where a.id= %s", (id, ))

    if file_info and not file_info.get('conf_content'):
      load_result = util.load_conf_info_to_db(file_info, pool)
      file_info = util.db_fetchone(pool, common_sql_content + "where a.id= %s", (id, ))
    else:
      load_result = {}

    return {'data':file_info, 'load_result':load_result}

  def post(self, id):
    args = self.parser.parse_args()
    if not args.get('group_id'):
      return util.get_return_info(False, u'必须选择一个分组')

    sql = """
      insert into conf_file_info(host_domain, host_ip, host_user_name, ssh_key_path,
                            host_pass, comment, last_ch_time, group_id)
      values(%(host_domain)s, %(host_ip)s, %(host_user_name)s, %(ssh_key_path)s,
                            %(host_pass)s, %(comment)s, now(), %(group_id)s)
      """
    util.db_execute(pool, sql, args)

    final = util.get_return_info(True)
    return final

  def put(self, id):
    args = self.parser.parse_args()
    if not args.get('group_id'):
      return util.get_return_info(False, u'必须选择一个分组')

    args['id'] = id

    sql = """ update conf_file_info set host_domain = %(host_domain)s,
                                        host_ip = %(host_ip)s,
                                        host_user_name = %(host_user_name)s,
                                        ssh_key_path = %(ssh_key_path)s,
                                        host_pass = %(host_pass)s,
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
    final = {'json':{'data':u'文件内容为空，请查看详情'}, 'file_info':{}}
    sql = common_sql_content + ' where a.id = %s'

    file_info = util.db_fetchone(pool, sql, (id, ) )
    if not file_info:
      return final

    # 文件内容还未加载
    if not file_info.get('conf_content'):
      return final

    conf_file_path = file_info.get('conf_file_path')
    # 是 erl文件才解析
    if conf_file_path:
      try:
        tuple_list = erl_terms.decode(file_info['conf_content'])
        convert_result = util.convert_tuple_to_map(tuple_list, 'data')

        final = {'json':convert_result, 'file_info':file_info}
      except Exception, e:
        final = {'json':{'data':u'文件解析失败，请确定是标准的erl配置文件格式, err_info:%s' % str(e)}, 'file_info':file_info}
    else:
      final = {'json':{'data':u'文件不是erl格式，暂时不支持解析为json格式'}, 'file_info':file_info}

    return final


class LoadConf(Resource):
  def get(self, id):
    """从数据库获取配置文件的信息，并存放到mysql中
    """
    file_info = util.db_fetchone(pool, common_sql + "where a.id = %s",(id, ) )
    final = util.load_conf_info_to_db(file_info, pool);
    return final


class groupSearch(Resource):
  """分组选择查询接口，分层级
  """
  def __init__(self):
    self.parser = reqparse.RequestParser()
    # 表示只显示 section，不显示具体的机器名
    self.parser.add_argument('only_section', type=int, trim=True)
    super(groupSearch, self).__init__()


  def build_map(self, db_list):
    result = {}
    for value in db_list:
      value_a = value['a']
      value_b = value['b']
      value_c = value['c']
      value_d = value['d']

      if value_a and not result.get(value_a):
        result[value_a] = {}

      if value_b and not result[value_a].get(value_b):
        result[value_a][value_b] = {}

      if value_c and not result[value_a][value_b].get(value_c):
        result[value_a][value_b][value_c] = {}

      if value_d and not result[value_a][value_b][value_c].get(value_d):
        result[value_a][value_b][value_c][value_d] = {}

    return result

  def recursion_map(self, deep_map):
    children = []
    if deep_map:
      for key, value in deep_map.items():
        key_split = key.split(':')
        entity = { 'name':key_split[1], 'id': key_split[0] , 'children': [] }
        children.append( entity )

        if value:
          entity['children'] = self.recursion_map(value)

    else:
      # 为空map
      pass

    children.sort(key=lambda x: x['name'])
    return children

  def recursion_map_only_section(self, deep_map):
    """只添加section
    """
    children = []
    if deep_map:
      for key, value in deep_map.items():
        key_split = key.split(':')
        entity = { 'name':key_split[1], 'id': key_split[0] , 'children': [] }

        if value:
          entity['children'] = self.recursion_map_only_section(value)

          children.append( entity )
    else:
      # 为空map
      pass

    children.sort(key=lambda x: x['name'])
    return children

  def get(self):
    # result = util.db_fetchall(pool, "select * from conf_group order by name")
    args = self.parser.parse_args()

    sql = """
      select concat(a.id, ':', a.name) a, concat(b.id, ':', b.name) b, concat(c.id, ':', c.name) c, concat(d.id, ':', d.name) d from
      conf_group a
      left join conf_group b on b.parent = a.id
      left join conf_group c on c.parent = b.id
      left join conf_group d on c.parent = c.id
      where a.parent is null
      order by d.name desc, c.name desc, b.name desc, a.name desc """
    db_list = util.db_fetchall(pool, sql)
    result = self.build_map(db_list)

    if args.get('only_section'):
      final = self.recursion_map_only_section(result)
    else:
      final = self.recursion_map(result)
    return {'data':final}


class groupList(Resource):
  """分组列表，用于页面展示
  """
  def get(self):
    sql = """ select distinct a.id, a.name, a.comment, a.conf_file_path, a.parent, c.name as parent_name,
               (case when b.descendant_id > 0 then 'false' else 'true' end) as is_leaf
                from conf_group a
                left join conf_group_relation b
                  on a.id = b.ancestor_id
                 and b.ancestor_id <> b.descendant_id
                left join conf_group c
                  on a.parent = c.id
               order by a.name"""
    result = util.db_fetchall(pool, sql)
    return {'data': result}


class Group(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('name', type=str)
    self.parser.add_argument('comment', type=str)
    self.parser.add_argument('conf_file_path', type=str)
    super(Group, self).__init__()

  def get(self, id):
    pass

  def post(self, id):
    args = self.parser.parse_args()

    sql = 'insert into conf_group(name, comment, conf_file_path) values(%(name)s, %(comment)s, %(conf_file_path)s)'
    util.db_execute(pool, sql, args)

    final = util.get_return_info(True)
    return final

  def put(self, id):
    args = self.parser.parse_args()
    args['id'] = id

    sql = 'update conf_group set name = %(name)s, comment = %(comment)s, conf_file_path = %(conf_file_path)s where id = %(id)s'
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

api.add_resource(groupSearch, '/group/search', endpoint = 'group_search')

api.add_resource(groupList, '/groups', endpoint = 'group_list')
api.add_resource(Group, '/groups/<int:id>', endpoint = 'group')



if __name__ == "__main__":
  app.run(host = config.server['host'], port = config.server['port'], debug = config.server['debug'])




