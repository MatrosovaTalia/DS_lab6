import os
import socket
from threading import Thread
from os import walk

clients = []
host = '172.31.45.95' # replace with 127.0.0.1 to run oh localhost
port = 2609
SEPARATOR = "<SEPARATOR>"
copy = 1

## This is a thread approach 
# We need to have a separate thread to each client
# and use blocking approach
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # close connection after client is done
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        try:

            data = self.sock.recv(1024).decode()
            filename, filesize = data.split(SEPARATOR)
            filename = os.path.basename(filename)

            # same name check
            filename = check_for_repeat(filename)

            with open(filename, "wb") as f:
                bytes_read = True
                while(bytes_read):
                    bytes_read = self.sock.recv(1024)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

            f.close()
            print("\n{} is received!\n".format(filename))
        except ValueError:
            print()

        finally:
            self._close()





def main():
    n_clients = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    # enable server to accept connections
    sock.listen(0)
    while True:
        con, addr = sock.accept()
        clients.append(con)
        n_clients += 1
        print("Client {} is connected from {}".format(n_clients, addr))
        ClientListener(n_clients, con).start()



# This function checks, whether there is a file with the same name
# and replaces the filename to copy_n if there is already the same name file
def check_for_repeat(filename):
    global copy
    files = []
    for (dirpath, dirnames, filenames) in walk('./'):
        files.extend(filenames)
        break

    if files.__contains__(filename):
        name, extension = os.path.splitext(filename)
        new_filename = "{}_copy{}{}".format(name, copy, extension)
        copy += 1

        return new_filename
    else:
        return filename

if __name__ == "__main__":
    main()
