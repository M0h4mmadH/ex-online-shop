class TooManyItemsException(Exception):
    pass


class EmptyCartException(Exception):
    pass


class UserCartAddressCityDoesNotMatch(Exception):
    def __init__(self,  message='', **kwargs):
        super().__init__(message)
        self.kwargs = kwargs
