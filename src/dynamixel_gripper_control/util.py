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

from typing import Sequence, Tuple, List

from .dynamixel_connector import DynamixelConnector, Field, DynamixelConnectionError, DynamixelCommunicationError


BAUD_RATES = (9_600, 57_600, 115_200, 1_000_000, 2_000_000, 3_000_000, 4_000_000, 4_500_000, 10_500_000)


def find_grippers(device: str = "/dev/ttyUSB0", baud_rates: Sequence[int] = BAUD_RATES) -> List[Tuple[str, int, int]]:
    """
    Sweeps the specified baud rates and all possible dynamixel ids to find connected RH-P12-RN[(A)] grippers.
    :param device:      On which serial device to sweep.
    :param baud_rates:  Baud rates to test
    :return: List of tuples containing the model name, baud rate and Dynamixel id of each identified gripper.
    """
    found_devices = []
    for r in baud_rates:
        print("Testing baud rate {}...".format(r))
        for i in range(1, 254):
            try:
                with DynamixelConnector(
                        device=device, fields=[Field(0, "H", "model_number", "Model Number", False, 0)], baud_rate=r,
                        dynamixel_id=i) as connector:
                    model_number = connector.read_field("model_number")
                    if model_number in [35073, 35074]:
                        model_name = "RH-P12-RN" if model_number == 35073 else "RH-P12-RN(A)"
                        found_devices.append((model_name, r, i))
                        print("Found {} with ID {} at baud rate {}".format(model_name, i, r))
            except DynamixelCommunicationError:
                pass
    return found_devices