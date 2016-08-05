# encoding:utf-8

import MySQLdb
from  DBUtils.PooledDB import PooledDB

import erl_terms
import util
import config

import sys
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
config.read('full.ini')


def parse_from_ini_file():
  for section_name, section_value in config.items():
    for field_name, field_value in section_value.items():
      print field_name, ': ', field_value

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
    where name like %s and id not in( select distinct ancestor_id from conf_group_relation )  """

  for key, value in config.items():
    sql_list.append( sql )
    param_list.append( (value, '%' + key + '%') )

  util.db_trans_execute(pool, sql_list, param_list)


def update_conf_file_host_user_name():
  sql = """ update conf_file_info set host_user_name ='yunba' where host_user_name is null """
  util.db_execute(pool, sql)

if __name__ == '__main__':
  pass
  # group_list = get_conf_group()
  # insert_group_data(group_list)

  # connect_list = get_connect_child_and_parent_list()
  # insert_group_relation(connect_list)
  # update_child_parent_connection(connect_list)

  # conf_file_list = get_conf_file_info_list()
  # insert_conf_list(conf_file_list)

  # add_host_domain_suffix()
  # set_conf_file_path_for_group()
  # update_conf_file_host_user_name()




