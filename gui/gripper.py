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

class SerialCommunication():
    arduino = serial.Serial('COM1', 115200, timeout=.1)

    def getGripperWidth():
        arduino.write('W')
        while True:
            data = arduino.readline()
            if data:
                print(data)
                break
            
    def getGripperHealth():
        arduino.write('H')
        while True:
            data = arduino.readline()
            if data:
                print(data)
                break
            
    def getSMAResistance():
        arduino.write('R')
        while True:
            data = arduino.readline()
            if data:
                print(data)
                break
            
    def getSMACurrent():
        arduino.write('I')
        while True:
            data = arduino.readline()
            if data:
                print(data)
                break
            
    def closeGripper():
        arduino.write('C')
        while True:
            data = arduino.readline()
            if data:
                print(data)
                break

    def openGripper():
        arduino.write('O')
        while True:
            data = arduino.readline()
            if data:
                print(data)
                break
            
