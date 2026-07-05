from enum import Enum as PyEnum


class AccountType(str, PyEnum):
    SAVING = "Saving"
    CURRENT = "Current"


class TransactionType(str, PyEnum):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"
    TRANSFER = "Transfer"

class UserRole(str, PyEnum):
    CUSTOMER = "Customer"
    ADMIN = "Admin"

class AccountStatus(str, PyEnum):
    ACTIVE = "Active"
    CLOSED = "Closed"
    INACTIVE = "Inactive"
    FROZEN = "Frozen"


class TransactionStatus(str, PyEnum):
    SUCCESS = "Success"
    FAILED = "Failed"


class SessionStatus(str, PyEnum):
    ACTIVE = "Active"
    DEACTIVE = "Deactive"