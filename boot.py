# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from supervisor import runtime
import storage

usbConnected=runtime.usb_connected

# If the D0 is connected to ground with a wire
# CircuitPython can write to the drive
#storage.remount("/", usbConnected)
