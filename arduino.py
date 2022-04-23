from pyfirmata import Arduino,SERVO

port = "/dev/ttyUSB0"
pin = 7
pin2 = 8
pin3 = 6 # yellow led
pin4 = 5 # red led

board = Arduino(port)

board.digital[pin].mode = SERVO 
board.digital[pin2].mode = SERVO 

def turnToServo(pin,angle):
    board.digital[pin].write(angle)

def door1(value):
    if value == 0 :
        turnToServo(pin,90)
    elif value == 1 :
        turnToServo(pin,270)

def door2(value):
    if value == 0 :
        turnToServo(pin2,90)
        led(6,1)
        led(5,0)
    elif value == 1 :
        turnToServo(pin2,0)
        led(6,0)
        led(5,1)

def led(pin,value):
    board.digital[pin].write(value)