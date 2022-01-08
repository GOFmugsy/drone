import time
import board
import pwmio
from adafruit_motorkit import MotorKit
import busio
import adafruit_bno055
from PID_CPY import PID
import math

step = 0.1
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
while True:
    euler = sensor.euler
    pitchpid = PID(1, 0.1, 0.05, setpoint=0)
    rollpid = PID(1, 0.1, 0.05, setpoint=0)
    throttle = 50 / 100# should be pid to distance sensor eventually
    # print("yaw: {}".format(euler[0]))
    # print("roll: {}".format(euler[1]))
    # print("pitch: {}".format(euler[2]))
    kit = MotorKit()
    prop1 = pitchpid(euler[2] / 90)
    prop2 = pitchpid(euler[2] / 90)
    prop3 = pitchpid(euler[2] / 90)
    prop4 = pitchpid(euler[2] / 90)
    kit.motor1.throttle = 0
    kit.motor2.throttle = -0.0
    kit.motor3.throttle = -0.0
    kit.motor4.throttle = 0.0
    # kit.motor1.throttle = prop1 if math.fabs(prop1) > throttle else throttle
    # kit.motor2.throttle = prop2 if math.fabs(prop2) > throttle else throttle
    # kit.motor3.throttle = prop3 if math.fabs(prop3) > throttle else throttle
    # kit.motor4.throttle = prop4 if math.fabs(prop4) > throttle else throttle
    # kit.motor1.throttle = throttle
    # kit.motor2.throttle = -1 * throttle
    # kit.motor3.throttle = -1 * throttle
    # kit.motor4.throttle = throttle 
    time.sleep(step)

