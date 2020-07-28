import serial
import serial.tools.list_ports
import time
import send_email
import Pomiar
import os
import datetime

# variables
file_name = 'Data_ws.txt'

# port
ports = serial.tools.list_ports.comports()
port = ports[0]
port = port.device

ser = serial.Serial(port, 9600)


# command Raspberry <- arduino
def serial_read_command():
    global ser
    x = ser.readline()
    x = x.decode()
    x = x.rstrip()
    return x


# get data arduino -> Raspberry
def get_data_serial():
    line = ser.readline()
    line = line.decode()
    line = line.rstrip()
    line_data = [float(x) for x in line.split()]
    pomiar = Pomiar.Pomiar(line_data)
    return pomiar


# write to txt file actual data
def write_to_file(x):
    with open(file_name, 'a+') as f:
        f.write((str(datetime.datetime.now(). strftime("%Y-%m-%d %H:%M:%S"))+'\n'))
        f.close()
    for i in range(len(x)):
        line = []
        line.append(int(x[i].name))
        line.append(x[i].temp)
        line.append(x[i].presure)
        line.append(x[i].humidity)
        line.append(x[i].batVoltage)
        line.append(x[i].RSSI)

        with open(file_name, 'a+') as f:
            #print ("Sensor ID = {}\nTemperature = {}\nPresure = {}\nHumidity = {}\nAltitiude = {}\n".format(line[0],line[1],line[2],line[3],line[4]))
            f.write(("Sensor ID = {}\nTemperature = {} *C\nPresure = {} hPa\nHumidity = {} %\Batery Voltage = {} bD\nRSSI = {} V\n".format(
                line[0], line[1], line[2], line[3], line[4], line[5])))
            f.close()


def main_core():
    ser.readline()
    while True:
        pomiars = []
        pomiars.append(get_data_serial())
        pomiars.append(get_data_serial())
        write_to_file(pomiars)
        send_email.send(file_name)
        os.remove(file_name)
        time.sleep(1)


main_core()