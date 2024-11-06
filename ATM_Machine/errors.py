class ATMError(Exception):
    """
    Base exception for ATM Machine.
    """

    pass


class AccountNotFoundError(ATMError):
    """
    Raises when account does not exist in the database.
    """

    pass


class AccountAlreadyExistsError(ATMError):
    """
    Raises when creating an already existing account.
    """

    pass


class ExitedError(ATMError):
    """
    Raises when user exited the ATM Machine.
    """

    pass
