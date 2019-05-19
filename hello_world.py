"""Set monitor."""
import asyncio

import pyrcrack


WIFI_NAME = 'wlan0'


async def set_monitor():
    """Scan for targets, return json."""
    async with pyrcrack.AirmonNg() as airmon:
        try:
            interfaces = await airmon.list_wifis()
            print(interfaces)
            interface = await airmon.set_monitor(WIFI_NAME)
            print(interface[0])
            foo = await airmon.run('start', WIFI_NAME)
            print(foo)

        finally:
            await airmon.run('stop', WIFI_NAME)

        


asyncio.run(set_monitor())