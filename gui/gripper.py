import serial
import time

# class Gripper():
#     def __init__(self):
#         # self.arduino = serial.Serial('COM1', 115200, timeout=.1)
#         return
#
#     def getGripperWidth(self):
#         return 85.5
#
#     def getGripperHealth(self):
#         return "Adequate"
#
#     def getSMAResistance(self):
#         return 31.5
#
#     def getSMACurrent(self):
#         return 0.0
#
#     def closeGripper(self):
#         return
#
#     def openGripper(self):
#
#         return


arduino = serial.Serial('COM1', 115200, timeout=.1)

def openGripper():
    arduino.write('>')
    while True:
        data = arduino.readline()
        if data:
            print(data)
            break
