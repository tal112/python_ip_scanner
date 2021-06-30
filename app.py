import eel
import os
import threading


connected_machines = []

def pinger(ip_address, lock):

    result = os.popen("ping {0} -n 1".format(ip_address)).read()

    if "TTL" in result:
        with lock:
            print(ip_address)
            connected_machines.append(ip_address)


def get_local_ip_address():
    ip_address = "I.P. Address Not Found"
    ipcon = os.popen("ipconfig")

    for line in ipcon.readlines():
        if "IPv4 Address. . . . . . . . . . ." in line:
            line_split = line.split(":")
            ip_address = line_split[1]
            ip_address = ip_address[:-1]

    ip_address = ip_address.replace(" ", "")


    ip_template = ".".join(ip_address.split('.')[0:-1]) + '.'
    return ip_template

@eel.expose
def scan_network():
    connected_machines.clear()

    ip_template = get_local_ip_address()

    threads = []

    lock = threading.Lock()

    for i in range(254):
        ip_address = ip_template + str(i)
        t = threading.Thread(target=pinger, args=(ip_address, lock))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    return connected_machines


eel.init('web')
eel.start('index.html', size=(850,400), port=0)   #python will select free ephemeral ports.
