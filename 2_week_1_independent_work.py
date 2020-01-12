import os
import json
import tempfile
import argparse


def main(key, value):
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    if not os.path.exists(storage_path):
        os.system(f"touch {storage_path}")

    if key is not None and value is not None:

        # dict_ = None

        with open(storage_path, 'r') as f:
            dict_ = json.load(f) if os.stat(storage_path).st_size else {}

            if key in dict_:
                dict_[key].append(value)
            else:
                dict_[key] = [value]

        with open(storage_path, 'w') as f:
            json.dump(dict_, f)

    elif key is not None:
        with open(storage_path, 'r') as f:
            dict_ = json.load(f) if os.stat(storage_path).st_size else {}
            print(*dict_.get(key, ''), sep=', ')
    else:
        print('Syntax error')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--key", action='store', type=str, dest='key_name',
                            help="TODO")
    arg_parser.add_argument("--val", action='store', type=str, dest='value_name',
                            help="TODO")
    args = arg_parser.parse_args()
    key_name = args.key_name
    value_name = args.value_name

    main(key_name, value_name)
