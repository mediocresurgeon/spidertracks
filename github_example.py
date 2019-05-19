import pyrcrack
import sys
import asyncio
from contextlib import suppress
from async_timeout import timeout


async def test(max_timeout):
    async with pyrcrack.AirodumpNg() as pdump:
        with suppress(asyncio.TimeoutError):
            async with timeout(max_timeout):
                #print(sys.argv)
                await pdump.run(sys.argv[0])
                while True:
                    await asyncio.sleep(1)
                    print(pdump.meta)
        return await pdump.proc.terminate()


asyncio.run(test(10))