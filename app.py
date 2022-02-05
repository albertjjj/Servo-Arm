from flask import *
from flask_wtf import *
from gpiozero import OutputDevice as stepper
from gpiozero import Servo
from time import sleep
import time


servo = Servo(18)
IN1 = stepper(24)
IN2 = stepper(25)
IN3 = stepper(8)
IN4 = stepper(7)
stepPins = [IN1,IN2,IN3,IN4]
mode = 0

IN5 = stepper(4)
IN6 = stepper(17)
IN7 = stepper(22)
IN8 = stepper(27)
stepPins2 = [IN5,IN6,IN7,IN8]

actions = [50]
actions2 = [50]


app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))

@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/slider_update', methods=['POST', 'GET'])
def slider():
    current = int(request.data)
    length = len(actions)
    seq = [[1,0,0,0],
             [0,1,0,0],
             [0,0,1,0],
             [0,0,0,1]]

    if current > actions[length-1]:
        stepDir = 1
        stepsNeeded = (2048 * (current/100)) - (2048 * (actions[length-1]/100))
    elif current < actions[length-1]:
        stepDir = -1
        stepsNeeded = (2048 * (actions[length-1]/100)) - (2048 * (current/100))


    num = round(stepsNeeded)

    stepCount = len(seq)
    stepCounter = 0

    for x in range(0, num):
        for pin in range(0,4):
            xPin=stepPins[pin]
            if seq[stepCounter][pin]!=0:
                xPin.on()
            else:
                xPin.off()
        stepCounter += stepDir
        if (stepCounter >= stepCount):
            stepCounter = 0
        if (stepCounter < 0):
            stepCounter = stepCount+stepDir
        time.sleep(0.004)
    actions.append(current)
    print(actions)

    return str(current)

@app.route('/slider_update2', methods=['POST', 'GET'])
def slider2():
    current2 = int(request.data)
    length = len(actions2)
    seq = [[1,0,0,0],
             [0,1,0,0],
             [0,0,1,0],
             [0,0,0,1]]

    if current2 > actions2[length-1]:
        stepDir = 1
        stepsNeeded = (2048 * (current2/100)) - (2048 * (actions2[length-1]/100))
    elif current2 < actions2[length-1]:
        stepDir = -1
        stepsNeeded = (2048 * (actions2[length-1]/100)) - (2048 * (current2/100))


    num = round(stepsNeeded)

    stepCount = len(seq)
    stepCounter = 0

    for x in range(0, num):
        for pin in range(0,4):
            xPin=stepPins2[pin]
            if seq[stepCounter][pin]!=0:
                xPin.on()
            else:
                xPin.off()
        stepCounter += stepDir
        if (stepCounter >= stepCount):
            stepCounter = 0
        if (stepCounter < 0):
            stepCounter = stepCount+stepDir
        time.sleep(0.004)
    actions2.append(current2)
    print(actions2)

    return str(current2)


@app.route('/buttonUpdate', methods=['POST', 'GET'])
def button():

    val = int(request.data)

    if val == 2:
        servo.min()
    elif val == 1:
        servo.max()
    else:
        print('button error')

    return str(val)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)