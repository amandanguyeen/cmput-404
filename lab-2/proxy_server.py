#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

from numpy import true_divide 

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# okay so you need a client socket to talk to google
# but you keep this main socket so your client can connect

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode()) 
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    
        #QUESTION 3
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        server_socket.bind((HOST, PORT))
        #set to listening mode
        server_socket.listen(2)
        
        #continuously listen for connections, this is where your client will connect 
        while True:
            conn, addr = server_socket.accept()
            print("Connected by", addr)

            p = Process(target= proxy_handler, args=(conn,addr))
            p.daemon = True
            p.start()
            conn.close()


def proxy_handler(conn, addr):
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)

    # WRITE CLIENT SOCKET HERE!!!!
    try:
        #define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        buffer_size = 4096

        #make the socket, get the ip, and connect
        google_client_socket = create_tcp_socket()

        remote_ip = get_remote_ip(host) 

        google_client_socket.connect((remote_ip , port))
        print (f'Socket Connected to {host} on ip {remote_ip}')

        ## i could technically hardcode the payload, but i wanted to utilize full_data but you have to replace hostname
        payload = full_data.decode("utf-8").replace('127.0.0.1', host)

        #send the data and shutdown
        send_data(google_client_socket, payload)
        google_client_socket.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        google_response = b""
        while True:
            data = google_client_socket.recv(buffer_size)
            if not data:
                break
            google_response += data
        print(google_response)
        conn.sendall(google_response) 
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        google_client_socket.close()
        

if __name__ == "__main__":
    main()
