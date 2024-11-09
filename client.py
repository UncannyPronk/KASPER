import socket, pyperclip
from device_detector import DeviceDetector

# Replace this with an actual User-Agent string to test
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"

dd = DeviceDetector(user_agent)
device_info = dd.parse()

# Access device details
device_type = device_info.device_type()

# dd = device_detector.DeviceDetector(request.headers.get('User-Agent'))
# device_info = dd.detect()

# Establish connection to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostbyname(socket.gethostname()), 5000))
s.connect(("localhost", 8080))

# Send client name to server
s.send(socket.gethostname().encode())
# s.send(input("Enter name: ").encode())
print(s.recv(1024).decode())
s.send(device_type.encode())
print(s.recv(1024).decode())

prevpaste = ""

def waitForNewPaste():
    global prevpaste
    while True:
        newpaste = str(pyperclip.paste())
        if newpaste != prevpaste:
            print(prevpaste, newpaste)
            prevpaste = newpaste
            break
    return newpaste

while True:
    # Send message to server
    message = waitForNewPaste()
    # print(f"1: {message}")
    if message != None:
        s.send(message.encode())
    # else:
    #     s.send("".encode())
    #     print("nothing")
    # print("message sent")

    # Quit chat
    if message == 'exit':
        s.close()
        break

    # Read incoming message
    message = s.recv(1024).decode()
    print(message)
    if message != None:
        # print(message)
        pyperclip.copy(message)
        print("Message copied to clipboard")
