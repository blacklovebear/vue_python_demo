# encoding:utf-8
import oursql
import MySQLdb
import paramiko


def db_fetchall(pool, sql, param = ()):
  """
  从数据库获取数据
  """
  conn = pool.connection()
  cur = conn.cursor(MySQLdb.cursors.DictCursor);
  cur.execute(sql, param)

  result = cur.fetchall()

  cur.close()
  conn.close()
  return result


def db_fetchone(pool, sql, param = ()):
  """
  从数据库获取数据
  """
  conn = pool.connection()
  cur = conn.cursor(MySQLdb.cursors.DictCursor);
  cur.execute(sql, param)

  result = cur.fetchone()

  cur.close()
  conn.close()
  return result

def db_execute(pool, sql, param = ()):
  """数据库执行sql
  """
  conn = pool.connection()
  cur = conn.cursor();
  cur.execute(sql, param)

  print '受影响的行数', cur.rowcount
  conn.commit()

  cur.close()
  conn.close()

def db_executemany(pool, sql, param = ()):
  """数据库执行sql
  """
  conn = pool.connection()
  cur = conn.cursor();
  cur.executemany(sql, param)

  print '受影响的行数', cur.rowcount
  conn.commit()

  cur.close()
  conn.close()

def ssh_get_file_content(conf_info_dict):
  """
  通过数据库中的配置信息，ssh读取文件内容
  """
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  try:
    ssh.connect(conf_info_dict.get('host_domain'),
                username = conf_info_dict.get('host_user_name'),
                key_filename = conf_info_dict.get('ssh_key_path'))
  except Exception, e:
    # 连接出错
    error_info = str(e)
    return error_info, ''

  stdin, stdout, stderr = ssh.exec_command("cat " + conf_info_dict.get('conf_file_path'))
  file_content =  stdout.readlines()
  error_info = stderr.readlines()

  return error_info, file_content



def tuple_to_map(tuple_input):
  """将tuple转换为dict
  """
  if type(tuple_input[1]) == tuple:
    return {tuple_input[0]:list(tuple_input[1])}
  else:
    return {tuple_input[0]:tuple_input[1]}


def convert_tuple_to_map(conf_list, key):
  """将嵌套的tuple（从erl转换过来），转换为dict
  """
  temp = []
  for index, value in enumerate(conf_list):

    if type(value) == list:
      output = convert_tuple_to_map(value, key)
    elif type(value) == tuple:

      if type(value[1]) in [list, tuple]:

        if len(value[1]) >= 2 and type(value[1][1]) not in [tuple, list]:
          output = tuple_to_map( value )
        elif len(value[1]) == 1 and type(value[1][0]) not in [tuple, list]:
          output = tuple_to_map( value )
        else:
          output = convert_tuple_to_map(value[1], value[0])
      else:
        output = tuple_to_map( value )
    else:
      output = {key:value}

    temp.append(output)
  return {key:temp}


def get_return_info(status, error_massage='error'):
  """根据true or false 返回对应的信息
  """
  if status:
    return {'code':0, 'message':'success'}
  else:
    return {'code':-1, 'message':error_massage}


def load_conf_info_to_db(file_info, pool):
  """从机器拉取配置文件信息，如果成功并加载的数据库中
  """
  error_info, file_content = ssh_get_file_content(file_info)

  if error_info:
    final = get_return_info(False, str(error_info))
  else:
    db_execute(pool, "update conf_file_info set conf_content = %s, last_ch_time = now() where id =%s ",
                     (''.join(file_content), file_info['id']) )
    final = get_return_info(True)

  return final


