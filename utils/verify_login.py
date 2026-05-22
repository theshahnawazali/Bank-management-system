from utils.auth import load_user,get_user_token, get_user_name,get_user_username


def verify_login_session():

    cookie_user = load_user()

    if not cookie_user:
        return None
    
    if len(cookie_user) < 2:
        return None
    
    user_id = cookie_user[1]
    cookie_token = cookie_user[0]

    token_data = get_user_token(user_id)

    if not token_data:
        return None
    
    db_token = token_data[0]

    if cookie_token != db_token:
        return None

    return {
        "name": get_user_name(user_id),
        "username": get_user_username(user_id)
    }
