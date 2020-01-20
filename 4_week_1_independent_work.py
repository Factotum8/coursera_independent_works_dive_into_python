import os
import ntpath
import functools
import tempfile as tf


def call_counter(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


class File:

    def __init__(self, path_to_file):

        if not os.path.exists(path_to_file):
            os.mknod(path_to_file)

        self._path_to_file = path_to_file
        self.__next__calls = 0

    @property
    def path_to_file(self):
        return self._path_to_file

    def __add__(self, other):

        dir_ = tf.gettempdir()

        new_name = f"{os.path.splitext(ntpath.basename(self._path_to_file))[0]}" \
                   f"{os.path.splitext(ntpath.basename(other.path_to_file))[0]}"

        new_file = os.path.join(dir_, new_name)
        with open(self._path_to_file, 'r') as f1, open(other.path_to_file, 'r') as f2, open(new_file, 'w') as f3:
            f3.write(f"{f1.read()}{f2.read()}")

        return File(new_file)

    def read(self):
        with open(self._path_to_file, 'r') as f:
            return f.read()

    def write(self, str_):
        with open(self._path_to_file, 'w') as f:
            try:
                f.write(str_)
            except Exception:
                return 1
            else:
                return 0

    def __iter__(self):
        return self

    @call_counter
    def __next__(self):

        with open(self._path_to_file) as f:

            for i, str_ in enumerate(f):
                if i < self.__next__calls:
                    continue
                self.__next__calls += 1
                return str_

            self.__next__calls = 0
            raise StopIteration

    def __repr__(self):
        return f"{self._path_to_file}"


if __name__ == '__main__':
    a = File('1') + File('2')
    for _ in a:
        print(_)
