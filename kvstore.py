#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import asyncio

class KvStore(object):
    def __init__(self):
        self.store = {}
    def set(self, key, value):
        self.store[key] = value
        return '+OK'
    def get(self, key):
        if key in self.store.keys():
            return self.store[key]
        else:
            return '-ERROR'
    def truncate(self, key):
        if key in self.store.keys():
            del self.store[key]
            return '+OK'
        else:
            return '-ERROR'

class KvStringParser(object):
    def __init__(self):
        self.data = []
        self.OP = ''
        self.KEY = ''
        self.VALUE = ''
    def parse(self, string):
        self.data = string.split(' ')
        self.OP = self.data[0]
        self.KEY = self.data[1].strip()
        if self.OP == 'GET':
            return 1, [ self.KEY ]
        elif self.OP == 'SET':
            self.VALUE = ' '.join(self.data[2:]).strip()
            return 2, [ self.KEY, self.VALUE ]
        elif self.OP == 'TRUNCATE':
            return 3, [self.KEY]
        else:
            return -1, []

class KvHandler(object):
    def __init__(self, store, parser):
        self.store = store
        self.parser = parser

    async def handler(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        op_type, query = self.parser.parse(message)
        print(op_type, query, self.store)
        if op_type == -1:
            data = '-ERROR'
        elif op_type == 3:
            data = self.store.truncate(query[0])
        elif op_type == 2:
            data = self.store.set(query[0], query[1])
        elif op_type == 1:
            data = self.store.get(query[0])
        else:
            data = '-GENERIC ERROR'
        addr = writer.get_extra_info('peername')

        print(f"Recieved {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(data.encode())
        await writer.drain()

        print("Close the connection")
        writer.close()


async def main(port):
    store = KvStore()
    parser = KvStringParser()
    handler = KvHandler(store, parser)
    server = await asyncio.start_server(
            lambda r, w: handler.handler(r, w), '127.0.0.1', port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if len(sys.argv) == 2:
    asyncio.run(main(sys.argv[1]))
else:
    print(f"Usage : python {sys.argv[0]} <PORT_NUMBER>")
