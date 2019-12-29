# NodeJS on Raspberry Pi

This is a JS version of the clock.

## Install node on raspberry pi

https://www.w3schools.com/nodejs/nodejs_raspberrypi.asp

```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v

mkdir /home/pi/js
cd /hom/pi/js
```

## Install i2c-bus

https://www.npmjs.com/package/i2c-bus

```
npm install i2c-bus

# Run "sudo raspi-config" ... be sure I2C hardware is enabled 
```

## Talking to the display

https://www.holtek.com/documents/10179/116711/HT16K33v120.pdf

```js
const i2c = require('i2c-bus')

bus = i2c.openSync(1)

bus.sendByteSync(0x70,0x21) // 0010_000s Turn on the oscillator
bus.sendByteSync(0x70,0xEF) // 1110_pppp Set brightness to full
bus.sendByteSync(0x70,0x81) // 1000_xbbd Display on

// LED patterns
data = Buffer.from([
	0x5B,0, // '2'
	0x3F,0, // '0'
	02,0,   // Colon on
	0x06,0, // '1'
	0x6F,0  // '9'
]);

// Show "20:19" on the display
bus.writeI2cBlockSync(0x70,0,10,data)
```
