import asyncio
import random
import aioredis
import requests
import json
import pathlib
import aiohttp

q = asyncio.Queue()
CONSUMERS_NUM = 5
DOWNLOAD_DIR = f'{pathlib.Path(__file__).parent.absolute()}/media/books'
# print(DOWNLOAD_DIR)

async def download_to_file(url, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            contents = await response.read()
            with open(f'{DOWNLOAD_DIR}/{file_name}', 'wb') as tf:
                tf.write(contents)
            return file_name

# async def fake_redis_pub():
#     redis = await aioredis.create_redis_pool('redis://redis')
#     await redis.publish('channel:download_request', 'Hello')
#     redis.close()
#     await redis.wait_closed()

async def producer():
    redis = await aioredis.create_redis_pool('redis://redis')
    ch1, = await redis.subscribe('channel:download_request')
    assert isinstance(ch1, aioredis.Channel)

    async def reader(channel):
        async for message in channel.iter():
            print("Got message:", message)
            await q.put(message)

    asyncio.get_running_loop().create_task(reader(ch1))
    # while True:
        # continue

async def consumer(num):
    while True:
        value = await q.get()
        print('Consumed', num, value)
        request_dict = json.loads(value)
        await download_to_file(request_dict['download_url'], request_dict['file_name'])



loop = asyncio.get_event_loop()

loop.create_task(producer())

for i in range(CONSUMERS_NUM):
    loop.create_task(consumer(i))

# loop.create_task(fake_redis_pub())

loop.run_forever()