# date: 2018-09-27
# author: rawat s.

from microbit import *
import random
import radio

BLINK_COUNT=10
N = 5

#####################################################################
# m = a nxn matrix with elements from {0,1}
#####################################################################

def blink_diag_major(n, dly=100):
    pause(1000)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( i, i, (j%2)*9 )
        sleep(dly) 

def blink_diag_minor(n, dly=100):
    sleep(10*dly)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( n-1-i, i, (j%2)*9 )
        sleep(dly) 

def blink_vertical(n, c, dly=100):
    sleep(10*dly)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( c, i, (j%2)*9 )
        sleep(dly) 

def blink_horizontal(n, r, dly=100):
    sleep(10*dly)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( i, r, (j%2)*9 )
        sleep(dly) 

#####################################################################
    
def check_diag_major(m,n):
    if sum([m[i][i] for i in range(n)]) == n:
        blink_diag_major(n)
        return True
    return False

def check_diag_minor(m,n):
    if sum([m[n-1-i][i] for i in range(n)]) == n:
        blink_diag_minor(n)
        return True
    return False

def check_vertical(m,n):
    for c in range(n): 
        if sum([m[r][c] for r in range(n)]) == n:
            blink_vertical(n, c)
            return True
    return False

def check_horizontal(m,n):
    for r in range(n): 
        if sum([m[r][c] for c in range(n)]) == n:
            blink_horizontal(n, r)
            return True
    return False

#####################################################################

def print_matrix(m,n):
	for r in range(n):
		for c in range(n):
			print('{:3d}'.format(m[r][c]), end='')
		print()
	print('\n')

#####################################################################

def create_numbers_matrix( n ):
	numbers = [ i for i in range(1,n*n+1) ]
	m = [ n*[0] for i in range(n) ]
	last_end = n*n - 1
	for r in range(n):
		for c in range(n):
			index = random.randint( 0, last_end )
			m[r][c] = numbers.pop( index )
			last_end -= 1
	return m

def create_check_matrix( n ):
	mid = int(n/2)
	m = [ n*[0] for i in range(n) ]
	m[mid][mid] = 1
	return m

def update_check_matrix( numbers_mat, check_mat, n, number ):
	for c in range(n):
		for r in range(n):
			if numbers_mat[r][c] == number:
				check_mat[r][c] = 1
				break

def update_led_matrix( check_mat, n ):
    #display.clear()
    for r in range(n):
        for c in range(n):
            display.set_pixel( c, r, 7*check_mat[r][c] )

check_funcs = [check_diag_major, check_diag_minor, check_vertical, check_horizontal] 
 
#####################################################################

radio.on()
radio.config(channel=19)
radio.config(power=7)

#random.seed( pin0.read_analog() )

sleep(500)
if button_b.is_pressed():
    sender = True
    display.scroll( 'S', 200 ) # sender
else:
    sender = False
    display.scroll( 'R', 200 ) # receiver

if sender:
    while True:
        while True:
            if button_a.is_pressed(): # press button A to start 
                break
            sleep(100)

        sleep(1000)
        for number in range(1,N*N+1):
            radio.send( str(number) )
            display.scroll( str(number),200 )
            sleep(500)
            recv_msg = radio.receive()
            if recv_msg == 'bingo':
                display.scroll( 'Bingo!', 200 )
                break


else:
    while True:
        while True:
            if button_a.is_pressed(): # press button A to start 
                break
            if button_b.is_pressed():
                display.clear()
            sleep(100)

        # create a new matrix with random numbers
        numbers_m = create_numbers_matrix(N)
        # create a check matrix
        check_m = create_check_matrix(N)
        # update the LED matrix corresponding to the check matrix
        update_led_matrix( check_m, N )
        sleep(1000)

        bingo = False
        number = 0
        
        while True:
            recv_msg = radio.receive()
            if not recv_msg:
                sleep(100)
                continue

            if recv_msg == 'bingo':
                break
            else:
                number = int(recv_msg,10)
                
            # check the incoming number against the number matrix
            update_check_matrix( numbers_m, check_m, N, number )
            # update the LED matrix
            update_led_matrix( check_m, N )
           
            # check all the bingo conditions
            for f in check_funcs:
                bingo = bingo or f( check_m, N ) 
            if bingo:
                break
            sleep(500) 
    
        if bingo:
            radio.send( 'bingo' )
            sleep(1000) 
            display.scroll( 'Bingo!', 200 )
            display.show( Image.HAPPY )
            sleep(1000) 
            bingo = False

        update_led_matrix( check_m, N )