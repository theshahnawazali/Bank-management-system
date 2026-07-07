from utils.auth import (
    get_user_id,
    delete_sessions,
    login_user,
    session_login
)
from utils.token import generate_session_token


def update_login_info(username):
    # Generate Random Sessions token
    token = generate_session_token()

    # Get User chat id from data base
    user_id = get_user_id(username)

    # Delete previous sessions from database
    delete_sessions(user_id[0])

    # Save token in browser
    login_user(user_id[0],token)

    # Save token in Database
    session_login(
        user_id[0],
        token
        )