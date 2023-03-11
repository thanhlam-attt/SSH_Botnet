from pexpect import pxssh


class Client:
    def __init__(self, host, user, passwd, por):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.por = por
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.passwd, self.por)
            return s
        except Exception:
            print('[-] Error Connecting')
            exit()

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before
