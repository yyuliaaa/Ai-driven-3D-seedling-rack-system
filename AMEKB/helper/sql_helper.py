import pyodbc

class SQLHelper:
    def __init__(self):
        self.conn_str = "DRIVER={SQL Server};SERVER=DESKTOP-MLD4123;DATABASE=农业机械装备知识库系统;Trusted_Connection=yes;"

    def get_connection(self):
        return pyodbc.connect(self.conn_str)

    def execute_query(self, sql, params=None):
        conn = None
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"执行查询时发生错误: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def fetch_data(self, sql, params=None):
        conn = None
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"查询数据时发生错误: {e}")
            raise
        finally:
            if conn:
                conn.close()