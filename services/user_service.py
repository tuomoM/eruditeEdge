from repositories.user_repository import UserRepository
from repositories.user_repository import user_repository as default_user_repository


class UserService:
    def __init__(self,user_repository:UserRepository = default_user_repository )-> None:
        self._user_repository = user_repository

    def register(self, username: str, password:str, password2:str)-> str:
        if password != password2:
            return "passwords are not identical"
        if self._user_repository.user_exists:
            return "Username already exists, choose another username"
        if len(password) < 6:
            return "Password must be atleast 6 characters"
        if len(username) < 4:
            return "Username must be atleast 4 characters"
        self._user_repository.create_user(username,password)
        return ""
    
    def login(self,username: str,password: str):
        result = self._user_repository.login_check()
        if result:
            return result

