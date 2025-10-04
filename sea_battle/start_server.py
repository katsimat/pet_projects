import asyncio

from src.constants import HOST, PORT
from src.server.server import Server


async def main():
    server = Server()
    await server.start(HOST, PORT)


if __name__ == '__main__':
    asyncio.run(main())
