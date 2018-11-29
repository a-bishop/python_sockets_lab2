# Andrew Bishop
# Camosun College ICS 226 Lab 2 solution
# Oct. 5 /18

# Basic UDP server
# Receives 1-byte integers, adds them, and returns the 4-byte result.
import socket, sys

port = int(sys.argv[1])

# Create the socket object using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the port. Using "" for the interface so it binds to
# all known interfaces, including "localhost".
s.bind(("", port))

# Servers stay open -- they handle a client, then loop back
# to wait for another client.
while True:

    # wait for a client to send a packet
    packet, addr = s.recvfrom(1024)

    # unpack the data.
    operator = packet[0]
    if operator & 1 != 0:
        operator = '+'
    elif operator & 2 != 0:
        operator = '-'
    elif operator & 4 != 0:
        operator = '*'

    count = int(packet[1])

    start = True
    neg = False

    for nums in packet[2:]:
        # print(nums)
        # print(count)
        # print(len(packet))
        mask = 8
        two = 0
        last = (len(packet) - 1)
        one = nums >> 4
        if nums & mask != 0:
            two = 8
        if nums & (mask >> 1) != 0:
            two = two + 4
        if nums & (mask >> 2) != 0:
            two = two + 2
        if nums & (mask >> 3) != 0:
            two = two + 1
        # Calculate the result.
        if operator == '+':
            if start == True:
                result = one + two
                start = False;
            elif (nums == packet[last]):
                if (count % 2 == 1):
                    result = result + one
                else:
                    result = one + two + result
            else:    
                result = one + two + result
        elif operator == '-':
            if start == True:
                result = one - two
                start = False;
            elif (nums == packet[last]):
                if (count % 2 == 1):
                    result = result - one
                else:
                    result = result - one - two
            else:
                result = result - one - two
        elif operator == '*':
            if start == True:
                result = one * two
                start = False;
            elif (nums == packet[last]):
                if (count % 2 == 1):
                    result = result * one
                else:
                    result = result * one * two
            else: 
                result = result * one * two

    return_packet = bytearray()
    #print(result);

    byte1 = (result >> 24 & 0xFF)
    return_packet.append(byte1)
    
    byte2 = (result >> 16 & 0xFF)
    return_packet.append(byte2)
    
    byte3 = (result >> 8 & 0xFF)
    return_packet.append(byte3)
    
    byte4 = (result & 0xFF)
    return_packet.append(byte4)
    
    # Pack the result into a byte array.
    #return_packet = result.to_bytes(4, byteorder="big", signed=True)

    # # Send the packet back to the client.
    s.sendto(return_packet, addr)
