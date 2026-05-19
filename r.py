from models.saving import saving_account
import bcrypt
from utils.auth import login_handle

# saving_account(1,"Shahnawaz Ali","Saving Account",1234845789,1000,"Shahnawaz")

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )

p = hash_password("password")
print(p)
q = verify_password("password",p)
print(q)

x = login_handle("shahnawaz")
print(x[0])