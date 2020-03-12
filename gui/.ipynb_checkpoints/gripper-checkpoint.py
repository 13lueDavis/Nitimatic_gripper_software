import serial
import time
from .open_coms import serial_ports

class Gripper:
    def __init__(self, port=None):
        if port is None:
            ports = serial_ports()
            port = [port for port in ports if 'serial' in port][0]
        print('Opening connection on port: {}'.format(port))

        self.arduino = serial.Serial(port, 9600, timeout=.1)
        self.arduino.close()
        self.arduino.open()
        self.arduino.write('\r'.encode())
        self.arduino.readline().decode()

    def getGripperWidth(self):
        self.arduino.flushInput()
        self.arduino.write('W\r'.encode())
        width = (self.arduino.readline().decode()[:-2])
        if width:
            width = int(width)/1000
            return width
        else: return -1

    def getGripperHealth(self):
        self.arduino.flushInput()
        self.arduino.write('H\r'.encode())
        health = (self.arduino.readline().decode()[:-2])
        if health:
            return int(health)
        else: return -1

    def getSMAResistance(self):
        self.arduino.flushInput()
        self.arduino.write('R\r'.encode())
        resistance = (self.arduino.readline().decode()[:-2])
        if resistance:
            resistance = int(resistance)/1000
            return resistance
        else: return -1

    def getSMACurrent(self):
        self.arduino.flushInput()
        self.arduino.write('I\r'.encode())
        current = (self.arduino.readline().decode()[:-2])
        if current:
            current = int(current)/1000
            return current
        else: return current
    
    def getSMAVoltage(self):
        self.arduino.flushInput()
        self.arduino.write('V\r'.encode())
        voltage = (self.arduino.readline().decode()[:-2])
        if voltage:
            voltage = int(voltage)/1000
            return voltage
        else: return -1

    def closeGripper(self):
        self.arduino.flushInput()
        self.arduino.write('c\r'.encode())
        return bool(int(self.arduino.readline().decode()[0]))

    def openGripper(self):
        self.arduino.flushInput()
        self.arduino.write('o\r'.encode())
        return bool(int(self.arduino.readline().decode()[0]))

    def setFanSpeed(self, speedPer):
        self.arduino.flushInput()
        self.arduino.write('f{}\r'.format(speedPer).encode())
        return True
    
    def setSMACurrent(self, current):
        # Amps
        self.arduino.flushInput()
        self.arduino.write('i{}\r'.format(int(current*1000)).encode())
        current = (self.arduino.readline().decode()[:-2])
        if current:
            return True
        else: return False