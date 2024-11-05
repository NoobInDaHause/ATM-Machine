class ATMError(Exception):
    """
    Base exception for ATM Machine.
    """
    pass

class AccountNotFoundError(ATMError):
    pass
