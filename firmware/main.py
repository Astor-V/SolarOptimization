from machine import I2C, Pin
from ina219 import INA219
import utime

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=50000)

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS, i2c)
ina.configure()

LOG_INTERVAL_S = 60
LOG_FILE = "power_log.txt"

try:
    with open(LOG_FILE, "r"):
        pass
except OSError:
    with open(LOG_FILE, "w") as f:
        f.write("timestamp_s,voltage_V,current_mA,power_mW\n")

print("Starting power log. Interval: {}s".format(LOG_INTERVAL_S))

while True:
    try:
        v = ina.voltage()
        i = ina.current()
        p = ina.power()

        timestamp = utime.time()
        line = "{},{:.4f},{:.4f},{:.4f}\n".format(timestamp, v, i, p)

        with open(LOG_FILE, "a") as f:
            f.write(line)

        print(line.strip())

    except Exception as e:
        print("Read error:", e)

    utime.sleep(LOG_INTERVAL_S)