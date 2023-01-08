import mysql.connector
import os

connection = None

try:
    connection = mysql.connector.connect(
        host='db',
        user=os.environ.get('MYSQL_USER'),
        passwd=os.environ.get('MYSQL_PASSWORD'),
        db=os.environ.get('MYSQL_DATABASE'),
    )
    cursor = connection.cursor()
    sql = '''
        CREATE TABLE records(
            records_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            song_id INT NOT NULL,
            result_id INT NOT NULL,
            created_at DATETIME NOT NULL
        )
    '''
    cursor.execute(sql)
    
    cursor.execute("SHOW TABLES")
    print(cursor.fetchall())
    
    cursor.close()
    
except Exception as e:
    # いずれメール送信するようにする
    print(f"Error Occured: {e}")
    
finally:
    if connection is not None and connection.is_connected():
        connection.close()