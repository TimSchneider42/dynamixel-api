from setuptools import setup

setup(
    name="dynamixel_api",
    version="0.0.1",
    packages=["dynamixel_api"],
    install_requires=[
        "pyserial>=3.5",
        "dynamixel-sdk @ git+https://github.com/ROBOTIS-GIT/DynamixelSDK.git@c7e1eb71c911b87f7bdeda3c2c9e92276c2b4627#subdirectory=python",
    ],
    entry_points={
            'console_scripts': [
                'find_grippers = dynamixel_api.util:find_grippers',
        ],
    },
)
