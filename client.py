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

            with socket.create_connection((self._host, self._port)) as sock:
                # put palm.cpu 23.7 1150864247\n
                sock.sendall(f"put {key} {value} {timestamp or int(time.time())}\n".encode("utf8"))
                sock.settimeout(self._timeout)

                response = ""
                try:
                    # response = sock.recv(4096).decode("utf8")
                    while True:
                        data = sock.recv(1024)

                        if not data:
                            break

                        response = f'{response}{data.decode("utf8")}'

                        if response[-2:] == '\n\n':
                            break

                except socket.timeout:
                    pass

                if response != self.answer_pattern:
                    raise ClientError(f"Server answer: {response}")

        except ClientError:
            raise
        except socket.error as e:
            raise ClientError("Can't send data to server") from e
        except Exception as e:
            raise ClientError("Client error") from e

    @staticmethod
    def loads(s):
        s = s.split('\n')[1:-2]
        s = [i.split(' ') for i in s]
        # [['palm.cpu', '10.5', '1501864247'], ['eardrum.cpu', '15.3', '1501864259']]
        d = {}
        for i in s:
            k, v, t = i
            if k in d:
                d[k].append((int(t), float(v)))
            else:
                d[k] = [(int(t), float(v))]

        return {k: sorted(v) for k, v in d.items()}

    def get(self, key='*'):
        try:

            with socket.create_connection((self._host, self._port)) as sock:
                sock.settimeout(self._timeout)
                sock.sendall(f"get {key}".encode("utf8"))

                response = ""

                try:
                    # response = sock.recv(4096).decode("utf8")

                    while True:
                        data = sock.recv(1024)

                        if not data:
                            break
                        response = f'{response}{data.decode("utf8")}'

                        if response[-2:] == '\n\n':
                            break

                except socket.timeout:
                    pass

                if response == self.answer_pattern:
                    return {}
                else:
                    return self.loads(response)

        except socket.error as e:
            raise ClientError(f"Socket error") from e
        except Exception as e:
            raise ClientError(f"Can't prepare data from server") from e


class ClientError(Exception):
    pass


if __name__ == '__main__':
    client = Client("127.0.0.1", 8888)
    print(client.get('*'))
    # print(client.put('k.ey', '123'))
