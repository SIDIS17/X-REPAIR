# ESP32 + ADXL345

Câblage I2C typique :

| ADXL345 | ESP32 |
|---|---|
| VCC | 3.3 V |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

Le firmware transmet `ax,ay,az` sur le port série à 230400 bauds.
