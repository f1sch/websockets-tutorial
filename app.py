#!/usr/bin/env python
import asyncio
import itertools
import json
import secrets

from websockets.asyncio.server import serve
from connect4 import PLAYER1, PLAYER2, Connect4

JOIN = {}

async def start(websocket):
    # Initialize a Connect Four game, the set of WebSocket connections
    # receiving moves from this game, and secret access token.
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access token to the browser of the first player,
        # where it'll be used for building a "join" link.
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))

        # Temporary - for testing:
        print("first player started the game", id(game))
        async for message in websocket:
            print("first player sent", message)
    
    finally:
        del JOIN[join_key]


async def handler(websocket):
    # Receive and parse the "init" event from the UI
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    # First player starts a new game
    await start(websocket)

# coroutine that manages a connection
async def handlerOLD(websocket):
    # Initialize a Connect Four game, the set of websocket connections
    # receiving moves from this game, and secret access token.
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected



    # Players take alternate turns, using the same browser
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        try:
            # Play the move
            row = game.play(player, column)
        except ValueError as exc:
            # Send an "error" event if the move was illegal
            event = {
                "type": "error",
                "message": str(exc), 
            }
            await websocket.send(json.dumps(event))
            continue

        # Send a "play" event to update the UI
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))

        # If move is winning, send a "win" event
        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
            await websocket.send(json.dumps(event))
        
        # Alternate turns.
        player = next(turns)
        

# coroutine that calls serve() to start a websocket server
async def main():
    # async with ensures correct termination of the program by the server
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()

if __name__ == "__main__":
    # entry point
    asyncio.run(main())