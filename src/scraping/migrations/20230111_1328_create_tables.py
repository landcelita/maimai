import mysql.connector
import os
import sys

connection = None

def up(connection: mysql.connector.MySQLConnection, cursor):
    cursor.execute('''
        CREATE TABLE records(
            record_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            song_id INT NOT NULL,
            difficulty INT NOT NULL COMMENT '1: BASIC, 2: ADVANCED, 3: EXPERT, 4: MASTER, 5: Re:MASTER, 0: Other',
            result_id INT NOT NULL,
            played_at DATETIME NOT NULL,
            created_at DATETIME NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE songs(
            song_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200),
            composer VARCHAR(200),
            genre VARCHAR(200),
            maimainet_idx VARCHAR(200),
            is_standard BOOLEAN
        );
    ''')
    cursor.execute('''
         CREATE TABLE results(
            result_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            achievement FLOAT,
            is_new_record BOOLEAN,
            dx_score INT,
            max_dx_score INT,
            fast INT,
            late INT,
            tap_cp INT,
            tap_p INT,
            tap_gr INT,
            tap_gd INT,
            tap_ms INT,
            hold_cp INT,
            hold_p INT,
            hold_gr INT,
            hold_gd INT,
            hold_ms INT,
            slide_cp INT,
            slide_p INT,
            slide_gr INT,
            slide_gd INT,
            slide_ms INT,
            touch_cp INT,
            touch_p INT,
            touch_gr INT,
            touch_gd INT,
            touch_ms INT,
            break_cp INT,
            break_p INT,
            break_gr INT,
            break_gd INT,
            break_ms INT,
            max_combo INT,
            full_combo INT
        )
    ''')
    connection.commit()
    
    cursor.execute('SHOW TABLES;')
    rows = cursor.fetchall()
    print(rows)
    
def down(connection: mysql.connector.MySQLConnection, cursor):
    cursor.execute("DROP TABLE IF EXISTS records")
    cursor.execute("DROP TABLE IF EXISTS songs")
    cursor.execute("DROP TABLE IF EXISTS results")
    connection.commit()
        
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