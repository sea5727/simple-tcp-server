
import sys
import asyncio
import time

async def example():
    ret = 0
    for i in range(1, 10, 1):
        await asyncio.sleep(0.1)
        ret += 1
    return ret

async def main():
    t1 = asyncio.create_task(example())
    t2 = asyncio.create_task(example())
    print(await t1 + await t2)


if __name__ == '__main__':
    asyncio.run(main())


