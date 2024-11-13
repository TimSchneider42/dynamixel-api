from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dynamixel_gripper_control",
    version="1.0.0",
    description="Python controller for grippers powered by DYNAMIXEL motors.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TimSchneider42/dynamixel-gripper-control",
    author="Tim Schneider, Erik Helmut",
    author_email="schneider@ias.informatik.tu-darmstadt.de, erik.helmut1@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "dynamixel-sdk @ git+https://github.com/ROBOTIS-GIT/DynamixelSDK.git@c7e1eb71c911b87f7bdeda3c2c9e92276c2b4627#egg=dynamixel-sdk&subdirectory=python"
    ],

    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
)
