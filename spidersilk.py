from shutil import which
from subprocess import Popen, run, PIPE, STDOUT
from PyQt5.QtWidgets import QApplication
from non_blocking_stream_reader import NonBlockingStreamReader
from device_collection import DeviceCollection
from stream_parser import parse
from spidersilk_window import SpiderSilkWindow


AIRMON_NAME = 'airmon-ng'
AIRODUMP_NAME = 'airodump-ng'


class SpiderSilk:
    """The application entry point.
    """

    __test_mode: bool
    __airmon_terminal: Popen
    __airmon_reader: NonBlockingStreamReader
    __devices: DeviceCollection


    def __init__(self, test_mode=True):
        """Initialises an instance of `SpiderSilk`.

        Args:
            test_mode (bool, optional): Indicates whether this app is running in test mode. Defaults to False.
        """
        self.__devices = DeviceCollection()
        self.__test_mode = test_mode
        if not self.__test_mode:
            # kill anything which will interfere with WiFi
            run([AIRMON_NAME, 'check', 'kill'])
            # begin airmon
            run([AIRMON_NAME, 'start', 'wlan0'])
            self.__airmon_process = Popen([AIRODUMP_NAME, 'wlan0mon'], stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
            self.__airmon_reader = NonBlockingStreamReader(self.__airmon_process)


    def __del__(self):
        """Releases resources used by this instance of `SpiderSilk`.
        """
        if not self.__test_mode:
            # turn off airmon output
            if self.__airmon_process:
                self.__airmon_process.terminate()
            # restore original WiFi settings
            run([AIRMON_NAME, 'stop', 'wlan0mon'])
            run(['service', 'NetworkManager', 'restart'])


    def execute(self):
        proceed = True
        qt = QApplication(list())
        ssw = SpiderSilkWindow(self.__devices)
        qt.processEvents()

        while proceed:
            proceed = ssw.isVisible()
            output = self.__airmon_reader.readline()
            device = parse(output)
            if device is not None:
                self.__devices.update_device(device)
                qt.processEvents()
            



if "__main__" == __name__:

    HAS_AIRMON = which(AIRMON_NAME) is not None
    HAS_AIRODUMP = which(AIRODUMP_NAME) is not None

    if  not HAS_AIRMON:
        print(f"Unable to find {AIRMON_NAME}.")

    if  not HAS_AIRODUMP:
        print(f"Unable to find {AIRODUMP_NAME}.")

    # Test mode should be used if the system lacks the correct applications.
    USE_TEST_MODE = not (HAS_AIRMON and HAS_AIRODUMP)

    if USE_TEST_MODE:
        print("Launching in test mode.\nConsider using Kali Linux next time!")

    try:
        app = SpiderSilk(USE_TEST_MODE)
        app.execute()
    finally:
        del app
