#Umesh Dhakal
#Lab 2
#MSCS631
# UDPPingerClient.py
# This client sends 10 UDP ping messages to the server.
# It measures RTT (round-trip time) and handles packet loss using a 1 second timeout.

from socket import *
import time

serverName = "127.0.0.1"
serverPort = 12000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set a timeout of 1 second
clientSocket.settimeout(1)

# Track RTT values and lost packets
rttList = []
lost = 0

for sequence_number in range(1, 11):
    # Record the time the message is sent
    sendTime = time.time()

    # Create ping message in the format: Ping sequence_number time
    message = "Ping " + str(sequence_number) + " " + str(sendTime)

    try:
        # Send the ping message to the server
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Receive the server response
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)

        # Calculate RTT
        rtt = time.time() - sendTime
        rttList.append(rtt)

        # Print server message and RTT
        print(modifiedMessage.decode())
        print("RTT:", rtt, "seconds")

    except timeout:
        # If no response is received within 1 second, the packet is considered lost
        print("Request timed out")
        lost += 1

# Close the client socket
clientSocket.close()

# Print packet loss rate and RTT statistics
lossRate = (lost / 10) * 100
print("Packet loss rate:", lossRate, "%")

if len(rttList) > 0:
    print("Min RTT:", min(rttList), "seconds")
    print("Max RTT:", max(rttList), "seconds")
    print("Avg RTT:", (sum(rttList) / len(rttList)), "seconds")
