import time
import board
import pwmio
from adafruit_motorkit import MotorKit
import busio
import adafruit_bno055
from PID_CPY import PID

step = 0.1
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
while True:
    euler = sensor.euler
    pitchpid = PID(1, 0.1, 0.05, setpoint=0)
    rollpid = PID(1, 0.1, 0.05, setpoint=0)
    throttle = 80 # should be pid to distance sensor eventually
    # print("yaw: {}".format(euler[0]))
    # print("roll: {}".format(euler[1]))
    # print("pitch: {}".format(euler[2]))
    kit = MotorKit()
    # kit.motor1.throttle = pitchpid(euler[2] / 90)
    kit.motor1.throttle = 0
    kit.motor2.throttle = -0.0
    kit.motor3.throttle = -0.0
    kit.motor4.throttle = 0.0
    time.sleep(step)

