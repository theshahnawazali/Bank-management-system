import bcrypt

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


# passwrd = hash_password("Shahnawaz")
# print(passwrd)
# user = verify_password("Shahnawaz","$2b$12$QF.nbPPtBDl71Mpsd6HyVOZLzncLxycKu24Laau7DKkHqZ/xnWC8y")
# print(user)

email = "shahnawaz@gmail.com"
if email.find("@"):
    print("Find")
