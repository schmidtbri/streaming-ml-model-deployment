import asyncio


# from here: https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code
def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
