class Value:

    def __init__(self, commission):
        self.commission = commission
        self.value = None

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, value):
        self.value = value * (1.0 - self.commission)


class Account:

    def __init__(self, commission):
        Account.amount = Value(commission)
        self.commission = commission


if __name__ == '__main__':
    _ = Account(0.3)
    _.amount = 150
    print(_.amount)
    # pass

