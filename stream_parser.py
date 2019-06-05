from typing import Optional
from network_device import NetworkDevice


def parse(line: str) -> Optional[NetworkDevice]:
    """Parses airmon-ng lines into NetworkDevice objects.
    """
    try:
        str_chunks = line.split()
        device = NetworkDevice(str_chunks[0])
        sig = int(str_chunks[1])
        device.signal_strength = sig
        return device
    except:
        return None