#!/usr/bin/env python
import asyncio
import json

from websockets.asyncio.server import serve
from connect4 import PLAYER1, PLAYER2

# coroutine that manages a connection
async def handler(websocket):
    for player, column, row in [
        (PLAYER1, 3, 0),
        (PLAYER2, 3, 1),
        (PLAYER1, 4, 0),
        (PLAYER2, 4, 1),
        (PLAYER1, 2, 0),
        (PLAYER2, 1, 0),
        (PLAYER1, 5, 0),
    ]:
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))
        await asyncio.sleep(0.5)
    event = {
        "type": "win",
        "player": PLAYER1,
    }
    await websocket.send(json.dumps(event))
    #async for message in websocket:
    #    print(message)

# coroutine that calls serve() to start a websocket server
async def main():
    # async with ensures correct termination of the program by the server
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()

if __name__ == "__main__":
    # entry point
    asyncio.run(main())