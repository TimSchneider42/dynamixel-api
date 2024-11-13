"""
MIT License

Copyright (c) 2021 Tim Schneider

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

from rhp12rn import RHP12RN, RHP12RNAConnector

with RHP12RNAConnector(device="/dev/ttyUSB0", baud_rate=57600, dynamixel_id=1) as connector:
    rhp12rn = RHP12RN(connector)

    # Make sure torque is disabled before writing EEPROM values
    rhp12rn.torque_enabled = False
    rhp12rn.position_limit_high = 660

    rhp12rn.torque_enabled = True
    print("Enabled motor.")

    print("Opening gripper...")
    rhp12rn.goal_position_rel = 0.0
    while rhp12rn.current_position_rel > 0.01:
        time.sleep(0.1)
        print("\rCurrent position: {}".format(rhp12rn.current_position_rel), end="")
    print("\rCurrent position: {}".format(rhp12rn.current_position_rel))
    print("Gripper fully opened.")

    time.sleep(1.0)

    print("Closing gripper...")
    rhp12rn.goal_position_rel = 1.0
    while rhp12rn.current_position_rel < 0.99:
        time.sleep(0.1)
        print("\rCurrent position: {}".format(rhp12rn.current_position_rel), end="")
    print("\rCurrent position: {}".format(rhp12rn.current_position_rel))
    print("Gripper fully closed.")

    rhp12rn.torque_enabled = False
    print("Disabled motor.")
