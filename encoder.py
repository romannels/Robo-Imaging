import RPi.GPIO as GPIO
import Image from PIL

#---------------------------------------------------------------------#
#-----------------------------Variables-------------------------------#
#---------------------------------------------------------------------#

Channel_A_Pin = 22		# connected to motor controller board Channel A
Channel_B_Pin = 23		# connected to motor controller board Channel B 
Interrupt_Pin = 24		# connected to motor controller board OR output
Turning_Pin = 25        #connected to Arduino
Direction = 1 #x direction, y direction is 0
Minimum_Distance = 4 # Minimum distance before killing robot
x, y = 0
pi = 3.14159265
x_coordinate = []
y_coordinate = []
ticks_per_revolution = 333
diameter = 4 #centimeters
distance_per_tick = pi * diameter / ticks_per_revolution
GPIO.setmode(GPIO.BCM) #setup GPIO using BCM numbering
#setup images
Map =Image.new(‘RGBA’, (600,600), (0,0,0,0))
draw = ImageDraw.Draw(Map)
QEM = [0,-1,1,2,1,0,2,-1,-1,2,0,1,2,1,-1,0] #Direction list
TURNING = 1 #this means it is turning, i.e. the GPIO pin connected to Arduino is high

#---------------------------------------------------------------------#
#-------------------------Initialize GPIO pins------------------------#
#---------------------------------------------------------------------#

GPIO.setup(Channel_A_Pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #Channel A
GPIO.setup(Channel_B_Pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #Channel B
GPIO.setup(Interrupt_Pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #Interrupt
GPIO.setup(Turning_Pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #Arduino, turn signal

InputA = GPIO.input(Channel_A_Pin)
InputB = GPIO.input(Channel_B_Pin)

GPIO.add_event_detect(Interrupt_Pin, GPIO.RISING, callback=where_am_I) # check interrupt pin and use where_am_I
GPIO.add_event_detect(Turning_Pin, GPIO.RISING, callback=position_ah_yeah) # Interrupts if vehicle is turning
GPIO.add_event_detect(Turning_Pin, GPIO.FALLING, callback=not_turning_ok) # Interrupts if vehicle has stopped turning




#---------------------------------------------------------------------#
#-----------------------------Functions-------------------------------#
#---------------------------------------------------------------------#

#if not turning, this updates the current x, or y position based on current direction
def where_am_I():
	if (Turning != TURNING):
		Old = New
		New = inputA + inputB
		Out = QEM[(old * 4) + new]
		Out = Out * distance_per_tick
		
		#this part didn't work and is somewhat useless
		#if (Out == 2):
			#print 'crap, something\'s messed up bro'
	
		if direction == 1:
			x = x + Out # increment in x direction
		elif direction == 2:
			y = y + Out # increment in y direction
		elif direction == 3:
			x = x - Out
		elif direction == 0:
			y = y - Out
    all_done()
			
			
# If robot changes turn state this picks the right one (i.e.:+x,-x,+y, or -y)			
def position_ah_yeah():
	turning_ok()
	Direction = Direction++
	Direction = Direction % 4 # picks one of four states
	
	update_list()
	
# probably didn't need this in a function, but changes state from not turning (going forward) to turning	
def turning_ok():
    Turning = TURNING
	
# probably didn't need this in a function, but changes state from turning to not turning (going forward)	
def not_turning_ok():
    Turning = !TURNING

# adds new coordinates to the x and y arrays	
def update_list():
    x_coordinate.append(x)
	y_coordinate.append(y)
	
	
# checks to see if robot has gone around room
def all_done():
    x_dim = len(x_coordinate)
	y_dim = len(y_coordinate)
	
	if(x_dim && y_dim  > 1):
	    if ((x_coordinate[x_dim] && y_coordinate[y_dim]) <= Minimum_Distance):
			x_coordinate = [int(x_i) for x_i in x_coordinate]
			y_coordinate = [int(y_i) for y_i in y_coordinate]
			 
			DrawMap(x_coordinate,y_coordinate)
			

			
#Draws line segments between consecutive points on a black background.  Color set to green (0,128,0,0)
def DrawMap(x_array, y_array):
	points = len(x_array)
	if (points != len(y_array))
		print 'something bad happened'
	i = 0
	while i<(points – 1):
		draw.line((x_array[i],y_array[i], x_array[i+1], y_array[i+1]), fill = (0,128,0,0), width = 3)
		i += 1
	OutputFile = ‘C://map.jpeg’
	Map.save(OutputFile, “JPEG”)
		    
			



