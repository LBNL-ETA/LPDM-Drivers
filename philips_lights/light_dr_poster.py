import socket
import time
import threading

class Light_DR_Poster(threading.Thread):
    def __init__(self):
        super(Light_DR_Poster, self).__init__()
        
    def write_to_lights(self, xml_to_write):
        ip="192.168.1.100"
        port=50020
        #s = socket.socket()
        address=(ip,port)
        
        self.sock = socket.create_connection(address, timeout=35)
        self.sock.setblocking(False)
        print "about to write the xml file to the socket"
        start_time = time.time()
        #lines = f.readlines()
        #time.sleep(2)
    
        #foo = ""
        print "Trying to wake up socket for writing"
        self.sock.send("")
#         time.sleep(0.1)
#         try:
#             while True:
#                 foo += self.sock.recv(1)
#                 print foo
#         except:
#             pass
        #time.sleep(5)
        #for l in lines:
        #   print l
        #   sock.send(l)
        print "Trying to write"
        self.sock.send(xml_to_write)
        #sock.shutdown(socket.SHUT_WR)
        chunk = ""
        #chunk = self.sock.recv(1)
        while (chunk.find("</events>") < 0):
            try:
                chunk += self.sock.recv(1)
                print chunk
            except Exception as e:
                pass
        
        print "Took {s} seconds to receive response:".format(s = time.time() - start_time)
        print chunk
        self.sock.close()
        return chunk
        #sock.close()
        