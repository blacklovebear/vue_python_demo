#show-conf-back
> 本项目为配置管理系统的后端，使用Python Flask 的restful接口开发

##目录结构
```
│  create_table.sql    # 数据库表创建文件
│  requirements.txt    # python 安装依赖文件
│  config.py           # 后端配置文件
│  README.md           # 项目说明
│  index.html          # 首页
│  restful.py          # restful API接口
│  run.py              # 项目运行文件
│  util.py             # 工具函数文件
```

##安装
```
sudo apt-get install python-dev libffi-dev mysql-server
sudo apt-get install libmysqlclient-dev
sudo pip install -r requirements.txt
```

##说明
```
config.py 中的配置内容根据你自身的需要修改
# mysql server info
mysql = {
  'host': "your_host",
  'user': "your_user",
  'passwd': "your_password",
  'db': "your_db",
  'port': 3306
}

# server
server = {
  'host':'127.0.0.1',
  'port':8888,
  'debug': True,
}
```

##本地运行
```
sudo python run.py
```

##更新Ansible配置文件
curl http://localhost:8888/ansible/upload --data-urlencode "file_content=`cat ./origin.txt`"

##线上部署
```
线上采取 supervisor + gunicorn + tornado的方式部署
详细部署参考supervisor的配置文件 /etc/supervisor/supervisor.conf

[program:config_display]
process_name=%(program_name)s
numprocs=1
user=yunba
command=gunicorn -k tornado -w4 -b 123.56.235.126:8888 restful:app                      ; supervisor启动命令
directory=/home/yunba/configure_display/ShowConfBack
startsecs=0                                                                             ; 启动时间
stopwaitsecs=0                                                                          ; 终止等待时间
autostart=true                                                                          ; 是否自动启动
autorestart=true                                                                        ; 是否自动重启
stdout_logfile=/home/yunba/configure_display/log/output.log                             ; log 日志
stderr_logfile=/home/yunba/configure_display/log/error.err
```

##访问
```
在浏览器地址栏输入http://127.0.0.1:8888
```