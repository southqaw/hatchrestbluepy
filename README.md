# Hatch Rest Python Library
This library allows an original [Hatch Rest](https://www.hatch.co/rest) to be controlled via BLE. This library uses the [bluepy](https://github.com/IanHarvey/bluepy) library as a backend, and therefore only runs on Linux. This library is primarily intended to be run on Raspberry Pi devices.
## Installation
```
pip install hatchrestbluepy
```
If you intend to use this library without elevated privileges, you will need to find `bluepy-helper` and run the following command to enable BLE access.
```
sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper
```
## Example

## Credits
This library is heavily based on the [pyhatchbabyrest](https://github.com/kjoconnor/pyhatchbabyrest) library, written by [@kjoconnor](https://github.com/kjoconnor).
