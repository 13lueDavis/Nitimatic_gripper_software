import serial
import time
import sys
import glob

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

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

    ##========== GET ==========##

    def getGripperWidth(self):
        self.arduino.flushInput()
        self.arduino.write('W\r'.encode())
        while not self.arduino.readline():
            pass
        width = (self.arduino.readline().decode())
        if width:
            width = float(width)
            return width
        else: return -1

    def getRawGripperWidth(self):
        self.arduino.flushInput()
        self.arduino.write('w\r'.encode())
        while not self.arduino.readline():
            pass
        width = (self.arduino.readline().decode())
        if width:
            width = float(width)
            return width
        else: return -1

    def getGripperHealth(self):
        self.arduino.flushInput()
        self.arduino.write('H\r'.encode())
        while not self.arduino.readline():
            pass
        health = (self.arduino.readline().decode())
        if health:
            return int(health)
        else: return -1

    def getSMAResistance(self):
        self.arduino.flushInput()
        self.arduino.write('R\r'.encode())
        while not self.arduino.readline():
            pass
        resistance = (self.arduino.readline().decode())
        if resistance:
            resistance = float(resistance)
            return resistance
        else: return -1

    def getSMACurrent(self):
        self.arduino.flushInput()
        self.arduino.write('I\r'.encode())
        while not self.arduino.readline():
            pass
        current = (self.arduino.readline().decode())
        if current:
            current = float(current)
            return current
        else: return -1

    def getSMAVoltage(self):
        self.arduino.flushInput()
        self.arduino.write('V\r'.encode())
        while not self.arduino.readline():
            pass
        voltage = (self.arduino.readline().decode())
        if voltage:
            voltage = float(voltage)
            return voltage
        else: return -1

    def getTime(self):
        self.arduino.flushInput()
        self.arduino.write('t\r'.encode())
        while not self.arduino.readline():
            pass
        processorTime = (self.arduino.readline().decode())
        if processorTime:
            processorTime = float(processorTime)
            return processorTime
        else: return -1

    ##========== SET ==========##

    def closeGripper(self):
        self.arduino.flushInput()
        self.arduino.write('c\r'.encode())
        while not self.arduino.readline():
            pass
        return bool(int(self.arduino.readline().decode()[0]))

    def openGripper(self):
        self.arduino.flushInput()
        self.arduino.write('o\r'.encode())
        while not self.arduino.readline():
            pass
        return bool(int(self.arduino.readline().decode()[0]))

    def setFanSpeed(self, speedPer):
        self.arduino.flushInput()
        self.arduino.write('f{}\r'.format(speedPer).encode())
        while not self.arduino.readline():
            pass
        return True

    def setSMACurrent(self, current):
        # Amps
        self.arduino.flushInput()
        self.arduino.write('i{}\r'.format(int(current*1000)).encode())
        while not self.arduino.readline():
            pass
        current = (self.arduino.readline().decode())
        if current:
            return True
        else: return False


    ##========== OTHER ==========##

    def calibrate(self):
        while True:
            print('Input current gripper width [mm]:')
            in1 = raw_input()
            try:
                mmDist1 = float(in1)
                vDist1 = float(self.getRawGripperWidth())
                break;
            except:
                print('Invalid input - Input actual distance in mm')
        while True:
            print('Input (new) current gripper width [mm]:')
            in2 = raw_input()
            try:
                mmDist2 = float(in2)
                vDist2 = float(self.getRawGripperWidth())
                break;
            except:
                print('Invalid input - Input actual distance in mm')

        m = (mmDist2 - mmDist1)/(vDist2 - vDist1)
        b = mmDist1 - m*vDist1

        print("Distance [mm] = {}*Volts + {}".format(m,b))

        self.arduino.flushInput()
        self.arduino.write('m{}\r'.format(int(m*1000)).encode())
        while not self.arduino.readline():
            pass
        success = (self.arduino.readline().decode()[:-2])

        self.arduino.flushInput()
        self.arduino.write('b{}\r'.format(int(b*1000)).encode())
        while not self.arduino.readline():
            pass
        success = (self.arduino.readline().decode()[:-2])
