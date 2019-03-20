import threading
import datetime
import time
import pymysql.cursors


class AsyncTask:
    def __init__(self):
        pass

    def TaskA(self):
        b = 0
        conn = pymysql.connect(host='localhost',
                                       user='root',
                                       password='1150',
                                       db='test',
                                       charset='utf8')
        print("MySQL coonected well")

        while (True):
            now = datetime.datetime.now()
            newday = now.strftime('%H_%M_%S')
            now = now.strftime('%Y_%m_%d')

            str_time = 'a' + now

            print(newday)

            if newday=='20_27_30':

                ## Create Table
                with conn.cursor() as cursor:
                    sql = '''
                        CREATE TABLE ''' + str_time + ''' (
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
                
                ## Create worker's list at table
                with conn.cursor() as cursor:
                    sql = 'INSERT INTO ' + str_time + ' (name) SELECT name FROM list'
                    cursor.execute(sql)
                conn.commit()
                print("worker's list created")

            time.sleep(1)
        threading.Timer(1,self.TaskA).start()

def main():
    at = AsyncTask()
    at.TaskA()

if __name__ == '__main__':
    main()