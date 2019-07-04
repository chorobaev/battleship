class ShipException(Exception):

    def __init__(self, msg, errors):
        super(ShipException, self).__init__(msg)

        self.errors = errors
