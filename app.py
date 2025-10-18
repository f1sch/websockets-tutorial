#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK

# coroutine that manages a connection
async def handler(websocket):
    async for message in websocket:
        print(message)

# coroutine that calls serve() to start a websocket server
async def main():
    # async with ensures correct termination of the program by the server
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()

if __name__ == "__main__":
    # entry point
    asyncio.run(main())