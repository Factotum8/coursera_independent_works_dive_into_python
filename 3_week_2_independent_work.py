import os
import csv


class CarBase:

    _car_type = None
    _allowed_extensions_file = ['.jpg', '.png', '.gif', '.jpeg']

    car_type = property()
    carrying = property()
    photo_file_name = property()

    def __init__(self, brand, photo_file_name, carrying, init_str=None):

        if not brand or not photo_file_name or not carrying:
            raise ValueError("Required parameters is empty", brand, photo_file_name, carrying)

        extension = os.path.splitext(photo_file_name)[1]
        if extension not in self._allowed_extensions_file:
            raise ValueError("Extension file image not allowed", photo_file_name)

        self._brand = brand
        self._photo_file_name = photo_file_name
        self._carrying = float(carrying)
        self._init_str = init_str

    @property
    def brand(self):
        return self._brand

    @photo_file_name.setter
    def photo_file_name(self, path):
        extension = os.path.splitext(path)[1]
        if extension in self._allowed_extensions_file:
            self._photo_file_name = path
        else:
            print("Value error: not correct value for path to photo")

    @photo_file_name.getter
    def photo_file_name(self):
        return self._photo_file_name

    @photo_file_name.deleter
    def photo_file_name(self):
        del self._photo_file_name

    @carrying.setter
    def carrying(self, val):
        val = float(val)
        if val < 0.0:
            self._carrying = val

    @carrying.getter
    def carrying(self):
        return self._carrying

    @carrying.deleter
    def carrying(self):
        del self._carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self._photo_file_name)[1]

    def __repr__(self):
        return str(self._init_str)


class Car(CarBase):

    _car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count, init_str=None):
        super().__init__(brand, photo_file_name, carrying, init_str=init_str)
        try:
            if '.' in passenger_seats_count or ',' in passenger_seats_count:
                raise ValueError(f"Passenger seats count isn't: ", passenger_seats_count)
            self._passenger_seats_count = int(passenger_seats_count)
        except ValueError as e:
            raise RuntimeError from e

    passenger_seats_count = property()
    car_type = property()

    @car_type.getter
    def car_type(self):
        return self._car_type

    @passenger_seats_count.setter
    def passenger_seats_count(self, val):
        try:
            self._passenger_seats_count = int(val)
        except ValueError:
            print("Can't set value for passenger seats count")

    @passenger_seats_count.getter
    def passenger_seats_count(self):
        return self._passenger_seats_count

    def __repr__(self):
        return f"{self._car_type}:{self._carrying}:{self._photo_file_name}:{self._brand}:{self._passenger_seats_count}"


class Truck(CarBase):

    _car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl, init_str=None):
        super().__init__(brand, photo_file_name, carrying, init_str)
        try:
            self._body_length, self._body_width, self._body_height = [float(b) for b in body_whl.split('x')]
        except ValueError:
            self._body_length, self._body_width, self._body_height = .0, .0, .0

    body_width = property()
    body_height = property()
    body_length = property()
    car_type = property()

    @car_type.getter
    def car_type(self):
        return self._car_type

    @body_length.setter
    def body_length(self, val):
        try:
            len_ = float(val)

            if len_ >= 0.0:
                self._body_length = len_
            else:
                self._body_length = 0.0

        except ValueError:
            self._body_length = 0.0

    @body_length.getter
    def body_length(self):
        return self._body_length

    @body_height.setter
    def body_height(self, val):
        try:
            height = float(val)

            if height >= 0.0:
                self._body_height = height
            else:
                self._body_height = 0.0

        except ValueError:
            self._body_height = 0.0

    @body_height.getter
    def body_height(self):
        return self._body_height

    @body_width.setter
    def body_width(self, val):
        try:
            width = float(val)

            if width >= 0.0:
                self._body_width = width
            else:
                self._body_width = 0.0

        except ValueError:
            self._body_width = 0.0

    @body_width.getter
    def body_width(self):
        return self._body_width

    def get_body_volume(self):
        return self._body_height * self._body_length * self._body_width


class SpecMachine(CarBase):

    _car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra=None, init_str=None):
        super().__init__(brand, photo_file_name, carrying, init_str)
        if not extra:
            raise ValueError("Field extra is empty")
        self.extra = extra

    car_type = property()

    @car_type.getter
    def car_type(self):
        return self._car_type


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        header = next(reader)
        for list_ in reader:
            curr_attrs = dict(zip(header, list_))
            try:
                if curr_attrs['car_type'] == 'car':
                    for attr in ['body_whl', 'extra']:
                        if curr_attrs[attr] not in (None, ''):
                            raise ValueError(f"Attr: {attr}", attr)
                    car = Car(curr_attrs['brand'], curr_attrs['photo_file_name'],
                              curr_attrs['carrying'], curr_attrs['passenger_seats_count'], init_str=list_)

                elif curr_attrs['car_type'] == 'spec_machine':
                    for attr in ['passenger_seats_count', 'body_whl']:
                        if curr_attrs[attr] not in (None, ''):
                            raise ValueError(f"Attr: {attr}", attr)

                    car = SpecMachine(curr_attrs['brand'], curr_attrs['photo_file_name'], curr_attrs['carrying'],
                                      curr_attrs['extra'], init_str=list_)

                elif curr_attrs['car_type'] == 'truck':
                    for attr in ['passenger_seats_count', 'extra']:
                        if curr_attrs[attr] not in (None, ''):
                            raise ValueError(f"Attr: {attr}", attr)

                    car = Truck(curr_attrs['brand'], curr_attrs['photo_file_name'],
                                curr_attrs['carrying'], curr_attrs['body_whl'], init_str=list_)
                else:
                    continue

                car_list.append(car)

            except Exception as e:
                print(f"Error: {e} for line: {curr_attrs}")

    return car_list


if __name__ == '__main__':
    print(get_car_list('./tttt.csv'))
