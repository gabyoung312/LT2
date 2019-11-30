import database as db

def login(username, password):
    is_valid_login = False
    user = None
    temp_user = db.get_user(username)
    if temp_user:
        if temp_user["password"] == password:
            is_valid_login = True
            user = {
                "username": username,
                "first_name": temp_user["first_name"],
                "last_name": temp_user["last_name"],
                "password": temp_user["password"]
            }

    return is_valid_login, user