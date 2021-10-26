import socket
import select
import time


globsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
globsocket.bind(("127.0.0.1", 28729))
globsocket.listen(5)

CHECK_NEW_CONN_INTERVAL = 0.05

dictal = {

}

conn_list = []


def getconn():
    read, w, e = select.select((globsocket, ), [], [], 0)
    for r in read:
        conn_list.append(Connection())


def sendmess(theme, mess):
    try:
        for c in dictal[theme]:
            c.send(mess, theme)
    except KeyError:
        pass


class Connection:
    def __init__(self):
        global globsocket
        globsocket.listen()
        self.conn, self.addr = globsocket.accept()
        self.fileno = self.conn.fileno

    def checksock(self):
        global dictal
        try:
            recved = self.conn.recv(1024).decode("ASCII", "ignore")
        except (ConnectionAbortedError, ConnectionResetError):
            conn_list.remove(self)
            return False
        if not recved:
            conn_list.remove(self)
            return False

        recved = recved.replace("<<START>>", "")
        messages = recved.split("<<END>>")

        for recv in messages:
            if not recv:
                continue
            try:
                if recv[:7] == "SETRECV":
                    if not recv[7:] in dictal:
                        dictal[recv[7:]] = [self]
                    else:
                        dictal[recv[7:]].append(self)
                    continue

                elif recv[:7] == "DELRECV":
                    if self in dictal[recv[7:]]:
                        dictal[recv[7:]].remove(self)
                    continue
            except IndexError:
                pass
            splittext = recv.split("<<||>>")
            sendmess(splittext[0], splittext[1])

    def loop(self):
        while self.checksock():
            pass

    def send(self, mess, tag):
        self.conn.sendall(f"<<START>>{tag}<<||>>{mess}<<END>>".encode("ASCII", "ignore"))


def checkforincoming():
    global conn_list
    if not conn_list:
        return
    readable, writeable, errored = select.select(conn_list, [], [], 0)
    for n in readable:
        n.checksock()
        print("R Object@", n)
    for n in writeable:
        print("W Object@", n)
    for n in errored:
        print("E Object@", n)


while True:
    time.sleep(CHECK_NEW_CONN_INTERVAL)
    checkforincoming()
    getconn()
    tagremove = []

    for tag in dictal:
        toremove = []
        for conn in dictal[tag]:
            if conn not in conn_list:
                toremove.append(conn)
        for conn in toremove:
            dictal[tag].remove(conn)
        if len(dictal[tag]) == 0:
            tagremove.append(tag)
    for tag in tagremove:
        dictal.pop(tag)
