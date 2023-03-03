import psycopg2
from psycopg2 import connect,extensions,sql

class ManageDatabase:
    def __init__(self):
        pass
        
    def database_connection(self,db_name,db_user,db_password,db_host):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        try:
            db_connection = psycopg2.connect(
            database=self.db_name, user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port= '5432'
            )
            autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
            db_connection.set_isolation_level(autocommit)
            # db_cursor=db_connection.cursor()
            return db_connection
        except (Exception, psycopg2.Error) as error:
            return error
            # db_connection_error=f"Database Connection Error:{error}"
            # return db_connection_error


def query_test():
    test = ManageDatabase().database_connection("flask_api", "dbadmin", "Abc123Abc123", "172.18.0.2")
    db_cursor=test.cursor()
    # select_query = "SELECT  id,fullname,customid,email FROM users where id=\'{id}\'".format(id=id)
    # db_cursor.execute(select_query)
    # response={}
    # results=db_cursor.fetchone()
    # response['id']=results[0]
    # response['fullname']=results[1]
    # response['customid']=results[2]
    # response['email']=results[3]
    # print(response,type(response))
    print(db_cursor)


query_test()
