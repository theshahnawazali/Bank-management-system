# Global Exception error

class UsernameAlreadyExists(Exception):
    pass

class EmailAlreadyExists(Exception):
    pass

class UsernameNotExists(Exception):
    pass

class EmailNotExists(Exception):
    pass

class TokenSetUnsuccesfull(Exception):
    pass

class RedisConnectionError(Exception):
    pass

class IncorrectPassword(Exception):
    pass

class BankAccountAlreadyExist(Exception):
    pass

class NegativeBalance(Exception):
    pass

class BankAccountNotExists(Exception):
    pass

class AccountNotActive(Exception):
    pass

class WithdrawalLimit(Exception):
    pass

class InsufficientBalance(Exception):
    pass

class TemporaryLock(Exception):
    pass