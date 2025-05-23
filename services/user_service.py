from repositories.user_repository import UserRepository
from repositories.user_repository import user_repository as default_user_repository
from werkzeug.security import check_password_hash, generate_password_hash

class UserService:
    def __init__(self,user_repository:UserRepository = default_user_repository )-> None:
        self._user_repository = user_repository

    def register(self, username: str, password:str, password2:str)-> str:
        if password != password2:
            return "passwords are not identical"
        if self._user_repository.user_exists(username):
            return "Username already exists, choose another username"
        if len(password) < 6:
            return "Password must be atleast 6 characters"
        if len(username) < 4:
            return "Username must be atleast 4 characters"
        password_hash = generate_password_hash(password)
        return self._user_repository.create_user(username,password_hash)
        
    
    def login(self,username: str,password: str):
        result = self._user_repository.login_get(username, password)
        if result:
            user_id = result[0]["id"]
            password_hash = result[0]["password_hash"]
            if check_password_hash(password_hash,password):
                return user_id
            


user_service = UserService()