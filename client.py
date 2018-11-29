# Andrew Bishop
# Camosun College ICS 226 Lab 2 solution
# Oct. 5 /18

# Basic UDP Client
# Sends up to 10 4-bit integers to the server. Receives a 4-byte response
# and prints it (in base-10).
import socket, sys

host = sys.argv[1]
port = int(sys.argv[2])
operator = sys.argv[3]

# get the count of numbers to process
num_count = len(sys.argv) - 4
if num_count <= 1:
  print("please enter two or more integers")
  sys.exit()

if num_count > 10:
  print("please only enter up to ten integers between zero and 15")
  sys.exit()

# 1. create the socket using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. build the packet.
if operator == '+':
  operator = 1
  operation = 'add'
elif operator == '-':
  operator = 2
  operation = 'subtract'
elif operator == '*':
  operator = 4
  operation = 'multiply'
else:
  print("please enter an operator (+, -, *) to process the numbers")
  sys.exit()

packet = bytearray()
packet.append(operator)
packet.append(num_count)

# checking the numbers, packing them two to a byte
arg_len = len(sys.argv)

for i in range(4, arg_len, 2):
  num1 = int(sys.argv[i]) << 4
  if i+1 == arg_len:
    numbyte = num1
    packet.append(numbyte)
    break
  else:
    num2 = int(sys.argv[i+1])
    numbyte = num1 | num2
    packet.append(numbyte)
    
# 3. send the packet.
s.connect( (host, port) )
s.send(packet)

# 4. receive the response
data = s.recv(4)

data1 = data[0] << 24
data2 = data[1] << 16
data3 = data[2] << 8
data4 = data[3]
total = data1 + data2 + data3 + data4

#account for negative values
if 0b10000000 & data[0] > 0:
  total = total - 2**32

print(total)

# 5. unpack the byte array to a meaningful value.
# print(int.from_bytes(data, byteorder="big", signed=True))

s.close()
