# mml-translate

This project involves the development of a translation tool for Megaman Legends (PC) to enable gameplay in different languages.

## How was this project created?

The `looking.py` script accesses the game's BIN folder and uses logic to test a theory:

- If character A has a value equal to 1, does character B have a value equal to 2?
- If character A has a value equal to 100, does character B have a value equal to 101?

It searches for a string and verifies whether this string exists in the BIN files by considering the positional differences between characters. The script also returns the hexadecimal value of each character.

### Example of Results

Character differences for 'looking': `[3, 0, -4, -2, 5, -7]`

The phrase 'looking' was found in the file: `C:\Users\vinic\Downloads\Megaman\DAT\ST00_02.BIN`

- Starting position of 'e' (hexadecimal): `0x31377`
- Hexadecimal values found: `['0x3a', '0x3d', '0x3d', '0x39', '0x37', '0x3c', '0x35']`

### Base Table

Using the results, the following table was generated:

```python
base_table = {
    0x01: '1', 0x02: '2', 0x03: '3', 0x04: '4', 0x05: '5', 0x06: '6', 0x07: '7',
    0x08: '8', 0x09: '9', 0x0A: ' ', 0x0B: ',', 0x0C: '0',  0x0E: '?',
    0x10: '.', 0x13: ':', 0x15: 'A', 0x16: 'B', 0x17: 'C', 0x18: 'D', 0x19: 'E',
    0x1A: 'F', 0x1B: 'G', 0x1C: 'H', 0x1D: 'I', 0x1E: 'J', 0x1F: 'K', 0x20: 'L',
    0x21: 'M', 0x22: 'N', 0x23: 'O', 0x24: 'P', 0x25: 'Q', 0x26: 'R', 0x27: 'S',
    0x28: 'T', 0x29: 'U', 0x2A: 'V', 0x2B: 'W', 0x2C: 'X', 0x2D: 'Y', 0x2E: 'Z',
    0x2F: 'a', 0x30: 'b', 0x31: 'c', 0x32: 'd', 0x33: 'e', 0x34: 'f', 0x35: 'g',
    0x36: 'h', 0x37: 'i', 0x38: 'j', 0x39: 'k', 0x3A: 'l', 0x3B: 'm', 0x3C: 'n',
    0x3D: 'o', 0x3E: 'p', 0x3F: 'q', 0x40: 'r', 0x41: 's', 0x42: 't', 0x43: 'u',
    0x44: 'v', 0x45: 'w', 0x46: 'x', 0x47: 'y', 0x48: 'z', 0x4D: "'", 0x82: "\n",
    0x50: "-", 0x4E: '"', 0x0D: "!"
}
```

### Translation Script

Based on this table, the `extract.py` script was developed. This script accesses the BIN files and attempts to translate hexadecimal values into text.
