"""
MIT License

Copyright (c) 2024 Tim Schneider, Erik Helmut

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time

from dynamixel_api import Motor, XL430W250TConnector

with XL430W250TConnector(device="/dev/ttyUSB0", baud_rate=57600, dynamixel_id=1) as connector:
    gripper = Motor(connector)

    # Make sure torque is disabled before writing EEPROM values
    gripper.torque_enabled = False

    # Set operating mode to extended position control (no need to specify position limits)
    gripper.operating_mode = 4

    gripper.torque_enabled = True
    print("Enabled motor.")

    print("Closing gripper...")
    gripper.goal_position = -2380
    while gripper.current_position > gripper.goal_position + 20:
        time.sleep(0.1)
        print("\rCurrent position: {}".format(gripper.current_position), end="")
    print("\rCurrent position: {}".format(gripper.current_position))
    print("Gripper fully closed.")

    gripper.torque_enabled = False
    print("Disabled motor.")
