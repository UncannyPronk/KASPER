import socket as s, threading as t, sys, time

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind(("", 5000))

server.listen()

print(f"Server started on {s.gethostbyname(s.gethostname())}\nAwaiting connections...\n")

devices = {}
device_types = {}
olddata = " "

emptyserver = True

def handle_devices(connection, address):
    global emptyserver, client_thread, devices, device_types, olddata
    device_name = connection.recv(1024).decode()
    devices[device_name] = connection
    connection.send("message received".encode())
    device_type = connection.recv(1024).decode()
    device_types[device_name] = device_type
    connection.send("message received".encode())
    print(f"{device_types} {device_name} has joined the server.")
    emptyserver = False

    while True:
        data = connection.recv(1024).decode()

        # print(data)
        if data == "exit":
            print(device_name+" has left the server")
            # try:
                # del device_types["*"+str(device_name)]
            # except KeyError:
            #     pass
            del devices[device_name]
            # print(device_types)
            # connection.send(str(device_types).encode())
            connection.close()
            try:
                client_thread.join()
            except RuntimeError:
                pass
                # serversocket.close()
                # sys.exit()
                
            if not emptyserver and len(devices) == 0:
                end = input("end server? (yes/no):")
                if end != "no":
                    server.close()
                    sys.exit()
            break
        else:
            for i in data.split("*"):
                if i == "_ignore_":
                    data = olddata
                    # print("old:"+olddata)
                    connection.send("*_ignore_*".encode())
                    # try:
                    #     for device in devices:
                    #         devices[device].send("*_*ignore_*_".encode())
                    #         time.sleep(1)
                    # except RuntimeError:
                    #     for device in devices:
                    #         devices[device].send("*_*ignore_*_".encode())
                    #     continue
                # elif data == "*_*ignore_*_*_*ignore_*_":
                #     for device in devices:
                #         devices[device].send("*_*ignore_*_".encode())
                    break
            else:
                print(device_name +" : "+data)
                for device in devices:
                    if data != olddata:
                        print(f"sending to {device}")
                        devices[device].send(str(data).encode())
                        time.sleep(1)
                olddata = data
                # connection.send("Ack".encode())

while True:
    global client_thread

    try:
        devicesocket, address = server.accept()
    except OSError:
        server.close()
        sys.exit()
        
    client_thread = t.Thread(target=handle_devices, args=(devicesocket, address))
    # client_thread.daemon = True
    client_thread.start()
