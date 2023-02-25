import os
from functools import reduce


def ip_to_int(ip):
    return reduce(lambda x, y: x + int(y[1]) * 2 ** (8 * y[0]), enumerate(reversed(ip.split('.'))), 0)


def display(data):
    result = []
    for ip, mac in data:
        result.append('\t{:>35}{:>20}'.format(ip, mac))
    return '\n'.join(result)


def scan():
    with os.popen("sudo ifconfig") as fp:
        ifc_data = fp.read().split('\n\n')

    data = []
    for connection in ifc_data:
        connection_data = connection.split()
        if not len(connection_data):
            continue
        name = connection_data[0]
        if name == 'lo:':
            continue
        try:
            ip = connection_data[connection_data.index('inet') + 1]
        except ValueError:
            ip = 'None'
        try:
            mac = connection_data[connection_data.index('ether') + 1]
        except ValueError:
            mac = 'None'
        try:
            netmask = connection_data[connection_data.index('netmask') + 1]
        except ValueError:
            netmask = 'None'
        data.append((name, ip, mac, netmask))

    for connection in data:
        name, ip, mac, netmask = connection
        req = f"{ip}/{ip_to_int(netmask).bit_count()}"
        with os.popen(f"sudo nmap -sn {req}") as fp:
            nmap_data = fp.read().split('\n')
        nmap_ip4 = [line.split()[4] for line in nmap_data if line.startswith("Nmap scan")]
        nmap_ip4.remove(ip)
        nmap_mac = [line.split()[2] for line in nmap_data if line.startswith("MAC")]
        print("{:<15}\n\t{:<15}{:>20}\n\t{:<15}{:>20}\n\t{:<15}{:>20}".format(name,
                                                                             'Home IP:', ip,
                                                                             'Home MAC:', mac,
                                                                             'Netmask:', netmask))
        print("\tConnected Devices: {:>16}{:>20}\n {}\n".format('IP', 'MAC', display(zip(nmap_ip4, nmap_mac))))


if __name__ == "__main__":
    scan()
    