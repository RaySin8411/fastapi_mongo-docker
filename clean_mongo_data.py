import time
import asyncio
from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:80/building/') as resp:
            data = await resp.json()
            data = data['data']
        tasks = [asyncio.create_task(delete(item["_id"], session)) for item in data]
        await asyncio.gather(*tasks)
        async with session.get('http://127.0.0.1:80/building/') as resp:
            data = await resp.json()
            data = data['data']

    print(data)


async def delete(_id, session):
    async with session.delete(f'http://127.0.0.1:80/building/{_id}'):
        print('ok')


if __name__ == '__main__':
    start_time = time.time()  # 開始執行時間

    loop = asyncio.get_event_loop()  # 建立事件迴圈(Event Loop)
    loop.run_until_complete(main())  # 執行協程(coroutine)
    print("花費:" + str(time.time() - start_time) + "秒")
