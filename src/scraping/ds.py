import mysql.connector
import os

class DS:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='db',
            user=os.environ.get('MYSQL_USER'),
            passwd=os.environ.get('MYSQL_PASSWORD'),
            db=os.environ.get('MYSQL_DATABASE'),
        )
        
    def read_latest_record(self) -> None | dict:
        cursor = self.conn.cursor()
        cols = ['record_id', 'song_id', 'difficulty', 'result_id', 'played_at', 'created_at']
        cursor.execute(f'SELECT {", ".join(cols)} FROM records ORDER BY played_at DESC LIMIT 1')
        row = cursor.fetchone()
        res = None
        if row is not None:
            res = {cols[i]: row[i] for i in range(len(cols))}
        cursor.close()
        return res
    
    def __del__(self):
        self.conn.close()
        
if __name__ == '__main__':
    ds = DS()
    print(ds.read_latest_record())