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

        self.buffer_string = ''

        self.arduino = serial.Serial(port, 9600, timeout=.1)
        self.arduino.close()
        self.arduino.open()
        self.arduino.write('\r'.encode())
        self.arduino.readline().decode()

    ##========== GET ==========##


    def receive(self):
        self.buffer_string = self.buffer_string + self.arduino.read(self.arduino.inWaiting()).decode()
        while '\n' not in self.buffer_string:
            self.buffer_string = self.buffer_string + self.arduino.read(self.arduino.inWaiting()).decode()

        lines = self.buffer_string.split('\n')
        last_received = lines[-2][:-2]
        self.buffer_string = lines[-1]

        return last_received


    def getSMACurrent(self):
        info = self.receive()
        current = float(info.split(',')[0])
        return current

    def getSMAVoltage(self):
        info = self.receive()
        voltage = float(info.split(',')[1])
        return voltage

    def getSMAResistance(self):
        info = self.receive()
        resistance = float(info.split(',')[2])
        return resistance

    def getGripperWidth(self):
        info = self.receive()
        width = float(info.split(',')[3])
        return width


    def getGripperHealth(self):
        info = self.receive()
        health = int(info.split(',')[4])
        return health

    def getTime(self):
        info = self.receive()
        time = int(info.split(',')[5])
        return time

    ##========== SET ==========##

    def closeGripper(self):
        self.arduino.flushInput()
        self.arduino.write('c\r'.encode())
        return True

    def openGripper(self):
        self.arduino.flushInput()
        self.arduino.write('o\r'.encode())
        return True

    def setFanSpeed(self, speedPer):
        self.arduino.flushInput()
        self.arduino.write('f{}\r'.format(speedPer).encode())
        return True

    def setSMACurrent(self, current):
        # Amps
        self.arduino.flushInput()
        self.arduino.write('i{}\r'.format(int(current*1000)).encode())
        return True


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
