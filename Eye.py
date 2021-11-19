import threading
import time
import sys
from postcomm import PostController


print([sys.argv[1]])
if len(sys.argv) == 2:
    p = PostController(host=sys.argv[1], port=sys.argv[2])
else:
    p = PostController()


def addtagloop():
    while True:
        try:
            userin = input()
            userin = userin.split(" ")
            if userin[0] == "tag":
                p.tag(userin[1])
                print(f"ADDED \"{userin[1]}\" as tag")
                continue
            elif userin[0] == "send":
                p.send(userin[1], userin[2])
                print("SENT MESSAGE")
                continue
        except (IndexError) as e:
            print(e)


threading.Thread(None, addtagloop).start()

print("""Eye is now running.
tag  {tag}                 |    Adds a tag
send {message} {tag}       |    Sends message to tag
""")
while True:
    time.sleep(0.01)
    if p.readable():
        recved = p.read()
        print(f"{recved[1]}: \"{recved[0]}\"")
