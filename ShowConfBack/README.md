#show-conf-back
> 本项目为配置管理系统的后端，使用Python Flask 的restful接口开发

##目录结构
<pre>
│  create_table.sql    # 数据库表创建文件
│  requirements.txt    # python 安装依赖文件
│  config.py           # 后端配置文件，不上库
│  README.md           # 项目说明
│  index.html          # 首页
│  restful.py          # restful API接口
│  run.py              # 项目运行文件
│  util.py             # 工具函数文件
</pre>

##安装
```
sudo pip install -r requirements.txt
```

##说明
```
config.py 由于不在库上，需要自己新建文件并配置以下内容：
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

##运行
```
sudo python run.py
```

##访问
```
在浏览器地址栏输入http://127.0.0.1:8888
```