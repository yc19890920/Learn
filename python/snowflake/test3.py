

fp = open("1.txt", 'rb')
lines = fp.readlines()
print lines
print len(lines)

print len(set(lines))
