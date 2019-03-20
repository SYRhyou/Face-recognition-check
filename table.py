import pymysql.cursors
import datetime
 
conn = pymysql.connect(host='localhost',
        user='root',
        password='1150',
        db='test',
        charset='utf8')
print("MySQL coonected well")
 
now = datetime.datetime.now()
now = now.strftime('%Y_%m_%d')
str_time = 'a' + now

with conn.cursor() as cursor:
    sql = '''
        CREATE TABLE '''+ str_time +''' (
            name varchar(45) NOT NULL,
            hitime varchar(45) NULL,
            byetime varchar(45) NULL,
            attendance varchar(45) NULL,
            primary key(name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''

    cursor.execute(sql)
conn.commit()
print(str_time+" Table Created \n")

with conn.cursor() as cursor:
    sql = 'INSERT INTO ' + str_time + ' (name) SELECT name FROM list'
    cursor.execute(sql)
conn.commit()
print("worker's list created")