#bash
read -p 'which tty port do you want to use? typically 0 or 1: ' ttyport
echo "using: " ttyUSB$ttyport " according to user input"
echo 1 | sudo tee /sys/bus/usb-serial/devices/ttyUSB$ttyport/latency_timer
