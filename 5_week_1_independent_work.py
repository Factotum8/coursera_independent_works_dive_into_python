import time
import json
import socket


class Client:

    answer_pattern = "ok\n\n"

    def __init__(self, host, port, timeout=None):
        self._host = host
        self._port = int(port)
        self._timeout = timeout

    def put(self, key, value, timestamp=None):
        try:
            # response = req.post(url=f"{self._host}:{self._port}",
            #                     data=f"put {key} {value} {timestamp or int(time.time())}\n",
            #                     timeout=self._timeout)
            #
            # if response.status_code != 200 or response.text != self.answer_pattern:
            #     raise ClientError(f"Response status not 200 OK, server answer: {response.text}")

            with socket.create_connection((self._host, self._port)) as sock:
                # put palm.cpu 23.7 1150864247\n
                sock.sendall(f"put {key} {value} {timestamp or int(time.time())}\n".encode("utf8"))
                sock.settimeout(self._timeout)

                response = ""
                try:
                    while True:
                        data = sock.recv(1024)
                        response = f'{response}{data.decode("utf8")}'
                except socket.timeout:
                    pass

                if response != self.answer_pattern:
                    raise ClientError(f"Server answer: {response}")

        except ClientError:
            raise
        except Exception as e:
            raise ClientError("Can't send data to server") from e

    @staticmethod
    def loads(s):
        return {metric: [(int(stamp), float(val)) for stamp, val in metric].sort() for metric in json.loads(s)}

    def get(self, key='*'):
        try:
            # response = req.post(url=f"{self._host}:{self._port}",
            #                     data=f"get {key}\n",
            #                     timeout=self._timeout)
            #
            # if response.text == self.answer_pattern:
            #     return {}
            # else:
            #     return self.loads(response.text)

            with socket.create_connection((self._host, self._port)) as sock:
                sock.sendall(f"get {key}".encode("utf8"))
                sock.settimeout(self._timeout)

                response = ""

                try:
                    while True:
                        data = sock.recv(1024)
                        response = f'{response}{data.decode("utf8")}'
                except socket.timeout:
                    pass

                if response == self.answer_pattern:
                    return {}
                else:
                    return self.loads(response)

        except Exception as e:
            raise ClientError(f"Can't get data from server") from e


class ClientError(Exception):
    pass


if __name__ == '__main__':
    pass
