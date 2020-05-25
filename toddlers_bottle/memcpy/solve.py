def round8(x):
    return (x + 7) & ~(8 - 1)

def align(start):
    # (size + 4) to accomodate malloc metadata
    while round8(start + 4) % 16 != 0:
        start += 4
    return start

for sz in [64, 128, 256, 512, 1024, 2048, 4096]:
    print(align(sz))
