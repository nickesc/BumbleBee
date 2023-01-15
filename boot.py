# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from supervisor import runtime
import storage

# If USB is not connected CircuitPython can write to the drive
usbConnected=runtime.usb_connected
storage.remount("/", readonly=usbConnected)
