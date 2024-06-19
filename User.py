class User:
    def __init__(self, user_id, username, email, password):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password
