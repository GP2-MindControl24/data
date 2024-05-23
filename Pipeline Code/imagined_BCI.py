import RPi.GPIO as GPIO
from time import sleep
import subprocess
import json
import numpy as np
import sys

GPIO.setmode(GPIO.BCM)
# Pins for Motor Driver Inputs 
Motor1E = 25  #Right
Motor1N = 23
Motor2N = 24

Motor2E = 22  #Left
Motor3N = 17
Motor4N = 27

GPIO.setup(Motor1E,GPIO.OUT) 
GPIO.setup(Motor1N,GPIO.OUT)
GPIO.setup(Motor2N,GPIO.OUT)

GPIO.setup(Motor2E,GPIO.OUT) 
GPIO.setup(Motor3N,GPIO.OUT)
GPIO.setup(Motor4N,GPIO.OUT)

PWM_FREQ = 100
SLOW_SPEED_DUTY_CYCLE = 50 

pwm_motor1 = GPIO.PWM(Motor1E, PWM_FREQ)
pwm_motor2 = GPIO.PWM(Motor2E, PWM_FREQ)

def move_forward():

    GPIO.output(Motor1N,GPIO.HIGH)
    GPIO.output(Motor2N,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor3N, GPIO.LOW) 
    GPIO.output(Motor4N, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)

    pwm_motor1.start(SLOW_SPEED_DUTY_CYCLE)
    pwm_motor2.start(SLOW_SPEED_DUTY_CYCLE)

def move_backward():

    GPIO.output(Motor1N,GPIO.LOW)
    GPIO.output(Motor2N,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor3N, GPIO.HIGH) 
    GPIO.output(Motor4N, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)

    pwm_motor1.start(SLOW_SPEED_DUTY_CYCLE)
    pwm_motor2.start(SLOW_SPEED_DUTY_CYCLE)
   
def turn_left():
    # Set motor 1 (left motor) to move backward
    GPIO.output(Motor3N, GPIO.HIGH) 
    GPIO.output(Motor4N, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)
    pwm_motor2.start(SLOW_SPEED_DUTY_CYCLE)
   
    
    # Set motor 2 (right motor) to move forward
    GPIO.output(Motor1N,GPIO.HIGH)
    GPIO.output(Motor2N,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

def turn_right():

    # Set motor 1 (left motor) to move backward
    GPIO.output(Motor3N, GPIO.LOW) 
    GPIO.output(Motor4N, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)
    pwm_motor2.start(SLOW_SPEED_DUTY_CYCLE)
   
    
    # Set motor 2 (right motor) to move forward
    GPIO.output(Motor1N,GPIO.LOW)
    GPIO.output(Motor2N,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)


def stop():

    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.LOW)



def label(script_path,test_path):
    # Run the trained_model script and capture its output
    result = subprocess.run(
        ['python', script_path,test_path],
        capture_output=True,
        text=True
    )
    # Check for errors in the script execution
    if result.returncode != 0:
        print("Error running trained_model script:")
        print(result.stderr)
        return None
    
    # Return the stdout which contains the predictions
    return result.stdout

# Path to the trained_model script
if len(sys.argv) != 2:
        print("Usage: python forward.py <input_csv_file>")
        sys.exit(1)


model_script_path = "/home/ajh/test_model.py"
csv_paths = sys.argv[1]

output = str(label(model_script_path, csv_paths))
print(output)

    # Move forward
if output == 'Up\n':
        move_forward()
        sleep(1)
        stop()

    # Move Backward
elif output == 'Down\n':
        move_backward()
        sleep(1)
        stop()
    

    # Move left
elif output == 'Left\n':
       turn_left()
       sleep(0.5)
       stop()

    #Move right
elif output == 'Right\n':
       turn_right()
       sleep(0.5)
       stop()

    # Clean up GPIO
GPIO.cleanup()
