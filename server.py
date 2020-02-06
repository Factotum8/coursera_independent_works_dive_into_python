import asyncio


class ClientServerProtocol(asyncio.Protocol):

    error_message = b"error\nwrong command\n\n"
    correct_complete_message = b"ok\n\n"
    _storage = {}  # {'key.val': {'1580908123': '123'}}

    def __init__(self):
        self.transport = None
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        print(f"Connect {exc} close")

    def data_received(self, data):
        resp = self.process_data(data)
        self.transport.write(resp)

    def _key_values_dump(self, key):

        def key_dump(k):
            salt = f"\n{k}"
            return f"{salt}{salt.join(f' {val} {stamp}' for stamp, val in self._storage[k].items())}"

        if key == '*':
            # ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n
            return f"ok{''.join(key_dump(k) for k in self._storage)}\n\n"
        elif key in self._storage:
            # ok\npalm.cpu 2.0 1150864248\npalm.cpu 0.5 1150864248\n\n
            return f"ok{key_dump(key)}\n\n"
        else:
            return f"ok\n\n"

    def process_data(self, data: bytes) -> bytes:
        try:
            data = data.decode("utf-8")
            v = data.strip('\n').split(' ')
            if v[0] == 'get':
                key = v[1]
                if len(v) != 2:
                    raise ValueError(f"Command from client isn't correct: {data}")

                if key == '*':
                    return self._key_values_dump(key).encode('utf-8')
                elif key in self._storage:
                    return self._key_values_dump(key).encode('utf-8')

                else:
                    return self.correct_complete_message

            elif v[0] == 'put':
                if len(v) != 4:
                    raise ValueError(f"Command from client isn't correct: {data}")
                key, val, stamp = v[1:]
                val = float(val)
                stamp = int(stamp)
                if key in self._storage:
                    self._storage[key][stamp] = val
                else:
                    self._storage[key] = {stamp: val}

                return self.correct_complete_message
            else:
                raise ValueError(f"Command from client isn't correct: {data}")

        except Exception as e:
            print(f"Can't process command from client, error: {e}: data: {data}")
            return self.error_message


def run_server(host, port):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
