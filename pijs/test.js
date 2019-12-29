// https://www.npmjs.com/package/i2c-bus

// https://www.holtek.com/documents/10179/116711/HT16K33v120.pdf

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

bus.writeI2cBlockSync(0x70,0,10,data)
