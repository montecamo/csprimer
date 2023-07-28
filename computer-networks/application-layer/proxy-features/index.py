import socket
import sys
import signal
import select
from proxy import Proxy
from log import log

OWN_ADDR = ("0.0.0.0", 8000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(OWN_ADDR)
s.listen()
fd = s.fileno()


def handler(_, __):
    s.close()
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


kqueue = select.kqueue()
events = [select.kevent(s.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD)]
proxies = {}

while True:
    for event in kqueue.control(events, len(events)):
        if event.ident == s.fileno():
            client_sock, client_addr = s.accept()
            log(f"New connection from {client_addr}")

            proxies[client_sock.fileno()] = Proxy(client_sock)

            event = select.kevent(
                client_sock.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD
            )

            events.append(event)
        else:
            if not event.ident in proxies:
                continue

            proxy = proxies[event.ident]

            proxy.handle()

            if proxy.state == "CLOSE":
                events = [x for x in events if x.ident != event.ident]
