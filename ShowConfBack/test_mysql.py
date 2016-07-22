import oursql
from  DBUtils.PooledDB import PooledDB

pool = PooledDB(oursql, 5, host="abj-elogic-test1.yunba.io",
                    user="yunba",
                    passwd="yunba321",
                    db="conf_show",
                    port=3306)

conn = pool.connection()


cur = conn.cursor(oursql.DictCursor);

cur.execute('select * from conf_file_info')

resut = cur.fetchall()

print resut

conn.close()


# if __name__ == '__main__':
