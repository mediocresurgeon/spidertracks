import sys
import typing
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from device_collection import DeviceCollection
from network_device import NetworkDevice


class SpiderSilkWindow(QWidget):


    __devices: DeviceCollection


    def __init__(self, devices: DeviceCollection):
        super().__init__()
        self.__devices = devices
        self.__initialise_ui()
        self.__devices.on_update(self.__on_devices_updated)


    def __initialise_ui(self):
        self.setWindowTitle("Nearby Wireless Devices")
        self.setGeometry(0, 0, 500, 1000)
        
        self.__tableWidget = QTableWidget()
        self.__rebuild_table()
        self.__tableWidget.move(0,0)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.__tableWidget)
        self.setLayout(self.layout)
        self.show()


    def __rebuild_table(self):
        devices = self.__devices.get_devices()

        row_count = 1 + len(devices)
        self.__tableWidget.setRowCount(row_count)
        self.__tableWidget.setColumnCount(3)

        # Column headers
        self.__tableWidget.setItem(0,0, QTableWidgetItem("MAC Address"))
        self.__tableWidget.setItem(0,1, QTableWidgetItem("Manufacturer"))
        self.__tableWidget.setItem(0,2, QTableWidgetItem("Signal Strength"))

        # Row data
        rowcount = 0
        for device in devices:
            rowcount += 1
            self.__tableWidget.setItem(rowcount,0, QTableWidgetItem(device.mac_address))
            self.__tableWidget.setItem(rowcount,1, QTableWidgetItem(device.mfr_name))
            self.__tableWidget.setItem(rowcount,2, QTableWidgetItem(f"{device.signal_strength}"))


    def __on_devices_updated(self, _: NetworkDevice):
        self.__rebuild_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mock_iphone = NetworkDevice("80:ED:2C:D3:6C:C4")
    mock_iphone.signal_strength = 10

    mock_android = NetworkDevice("08-C5-E1-D3-6C-C4")
    mock_android.signal_strength = 20

    mock_devices = DeviceCollection()
    mock_devices.update_device(mock_iphone)
    mock_devices.update_device(mock_android)

    ex = SpiderSilkWindow(mock_devices)

    mock_iphone2 = NetworkDevice("80:ED:2C:D3:6C:C4")
    mock_iphone2.signal_strength = 20
    mock_devices.update_device(mock_iphone2)
    app.processEvents()
    while True:
        continue
    #sys.exit(app.exec_())
