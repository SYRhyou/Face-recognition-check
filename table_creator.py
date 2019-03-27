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
                                       password='438520',
                                       db='fbtpduf',
                                       charset='utf8')
        print("MySQL coonected well")

        while (True):
            now = datetime.datetime.now()
            newday = now.strftime('%H_%M_%S')
            now = now.strftime('%Y_%m_%d')

            str_time = 'a' + now

            print(newday)

            if newday=='15_58_00':

                ## Create Table
                with conn.cursor() as cursor:
                    sql = '''
                        CREATE TABLE ''' + str_time + ''' (
                            ENO varchar(45) NOT NULL,
                            NAME varchar(45) NULL,
                            DEPARTMENT varchar(45) NULL,
                            POSITION varchar(45) NULL,
                            ENTER_TIME varchar(45) NULL,
                            EXIT_TIME varchar(45) NULL,
                            ATTENDANCE varchar(45) NULL,
                            primary key(ENO)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                    '''
                    cursor.execute(sql)
                conn.commit()
                print(str_time+" Table Created \n")
                
                ## Create worker's list at table
                with conn.cursor() as cursor:
                    sql = 'INSERT INTO ' + str_time + ' (ENO, NAME, DEPARTMENT, POSITION) SELECT * FROM list'
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