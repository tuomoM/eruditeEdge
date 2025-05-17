from werkzeug.security import check_password_hash, generate_password_hash
import db

class UserRepository:
    def user_exists(self, username:str) -> bool:
        sql = "select id from users where username = ? "
        result = db.query(sql, [username])
        return bool(result)
    
    def create_user(self,username:str,password:str):
        passwordhash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql,[username, passwordhash])

    def login_check(self,username: str, password: str):
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        if not result:
          return None
        user_id = result[0]["id"]
        password_hash = result[0]["password_hash"]
        if check_password_hash(password_hash, password):
          return user_id
        else:
          return None
            
    def get_user(self,user_id):
      sql = "SELECT id, username FROM users WHERE id = ?"
      result = db.query(sql, [user_id])
      return result[0] if result else None
        
user_repository = UserRepository()