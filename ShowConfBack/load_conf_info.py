# encoding:utf-8
import re

import MySQLdb
from  DBUtils.PooledDB import PooledDB

import util
import config

import sys, getopt
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import configparser


# DB pool
pool = PooledDB(MySQLdb, 5,
                host = config.mysql['host'],
                user = config.mysql['user'],
                passwd = config.mysql['passwd'],
                db = config.mysql['db'],
                port = config.mysql['port'],
                charset = 'utf8',
                use_unicode = True)

config = configparser.ConfigParser()


def trans_origin_text_to_ini(input_file_name, output_file_name):
  pattern = re.compile(r"^\S+")
  input_file = open(input_file_name, 'r')
  output_file = open(output_file_name, 'w')

  for i, line in enumerate(input_file):
      four_letter_words = pattern.findall(line)
      for word in four_letter_words:
          if word.startswith('['):
            output_file.write('%s\n' % word)
          else:
            output_file.write('%s\n' % (word + '=0'))

  input_file.close()
  output_file.close()

def config_read_file(file_name):
  config.read(file_name)


def get_conf_group():
  """获取分组数据
  """
  group_list = []
  for section_name, section_value in config.items():

    if section_name.endswith('children'):
      print section_name[0:-9]
      group_list.append((section_name[0:-9],))

      # children 下面还是分组
      for field_name, field_value in section_value.items():
        group_list.append((field_name,))

    else:
      group_list.append((section_name,))
  # 去掉第一个u'DEFAULT'
  return list(set(group_list[1:]))


def truncate_tables():
  sql_list = ['DELETE FROM %s' % table for table in
                  ['conf_file_info', 'conf_group_relation', 'conf_group']]

  util.db_trans_execute(pool, sql_list, [(),(),()])


def insert_group_data(group_list):
  sql = """ insert into conf_group(name) values(%s) """
  util.db_executemany(pool, sql, group_list);


def get_connect_child_and_parent_list():
  connect_list = []
  for section_name, section_value in config.items():

    if section_name.endswith('children'):
      section_temp = section_name[0:-9]
      # 将自己加入关系链
      # connect_list.append( (section_temp, section_temp) )
      # children 下面还是分组
      for field_name, field_value in section_value.items():
        connect_list.append((section_temp, field_name))

  return list(set(connect_list))

def insert_group_relation(connect_list):
  sql = """ insert into conf_group_relation(ancestor_id, descendant_id)
            select a.id, b.id from(
                select id from conf_group where name = %s
              ) a
              join
              ( select id from conf_group where name = %s ) b
  """
  util.db_executemany(pool, sql, connect_list);


def update_child_parent_connection(connect_list):
  sql = """ update conf_group a, (select id from conf_group where name = %s) b
          set a.parent = b.id  where a.name = %s """

  util.db_executemany(pool, sql, connect_list)


def get_conf_file_info_list():
  conf_file_list = []
  for section_name, section_value in config.items():

    if section_name.endswith('children'):
      pass
    else:
      # children 下面还是分组
      for field_name, field_value in section_value.items():
        conf_file_list.append((field_name, section_name))

  return list(set(conf_file_list))


def insert_conf_list(conf_file_list):
  sql = """ insert into conf_file_info(host_domain, group_id)
                select %s, id from conf_group where conf_group.name = %s """
  util.db_executemany(pool, sql, conf_file_list);


def add_host_domain_suffix():
  sql = """update conf_file_info set host_domain = concat(host_domain,'.yunba.io')
            where host_domain not like '%%.yunba.io'; """
  util.db_execute(pool, sql)


def set_conf_file_path_for_group():
  """将已知的一些配置文件路径添加到数据库
  """
  config = {
    'elogic': '/home/yunba/elogic/rel/files/app.config',
    'erest':  '/home/yunba/erest/rel/files/app.config',
    'emqtt': '/home/yunba/etopicfs/files/app.config',
    'etopicfs': '/home/yunba/etopicfs/files/app.config',
  }
  sql_list = []
  param_list = []

  sql ="""
    update conf_group
    set conf_file_path = %s
    where parent in (select id from (select * from conf_group) a where name like %s)
    and id not in( select distinct ancestor_id from conf_group_relation )  """

  for key, value in config.items():
    sql_list.append( sql )
    param_list.append( (value, '%' + key + '%') )

  util.db_trans_execute(pool, sql_list, param_list)


def update_conf_file_host_user_name():
  sql = """ update conf_file_info set host_user_name ='yunba' where host_user_name is null """
  util.db_execute(pool, sql)


def update_conf_file_ssh_key():
  sql = """ update conf_file_info set ssh_key_path ='/home/yunba/.ssh/id_rsa' where ssh_key_path is null """
  util.db_execute(pool, sql)


def run(ansible_file):
  trans_origin_text_to_ini(ansible_file, 'final.ini')
  config_read_file('final.ini')

  group_list = get_conf_group()

  if not group_list:
    sys.exit()

  truncate_tables()
  insert_group_data(group_list)

  connect_list = get_connect_child_and_parent_list()
  insert_group_relation(connect_list)
  update_child_parent_connection(connect_list)

  conf_file_list = get_conf_file_info_list()
  insert_conf_list(conf_file_list)

  add_host_domain_suffix()
  set_conf_file_path_for_group()
  update_conf_file_host_user_name()

  update_conf_file_ssh_key()

def main(argv):
  ansible_file = ''
  try:
    opts, args = getopt.getopt(argv,"hc:",["config="])
  except getopt.GetoptError:
    print 'load_conf_info.py -c <ansible_conf_file>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'load_conf_info.py -c <ansible_conf_file>'
      sys.exit()
    elif opt in ("-c", "--config"):
      run(arg)


if __name__ == '__main__':
  main(sys.argv[1:])



