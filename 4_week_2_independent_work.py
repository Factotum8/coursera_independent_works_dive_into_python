class Value:

    def __init__(self):
        self.value = None

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, value):
        self.value = value - value * obj.commission


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    a = Account(0.9)
    a.amount = 150
    print(a.amount)

