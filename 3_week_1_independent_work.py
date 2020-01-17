class FileReader:
    """
    Class for read file to str and print
    """
    def __init__(self, path_to_file=None):
        self._path_to_file = path_to_file

    def read(self):
        try:
            with open(self._path_to_file, "r") as f:
                return f.read()
        except FileNotFoundError as e:
            print(e)
            return ""
