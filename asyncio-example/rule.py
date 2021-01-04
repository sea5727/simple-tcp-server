import asyncio

async def g():
    # TODO Pause here and come back to g() when f() is ready
    # TODO 여기서 멈추고 f가 준비되면 돌아와라 
    r = await f()
    return r