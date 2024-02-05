import socket

from dns import *

query = build_query("www.example.com", TYPE_A)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(query, ("8.8.8.8", 53))
response, _ = sock.recvfrom(1024)
