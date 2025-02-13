# dynamixel-api


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/TimSchneider42/dynamixel-api">
    <img src="https://raw.githubusercontent.com/TimSchneider42/dynamixel-api/master/docs/python_dynamixel_api_logo.png" alt="dynamixel_api" height="170">
  </a>

  <h3 align="center">Python API for Dynamixel Motors</h3>

  <p align="center">
    Elevate your robotics projects with dynamixel-api -- a powerful and user-friendly Python wrapper for the Dynamixel SDK libary, designed to effortlessly control various Dynamixel motors.
    <br />
    <a href="https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/"><strong>Explore Dynamixel SDK »</strong></a>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ol>
        <li>
          <a href="#prerequisites">Prerequisites</a>
        </li>
        <li>
          <a href="#hardware-setup">Hardware Setup</a>
        </li>
        <li>
          <a href="#installation">Installation</a>
        </li>
      </ol>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ol>
        <li>
            <a href="#control-the-dynamixel-motor">Control the Dynamixel Motor</a>
        </li>
        <li>
            <a href="#custom-motor-support">Custom Motor Support</a>
        </li>
      </ol>
    </li>
    <li>
      <a href="#contribution">Contribution</a>
    </li>
    <li>
        <a href="#license">License</a>
    </li>
  </ol>
</details>


<!-- INTRODUCTION -->
## Introduction
`dynamixel-api` is a Python wrapper for the [Dynamixel SDK library](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/), designed to control various Dynamixel motors. This library provides a high-level API that simplifies motor control through a `DynamixelConnector` class, which establishes and manages serial connections, and a `Motor` class that offers direct access to frequently used control parameters. Users can read and write motor control fields easily, enabling quick setup for common robotic manipulation tasks. The library's modular design can accommodate multiple types of Dynamixel motors, making it versatile for various robotics applications.


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
Make sure you have a working Python 3 installation. If not, follow the instructions on the <a href="https://www.python.org/downloads/">Python 3 download page</a>.

### Hardware Setup
To use the `dynamixel-api` library, you need to have a Dynamixel motor and the appropriate hardware to connect it to your computer. The motors are controlled via a <a href="https://emanual.robotis.com/docs/en/parts/interface/u2d2_power_hub/">U2D2 Power Hub Board</a>, which connects to the motor with a 4-pin JST EH cable. The U2D2 Power Hub Board is connected to a computer via a USB cable, allowing the user to send commands to the motor using the Dynamixel SDK library.

### Installation
To install the `dynamixel-api` library, simply run the following command:
```sh
pip3 install dynamixel-api
```

or clone the repository and install the package locally:
```sh
git clone https://github.com/TimSchneider42/dynamixel-api.git
pip3 install ./dynamixel-api
```

## Usage
The `dynamixel-api` library provides out-of-the-box support for the following hardware:
- [ROBOTIS RH-P12-RN and RH-P12-RN(A) Grippers](https://emanual.robotis.com/docs/en/platform/rh_p12_rn/): These are advanced robotic grippers powered by Dynamixel motors.
- [DYNAMIXEL XL430-W250-T Motor](https://emanual.robotis.com/docs/en/dxl/x/xl430-w250/): The motor used to control the [actuated-UMI gripper](https://github.com/actuated-umi/actuated-umi-gripper).

### Control the Dynamixel Motor

First, create a `Connector` instance of your motor and call the `connect()` function to establish a serial connection to the motor. For example, to connect to an XL430-W250-T motor:

```python
from dynamixel_api import XL430W250TConnector

connector = XL430W250TConnector(device="/dev/ttyUSB0", baud_rate=57600, dynamixel_id=1)
connector.connect()
...
connector.disconnect()
```

`Connector` instances can also be used as context managers:

```python
with XL430W250TConnector(device="/dev/ttyUSB0", baud_rate=57600, dynamixel_id=1) as connector:
    ...
```

The `connector` object allows reading and writing of arbitrary addresses of the motor's control table:

```python
print(connector.read_field("torque_enable"))
connector.write_field("torque_enable", 1)
print(connector.read_field("torque_enable"))
```

For a comprehensive list of its entries, refer to the [docs of your motor](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/).
Alternatively for this example, all entries are listed in [`dynamixel_api/models/xl430w250t.py`](dynamixel_api/models/xl430w250t.py).
Note that the motors have to be disabled (`"torque_enabled"` has to be set to 0) for EEPROM values to be written, while RAM values can be written at any time.

For convenience, the `Motor` class provides direct access to the most commonly used fields:

```python
import time
from dynamixel_api import Motor

motor = Motor(connector)
motor.torque_enabled = True
motor.goal_position = 1.0
time.sleep(3.0)
motor.torque_enabled = False
```

For a full example of the usage of this package, refer to [`example/xl430w250t_open_close.py`](example/xl430w250t_open_close.py).

### Custom Motor Support
To use a custom motor, define its control table (EEPROM and RAM Fields) and implement a `Connector` class based on the motor's documentation. Refer to the [`dynamixel_api/models`](dynamixel_api/models) folder for examples and templates.

After defining the `Connector` class, you can use the Motor class to control the motor as shown above. If you want to have additional control over the motor, you can create a child class of the `Motor` class and add custom methods.

### Finding the correct baud rate and Dynamixel ID
If the baud rate and/or Dynamixel ID is unknown, the `find_grippers`(dynamixel_api/sweep.py) method can be used to find those parameters by performing a full sweep. It can be invoked as follows from the command line after installing the package:

```sh
dynamixel-sweep
```

You can pass following arguments to the command:
- `--device`: The device path to the serial port (default: /dev/ttyUSB0)
- `--baud-rate`: The baud rate to use for the sweep (default: 9_600 57_600 115_200 1_000_000 2_000_000 3_000_000 4_000_000 4_500_000 10_500_000)


<!-- CONTRIBUTION -->
## Contribution
We welcome contributions to this repository. If you would like to contribute, please <a href="https://github.com/TimSchneider42/dynamixel-api/fork">fork</a> this repository and submit a <a href="https://github.com/TimSchneider42/dynamixel-api/compare">pull request</a> with your changes.


<!-- LICENDE -->
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
