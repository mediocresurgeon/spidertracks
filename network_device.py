from typing import Callable, List, Optional, Tuple
from oui_dictionary import OuiDictionary


class NetworkDevice:
    """A physical device which has WiFi capabilities, such as a smartphone.
    """

    __mac_address: Tuple[str, str, str, str, str, str, str, str] = None
    __mfr_name: str = None
    __signal_strength: Optional[int] = None
    __on_signal_strength_changed = list()


    def __init__(self, mac_address: str):
        """Create a new instance of `NetworkDevice`.

        Args:
            mac_address (str): This device's MAC address.
        """
        self.__mac_address = NetworkDevice.parse_mac_address(mac_address)
        self.__mfr_name = OuiDictionary.get_mfr_name((self.__mac_address[0], self.__mac_address[1], self.__mac_address[2]))


    @staticmethod
    def parse_mac_address(mac_address: str) -> Tuple[str, str, str, str, str, str, str, str]:
        """Parses a string into a MAC address (hex format).

        Args:
            mac_address (str): The MAC address to parse.

        Raises:
            TypeError: Raised if the mac address is not a string.
            ValueError: Raised if the mac address is not in hex format.

        Returns:
            Tuple[str, str, str, str, str, str, str, str]: The MAC address in standard hex format
        """
        if not isinstance(mac_address, str):
            raise TypeError("mac_address is not a string: " + str(mac_address))
        temp: str = mac_address.strip().upper()

        char_list: List[str] = []
        if ":" in temp:
            char_list = temp.split(":")
        elif "-" in temp:
            char_list = temp.split("-")
        else:
            raise ValueError("mac_address contains invalid characters.")

        if 6 == len(char_list):
            return tuple(char_list)
        raise ValueError("mac_address does not contain the correct number of octets.")


    @property
    def mac_address(self) -> str:
        """Gets this `NetworkDevice`'s MAC address.

        Returns:
            str: The MAC address in hex format.
        """
        return ":".join(self.__mac_address)


    @property
    def mfr_name(self) -> str:
        """Gets the name of the manufacturer which built this `NetworkDevice`.

        Returns:
            str: The name of the manufacturer.
        """
        return self.__mfr_name


    @property
    def signal_strength(self) -> Optional[int]:
        """Returns the signal strength of this `NetworkDevice`.

        Returns:
            Optional[int]: The signal strength.
        """
        return self.__signal_strength


    @signal_strength.setter
    def signal_strength(self, strength: Optional[int]):
        """Sets the signal_strength value.
        If this changes the value, this will trigger any callbacks
        set by the on_signal_strength_changed() method.

        Args:
            strength (Optional[int]): The new signal strength.
        """
        if self.__signal_strength != strength:
            original_strength = self.__signal_strength
            self.__signal_strength = strength
            for callback in self.__on_signal_strength_changed:
                callback(self, original_strength)


    def on_signal_strength_changed(self, callback: Callable[[object, Optional[int]], None]):
        """Event handler for when the signal_strength value changes.

        Args:
            callback (Callable[[Optional[int], Optional[int]], None]): The function to call when the signal_strength changes. Second argument is the old value is the old signal strength.
        """
        self.__on_signal_strength_changed.append(callback)


if "__main__" == __name__:
    ios_mac = "80:ED:2C:D3:6C:C4"
    iPhone = NetworkDevice(ios_mac)
    assert iPhone.mac_address, "80:ED:2C:D3:6C:C4"
    assert iPhone.mfr_name, "Apple"

    android_mac = "08-C5-E1-D3-6C-C4"
    samsung = NetworkDevice(android_mac)
    assert samsung.mac_address, "08:C5:E1:D3:6C:C4"
    assert samsung.mfr_name, "Samsung Electro-Mechanics(Thailand)"
