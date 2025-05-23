import db

class UserRepository:
    def user_exists(self, username:str) -> bool:
        sql = "select id from users where username = ? "
        result = db.query(sql, [username])
        return bool(result)
    
    def create_user(self,username:str,password:str):
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql,[username, password])
        return db.query("SELECT id from users WHERE username = ?", [username])
    
    def login_get(self,username: str, password: str):
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        if not result:
          return None
        return result
            
    def get_user(self,user_id):
      sql = "SELECT id, username FROM users WHERE id = ?"
      result = db.query(sql, [user_id])
      return result[0] if result else None
        
user_repository = UserRepository()