use conf_show;

CREATE TABLE IF NOT EXISTS conf_group(
  `id`          MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          char(32)
);

CREATE TABLE IF NOT EXISTS conf_file_info(
  `id`            MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  host_domain     varchar(64),                      -- 所在机器域名
  host_ip         char(32),                         -- 机器ip
  host_user_name  char(32),                         -- 机器用户名
  host_pass       char(32),                         -- 机器密码
  ssh_key_path    varchar(128),                     -- ssh key所在路径
  conf_file_path  varchar(256) NOT NULL,            -- 配置文件路径
  service_name    varchar(64),                      -- 所属服务名称
  conf_content    MEDIUMTEXT,                       -- 配置文件内容信息
  last_ch_time    DATETIME,                         -- 最后一次修改时间
  comment         varchar(64),                      -- 备注信息
  group_id        MEDIUMINT,                        -- 所属组
  FOREIGN KEY(group_id) REFERENCES conf_group(id)
);

insert into conf_group(name) values('test');
commit;

insert into conf_file_info(host_domain, host_user_name, ssh_key_path,
                          conf_file_path, service_name, group_id)
  values('abj-elogic-test1.yunba.io', 'yunba', '/Users/weizhiyun078/.ssh/id_rsa',
    '~/yunba_portal/config.js', 'yunba_portal', 1);

insert into conf_file_info(host_domain, host_user_name, ssh_key_path,
                          conf_file_path, service_name, group_id)
  values('abj-elogic-test1.yunba.io', 'yunba', '/Users/weizhiyun078/.ssh/id_rsa',
    '~/test_conf_show/test.erl', 'test_erl', 1);

commit;