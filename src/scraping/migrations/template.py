# the file name's format should be like "yyyymmdd_HHMM_filename.py"

import mysql.connector
import os
import sys

connection = None

def up(connection: mysql.connector.MySQLConnection, cursor):
    pass
    
def down(connection: mysql.connector.MySQLConnection, cursor):
    pass
        
def main():
    cmds = sys.argv # あとで引数を入れておく
    connection = None
    if cmds[1] == None:
        return
    
    try:
        connection = mysql.connector.connect(
            host='db',
            user=os.environ.get('MYSQL_USER'),
            passwd=os.environ.get('MYSQL_PASSWORD'),
            db=os.environ.get('MYSQL_DATABASE'),
        )
        
        cursor = connection.cursor()
        if cmds[1] == 'up':
            up(connection, cursor)
        elif cmds[1] == 'down':
            if os.environ.get('MIGRATION_MODE') == 'prod':
                print('This command will drop all the **PROD** tables! Are you sure?')
                if choice_yn():
                    down(connection, cursor)
                else:
                    print('canceled')
        elif cmds[1] == 'recreate':
            if os.environ.get('MIGRATION_MODE') == 'prod':
                print('This command will drop all the **PROD** tables! Are you sure?')
                if choice_yn():
                    down(connection, cursor)
                    up(connection, cursor)
                else:
                    print('canceled')
        else:
            raise(Exception(f'unknown arg {cmds[1]}'))
        cursor.close()
        
    except Exception as e:
        # いずれメール送信するようにする
        print(f"Error Occured: {e}")
        
    finally:
        if connection is not None and connection.is_connected():
            connection.close()

def choice_yn():
    while True:
        choice = input("yes or no: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

if __name__ == '__main__':
    main()