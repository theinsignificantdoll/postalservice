import socket
import select


class PostController:
    def __init__(self, host="127.0.0.1", port=28729):
        self.buffer = []
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(0.01)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(None)
        self.registeredtags = []

    def tag(self, tag):
        self.sock.sendall(f"<<START>>SETRECV{tag}<<END>>".encode("ASCII", "ignore"))

    def tags(self, tags):
        for tag in tags:
            self.tag(tag)

    def deltag(self, tag):
        self.sock.sendall(f"<<START>>DELRECV{tag}<<END>>".encode("ASCII", "ignore"))

    def deltags(self, tags):
        for tag in tags:
            self.deltag(tag)

    def readable(self):
        if self.buffer:
            return True
        r, w, e = select.select((self.sock, ), [], [], 0)
        return r != []

    def read(self):
        if len(self.buffer) != 0:
            return self.buffer.pop(0)
        recved = self.sock.recv(1024).decode("ASCII", "ignore")
        if recved == "":
            raise ConnectionAbortedError
        recved = recved.replace("<<START>>", "")
        recved = recved.split("<<END>>")
        try:
            while True:
                recved.remove("")
        except ValueError:
            pass
        out = recved[0].split("<<||>>")
        out.reverse()
        for n in recved[1:]:
            o = n.split("<<||>>")
            o.reverse()
            self.buffer.append(o)
        return out

    def send(self, mess, tag):
        self.sock.sendall(f"<<START>>{tag}<<||>>{mess}<<END>>".encode("ASCII", "ignore"))

