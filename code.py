import time
import board
import pwmio
from adafruit_motorkit import MotorKit
import busio
import adafruit_bno055
from PID_CPY import PID
import math
import neopixel

#step = 0.05
step = 0.0001
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)
throttle = 0.9 # should be pid to distance sensor eventually
kit = MotorKit()
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3
waitingLight = (255, 255, 51)
runningLight = (51, 255, 51)

def stopMotors(kit):
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0

# kit and target percent throttle
# 1  2
# 4  3
def throttleUp(kit, target):
    for i in range(target * 100):
        print("Throttle to " + str(i / 100) )
        kit.motor1.throttle = i / 100
        kit.motor2.throttle = i / 100
        kit.motor3.throttle = i / 100
        kit.motor4.throttle = i / 100
        time.sleep(0.2)

def throttleDown(kit, target):
    for i in reversed(range(target)):
        kit.motor1.throttle = i / 100
        kit.motor2.throttle = i / 100
        kit.motor3.throttle = i / 100
        kit.motor4.throttle = i / 100
        time.sleep(step)

# 1  2
# 4  3
def balanceTest(kit, sensor, target):
    euler = sensor.euler
    pitchpid = PID(1, 30, 0.1, setpoint=0.0222) # 5deg
    rollpid = PID(2, 30, 0.1, setpoint=0)
    throttlepid = PID(25, 0, 0.1, setpoint=target)
    # print("yaw: {}".format(euler[0]))
    # print("roll: {}".format(euler[1]))
    # print("pitch: {}".format(euler[2]))
    prop1 = target - pitchpid(euler[2] / 90) - rollpid(euler[1] / 90) 
    # prop1 = target - rollpid(euler[1] / 90) 
    # prop1 = target - pitchpid(euler[2] / 90) 
    # if euler[2] < 0:
        # prop1 = prop1 - pitchpid(euler[1] / 90)
    # prop1 = throttlepid(prop1)
    if prop1 > 1.0:
        prop1 = 1.0
    if prop1 < -1.0:
        prop1 = -1.0
    if prop1 < 0:
        prop1 = 0
    prop2 = target - pitchpid(euler[2] / 90) + rollpid(euler[1] / 90)
    # prop2 = target - pitchpid(euler[2] / 90)
    # prop2 = throttlepid(prop2)
    if prop2 > 1.0:
        prop2 = 1.0
    if prop2 < -1.0:
        prop2 = -1.0
    if prop2 < 0:
        prop2 = 0
    prop3 = target + pitchpid(euler[2] / 90) + rollpid(euler[1] / 90)
    # prop3 = target + pitchpid(euler[2] / 90)
    # prop3 = throttlepid(prop3)
    if prop3 > 1.0:
        prop3 = 1.0
    if prop3 < -1.0:
        prop3 = -1.0
    if prop3 < 0:
        prop3 = 0
    prop4 = target + pitchpid(euler[2] / 90) - rollpid(euler[1] / 90)
    # prop4 = target + pitchpid(euler[2] / 90)
    # prop4 = throttlepid(prop4)
    if prop4 > 1.0:
        prop4 = 1.0
    if prop4 < -1.0:
        prop4 = -1.0
    if prop4 < 0:
        prop4 = 0
    # print("p2: " + str(prop2) + " p1: " + str(prop1) + "\np3: " + str(prop3) + " p4: " + str(prop4))
    kit.motor1.throttle = prop1
    kit.motor2.throttle = prop2
    kit.motor3.throttle = prop3
    kit.motor4.throttle = prop4

print("Startup")
stopMotors(kit)

# print("Throttle up")
# throttleUp(kit, throttle)
# time.sleep(5)

# main program loop
pause = True
pauseDeBounce = 0 # steps
while True:
    # wait for test start
    euler = sensor.euler

    if pause:
        pixel.fill((255, 0, 0))
        stopMotors(kit)
        if euler[2] > 90 and pauseDeBounce == 0: # pitch down
            print("unPause")
            pause = False
            pauseDeBounce = 100
    else:
        pixel.fill((0, 255, 0))
        # begin hover test
        balanceTest(kit, sensor, throttle)
        if euler[2] > 90 and pauseDeBounce == 0:
            print("Pause")
            pause = True
            pauseDeBounce = 100
    
    if pauseDeBounce != 0:
        pauseDeBounce = pauseDeBounce - 1
        
    time.sleep(step)

