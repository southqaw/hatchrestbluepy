import bluepy.btle as btle
import time
from .constants import MAC_PREFIX, SERV_TX, SERV_FEEDBACK, HatchRestSound
from typing import List


class ScanDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass
        # if isNewDev:
        #     print("Discovered device {}".format(dev.addr))
        # elif isNewData:
        #     print("Received new data from {}".format(dev.addr))


class HatchRest(object):
    """ A syncronous interface to a Hatch Rest using bluepy. """

    def __init__(self, addr: str = None):
        """ Start the interface

        :param addr: The address tp connect to.
        """
        self.peripheral = btle.Peripheral()
        self.addr = addr
        if addr is None:
            devices = self._scan(10.0)
            for device in devices:
                if device.addr[:8] == MAC_PREFIX:
                    self.addr = device.addr
        self.connect()

    def connect(self):
        self.peripheral.connect(self.addr, addrType=btle.ADDR_TYPE_RANDOM)

        tx_service = self.peripheral.getServiceByUUID(SERV_TX)
        feedback_service = self.peripheral.getServiceByUUID(SERV_FEEDBACK)

        self.tx_char = tx_service.getCharacteristics()[0]
        self.feedback_char = feedback_service.getCharacteristics()[0]

        self._refresh_data()

    def _scan(self, timeout: float) -> List[btle.ScanEntry]:
        """
        Get a list of BLE devices in range of the host.
        """
        scanner = btle.Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(timeout)
        return devices

    def _send_command(self, command: str) -> None:
        """ Send a command to the device.

        :param command: The command to send.
        """
        self.tx_char.write(bytearray(command, "utf-8"))
        time.sleep(0.5)
        self._refresh_data()
        self._refresh_data()

    def _refresh_data(self) -> None:
        """ Request updated data from the device and set the local attributes. """
        response = [hex(x) for x in list(self.feedback_char.read())]

        # Make sure the data is where we think it is
        assert response[5] == "0x43"  # color
        assert response[10] == "0x53"  # audio
        assert response[13] == "0x50"  # power

        red, green, blue, brightness = [int(x, 16) for x in response[6:10]]

        sound = HatchRestSound(int(response[11], 16))

        volume = int(response[12], 16)

        power = not bool(int("11000000", 2) & int(response[14], 16))

        self.color = (red, green, blue)
        self.brightness = brightness
        self.sound = sound
        self.volume = volume
        self.power = power

    def power_on(self):
        command = "SI{:02x}".format(1)
        self._send_command(command)

    def power_off(self):
        command = "SI{:02x}".format(0)
        self._send_command(command)

    def set_sound(self, sound):
        command = "SN{:02x}".format(sound)
        self._send_command(command)

    def set_volume(self, volume):
        command = "SV{:02x}".format(volume)
        self._send_command(command)

    def set_color(self, red: int, green: int, blue: int):
        self._refresh_data()

        command = "SC{:02x}{:02x}{:02x}{:02x}".format(red, green, blue, self.brightness)
        self._send_command(command)

    def set_brightness(self, brightness: int):
        self._refresh_data()

        command = "SC{:02x}{:02x}{:02x}{:02x}".format(
            self.color[0], self.color[1], self.color[2], brightness
        )
        self._send_command(command)

    def set_light(self, red: int, green: int, blue: int, brightness: int):
        command = "SC{:02x}{:02x}{:02x}{:02x}".format(red, green, blue, brightness)
        self._send_command(command)

    def disconnect(self) -> None:
        self.peripheral.disconnect()

    @property
    def connected(self):
        conn = False
        try:
            if self.peripheral.getState() == 'conn':
                conn = True
        except btle.BTLEInternalError:
            conn = False
        return conn
