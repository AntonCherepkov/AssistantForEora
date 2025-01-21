from loader import *
from utils.setting_commands import set_commands
import asyncio
from handlers import routers


async def main():
    await set_commands(bot)
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(FileCheckMiddleware())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
