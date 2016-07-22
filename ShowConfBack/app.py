# encoding:utf-8
from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin
from webargs import fields
from webargs.flaskparser import use_args

import MySQLdb
from  DBUtils.PooledDB import PooledDB

import util
import erl_terms

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


app = Flask(__name__)

# CORS(app, origins="http://zptst.yunba.io")
CORS(app)


pool = PooledDB(MySQLdb, 5, host="abj-elogic-test1.yunba.io",
                    user="yunba",
                    passwd="yunba321",
                    db="conf_show",
                    port=3306,
                    charset='utf8',
                    use_unicode=True)

@app.route('/all_conf/')
@use_args({'kw': fields.Str(),
           'group_id': fields.Int(),
          })
def all_conf(args):
  """加载所有配置文件列表
  """
  print args
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
  return jsonify({'data':result})


@app.route('/conf_info/')
@use_args({'conf_id': fields.Int(required=True)})
def conf_info(args):
  """获取单个配置文件信息
  """
  file_info = util.db_fetchone(pool, 'select * from conf_file_info where id= %s',
                                  (args['conf_id'],))

  if file_info and not file_info.get('conf_content'):
    util.load_conf_info_to_db(file_info, pool)

  return jsonify({'data':file_info})



@app.route('/parse/conf/')
@use_args({'conf_id': fields.Int(required=True)})
def parse_conf(args):
  """将erl的配置文件信息解析成json格式
  """
  final = {'json':{'data':u'文件为空'}, 'file_info':{}}

  file_info = util.db_fetchone(pool, 'select * from conf_file_info where id = %s',
                                      (args['conf_id'], ) )

  if not file_info:
    return jsonify(final)

  # 文件内容还未加载
  if not file_info.get('conf_content'):
    util.load_conf_info_to_db(file_info, pool)

    # 重新获取一次
    file_info = util.db_fetchone(pool, 'select * from conf_file_info where id = %s',
                                      (args['conf_id'], ) )

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

  return jsonify(final)



@app.route('/load_conf/')
@use_args({'conf_id': fields.Int(required=True)})
def load_conf(args):
  """从数据库获取配置文件的信息，并存放到mysql中
  """
  file_info = util.db_fetchone(pool, 'select * from conf_file_info where id = %s',
              (args['conf_id'], ) )

  final = util.load_conf_info_to_db(file_info, pool);

  return jsonify(final)



@app.route('/input/file_info/', methods=['GET', 'POST'])
@use_args({
  'id': fields.Int(),
  'host_domain': fields.Str(),
  'host_ip': fields.Str(),
  'host_user_name': fields.Str(),
  'ssh_key_path': fields.Str(),
  'host_pass': fields.Str(),
  'conf_file_path': fields.Str(),
  'service_name': fields.Str(),
  'comment': fields.Str(),
  'group_id': fields.Function(deserialize=lambda x: None if not x or x == '0' else x),
})
def input_file_info(args):
  """输入配置文件相关信息到数据库
  """
  print args
  # 更新
  if args.get('id'):
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
  else:
    sql = """
      insert into conf_file_info(host_domain, host_ip, host_user_name, ssh_key_path,
                            host_pass, conf_file_path, service_name, comment, last_ch_time, group_id)
      values(%(host_domain)s, %(host_ip)s, %(host_user_name)s, %(ssh_key_path)s,
                            %(host_pass)s, %(conf_file_path)s, %(service_name)s, %(comment)s, now(), %(group_id)s)
      """

  util.db_execute(pool, sql, args)

  final = util.get_return_info(True)
  return jsonify(final)

@app.route('/load/group/')
def load_group():
  result = util.db_fetchall(pool, " select id, name from conf_group")
  return jsonify({'data':result})

@app.route('/test/')
@use_args({'sql':fields.Str(required=True)})
def test(args):
  util.db_execute(pool, args['sql'])
  return 'success'

@app.route('/')
def hello_world():
  """测试直接从远程机器读取配置文件
  """
  ssh = paramiko.SSHClient()

  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect("abj-elogic-test1.yunba.io",
    username="yunba", key_filename="/Users/weizhiyun078/.ssh/id_rsa")

  stdin, stdout, stderr = ssh.exec_command("cat ~/yunba_portal/config.js")
  result =  stdout.readlines()
  print 'error:', stderr.readlines()

  return jsonify({'data': result})


if __name__ == "__main__":
  app.run(host='192.168.2.121', port=8888, debug=True)






