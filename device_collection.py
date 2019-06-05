from typing import Callable, Dict, List, Optional
from network_device import NetworkDevice


class DeviceCollection:
    """A collection of `NetworkDevice`s.
    This collection will notify listeners of changes to `NetworkDevice`s present in the collection.
    """

    __devices: Dict[str, NetworkDevice] = dict()
    __on_update: List[Callable[[str], None]] = list()


    def get_devices(self) -> List[NetworkDevice]:
        """Returns all devices in this collection.

        Returns:
            List[NetworkDevice]: [description]
        """
        return self.__devices.values()


    def get_device(self, mac_address: str) -> Optional[NetworkDevice]:
        """Returns a specific device from this collection by MAC address.
        If no matching device exists, returns None.

        Args:
            mac_address (str): The MAC address to search for.

        Returns:
            Optional[NetworkDevice]: A NetworkDevice with matching MAC address, or None.
        """
        return self.__devices.get(mac_address, None)


    def update_device(self, device: NetworkDevice):
        """Adds a new NetworkDevice to this collection, or updates an existing NetworkDevice.

        Args:
            device (NetworkDevice): The NetworkDevice to add or update.
        """
        # If the NetworkDevice already exists, update it.
        if device.mac_address in self.__devices:
            self.__devices[device.mac_address].signal_strength = device.signal_strength
        # If the NetworkDevice is new, add it and assign an event listener.
        else:
            self.__devices[device.mac_address] = device
            device.on_signal_strength_changed(self.__device_changed_handler)
            self.__device_changed_handler(device)


    def on_update(self, callback: Callable[[NetworkDevice], None]):
        """Assign a callback to handle when this collection changes.

        Args:
            callback (Callable[[NetworkDevice], None]): The callback function.
        """
        self.__on_update.append(callback)


    def __device_changed_handler(self, device: NetworkDevice, _: Optional[int]=None):
        """Notifies any listeners that a NetworkDevice has been added or updated.

        Args:
            device (NetworkDevice): The NetworkDevice which was updated.
            _ (Optional[int]): The previous signal strength
        """
        for callback in self.__on_update:
            callback(device)
