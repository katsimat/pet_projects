import asyncio
from threading import Thread

from src.local_game.local_game import local_game

if __name__ == '__main__':
    l_g = local_game()
    async_thread = Thread(target=asyncio.run, args=(l_g.start_async(),))
    async_thread.start()

    l_g.start()
