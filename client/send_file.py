import socket              
import sys
# tqdm is used to print sending progress bar
import tqdm as tqdm
import os


# run with: python send_file.py <filename> <server-address> <port>
s = socket.socket()         
if len(sys.argv) != 4:
    print("Wrong input: {}, please use: <filename> <server-address> <port>".format(sys.argv[0]))
    sys.exit(1)

# Add separator, so we eill be able to split 
SEPARATOR = "<SEPARATOR>"
# number of units to be sent at once
sent_units = 1024
filename, host, port = sys.argv[1:4]
filesize = os.path.getsize(filename)

s.connect((host, int(port)))
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# Create a progress bar to track sent bytes
progress = tqdm.tqdm(range(filesize), f"Sending {filename}",
                     unit="B", unit_scale=True,
                     unit_divisor=sent_units)

f = open(filename,'rb')
u = f.read(sent_units)
# update progress bar
for _ in progress:
    s.send(u)
    u = f.read(sent_units)
    progress.update(len(u))

# close file and socket after sending
f.close()
print("\n{} is sent!\n".format(filename))
s.shutdown(socket.SHUT_WR)

s.close()
