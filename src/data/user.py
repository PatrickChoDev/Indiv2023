import psycopg2


class AuthenticationDatabase:
    def __init__(self,host="pgsql.docker",database="indiv",user="indiv",password="indiv"):
        self.__conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password)
        

    def status(self):
        return self.__conn.info
    
    def login(self,username: str,password: str):
        cursor = self.__conn.cursor()
        cursor.execute(f"SELECT user_id,username,chainlit_role FROM users WHERE username='{username}' and password='{password}'")
        row = cursor.fetchone()
        try:
            self.__conn.commit()
        except psycopg2.Error as e:
            print(e)
            return None
        cursor.close()
        return row
    
    def getRoleLevel(self,user_id):
        if not user_id: return 0
        cursor = self.__conn.cursor()
        cursor.execute(f"SELECT role FROM users WHERE user_id='{user_id}'")
        row = cursor.fetchone()
        try:
            self.__conn.commit()
        except psycopg2.Error as e:
            print(e)
            return 0
        cursor.close()
        match row[0]:
            case "admin": return 3
            case "professor": return 2
            case "student": return 1
        return 0


if __name__ == "__main__":
    auth_db = AuthenticationDatabase()
    print(auth_db.login("admin","pass"))
    print(auth_db.getRoleLevel(auth_db.login("admin","pass")[0]))