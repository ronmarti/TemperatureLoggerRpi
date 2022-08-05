# TemperatureLoggerRpi
Temperature logger running periodically on Raspberry Pi.
Only a basic script with limited deployment functions.

## Deployment Method
Currently, just upload the content of the folder to RPi to the location `~/pi/TemperatureLogger` and don't forget to add the `.secrets` folder with all the secrets, otherwise, the logger won't be able to connect to the databases.

## Rasperry on LAN
Node name is `raspberry`, hostname `raspberrypi`, username `pi`, password - you know...