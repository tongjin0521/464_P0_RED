#!/usr/bin/env python

'''
final_control.py

This is the final and only python file we used during the competition. 
When running, it will start and run an app called P0App(), which controls the whole running process.
Inside P0App(), we created four Motion () instances: forward, turn_left, turn_right, and lift.
Motion() is a subclass of Plan that helps us control motions, including continuous motions, like forward, or one-time motion, like turn_left and turn_right.
Motion() takes six inputs as (1)app: P0App(); (2)servo: the servo we want to control; (3)start_pos: the position we want the motor to start; (4)end_pos: the position we want the motor to end; (5)step_size: how large a step we want to move for each while loop; (6)reset_pos: the position we want the motor to be at when we end the movement; (7) loop: whether we want the movement to be continuous or just one-time. 
Inside P0App(), we also have a function called reset_mode, which helps us reset the motors to their reset positions.
P0App() will take keyboard input and correspondingly run certain predefined motions when P0App() is initialized. The details on how to control it is listed in the USAGE.txt.
 
'''
from joy.plans import Plan
from joy.decl import *
from joy.misc import *
from joy import *
import ckbot
import time 

RESET_FRONT_ANGLE = 6100
RESET_BACK_ANGLE = 0
RESET_FRONT_STEP_SIZE = 160
RESET_BACK_STEP_SIZE = 56

MANUAL_FRONT_STEP_SIZE = 400
MANUAL_BACK_STEP_SIZE = 400

LEFT_TURN_RESET_ANGLE = 0
LEFT_TURN_START_ANGLE = 0
LEFT_TURN_END_ANGLE = -1600
LEFT_TURN_STEP_SIZE = 56

RIGHT_TURN_RESET_ANGLE = 0
RIGHT_TURN_START_ANGLE = 0
RIGHT_TURN_END_ANGLE = 1600
RIGHT_TURN_STEP_SIZE = 56

FORWARD_REST_ANGLE = RESET_FRONT_ANGLE
FORWARD_START_ANGLE = RESET_FRONT_ANGLE
FORWARD_END_ANGLE = -1600
FORWARD_STEP_SIZE = 130

LIFT_RESET_ANGLE = RESET_FRONT_ANGLE
LIFT_START_ANGLE = RESET_FRONT_ANGLE
LIFT_END_ANGLE = 2000
LIFT_STEP_SIZE = 150


def angle_limit_check(input_angle):
    if (input_angle > 9700):
      return 9700
    elif (input_angle < -9700):
      return -9700
    else:
      return input_angle

class Motion (Plan):
    def __init__(self, app, servo, start_pos=-9780, end_pos=9780, step_size=100, reset_pos=0, loop = False, *arg,**kw):
        Plan.__init__(self,app,**kw)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.reset_pos = reset_pos
        self.step_size = step_size
        self.servo = servo
        self.loop = loop
        self.increase = -1
        self.app = app

    def change_pos(self):
        if self.loop:
            if self.current_pos < self.end_pos:
                self.increase = 1
            if self.current_pos > self.start_pos:
                self.increase = -1
            self.servo.set_pos(angle_limit_check(self.current_pos + self.increase * self.step_size))
            
        else:
            self.increase = -1 if self.current_pos > self.end_pos else 1
            self.servo.set_pos(angle_limit_check(self.current_pos + self.increase * self.step_size))
        
        self.current_pos = angle_limit_check(self.current_pos + self.increase * self.step_size)
    def behavior(self):
        if self.loop:
            while (True):
                yield
                self.change_pos()
        else:
            print(self.current_pos)
            while (abs(self.current_pos - self.end_pos) > self.step_size):
                print(self.current_pos)
                self.change_pos()
            yield
            self.stop()

    def onStop(self):
        if self.loop:
            self.servo.set_pos(angle_limit_check(self.reset_pos))
        else:
            
            if self.end_pos == LEFT_TURN_END_ANGLE or self.end_pos == RIGHT_TURN_END_ANGLE:
                self.app.reset_mode()
    
    def onStart(self):
        self.servo.set_pos(angle_limit_check(self.start_pos))
        self.current_pos = self.start_pos

class P0App( JoyApp ):
    def __init__(self,robot=dict(count=2),*arg,**kw):
        cfg = dict ()

        # initializes the application's app.robot attribute
        JoyApp.__init__(self,robot=robot,cfg=cfg,*arg,**kw)

        # Handle connecting to the servos
        c = ckbot.logical.Cluster(count=2, names={
          0x10: 'back',
          0x17: 'front',
        })

        self.back = c.at.back
        self.front = c.at.front
        self.forward = Motion(self,self.front,start_pos=FORWARD_START_ANGLE,end_pos = FORWARD_END_ANGLE,reset_pos = FORWARD_REST_ANGLE,step_size = FORWARD_STEP_SIZE,loop = True )
        self.turn_left = Motion(self,self.back,start_pos =LEFT_TURN_START_ANGLE,end_pos= LEFT_TURN_END_ANGLE,reset_pos=LEFT_TURN_RESET_ANGLE,step_size=LEFT_TURN_STEP_SIZE,loop = False )
        self.turn_right = Motion(self,self.back,start_pos =RIGHT_TURN_START_ANGLE,end_pos= RIGHT_TURN_END_ANGLE,reset_pos=RIGHT_TURN_RESET_ANGLE,step_size=RIGHT_TURN_STEP_SIZE ,loop = False)
        self.lift = Motion(self,self.front,start_pos =LIFT_START_ANGLE,end_pos= LIFT_END_ANGLE,reset_pos=LIFT_RESET_ANGLE,step_size=LIFT_STEP_SIZE,loop = False )

    def reset_mode(self):
        curr_angle_front = self.front.get_pos()
        front_increase = 1 if RESET_FRONT_ANGLE > curr_angle_front else -1
        while abs(curr_angle_front - RESET_FRONT_ANGLE) > RESET_FRONT_STEP_SIZE:
            self.front.set_pos(angle_limit_check(curr_angle_front + front_increase*RESET_FRONT_STEP_SIZE))
            curr_angle_front = angle_limit_check(curr_angle_front + front_increase*RESET_FRONT_STEP_SIZE)
        curr_angle_back = self.back.get_pos()
        back_increase = 1 if RESET_BACK_ANGLE > curr_angle_back else -1
        while abs(curr_angle_back - RESET_BACK_ANGLE) > RESET_BACK_STEP_SIZE:
            self.back.set_pos(angle_limit_check(curr_angle_back + back_increase*RESET_BACK_STEP_SIZE))
            curr_angle_back = angle_limit_check(curr_angle_back + back_increase*RESET_BACK_STEP_SIZE)
    
    def onStart(self):
        progress("Started program")

    def onEvent(self,evt):
        """
        Responds to keyboard events
            - left arrow: go left
            - right arrow: go right
            - up arrow: go forward
            - space key: pause/stop
        """
        progress("----------")
        if evt.type != KEYDOWN:
            return
            
        # assertion: must be a KEYDOWN event
        if evt.key == K_LEFT:
            progress("KEY: LEFT")
            self.forward.stop()
            self.turn_right.start()
            self.lift.start()
            
            self.turn_left.start()

            # self.reset_mode()


        elif evt.key == K_RIGHT:
            progress("KEY: RIGHT")
            self.forward.stop()
            self.turn_left.start()
            self.lift.start() 
            
            self.turn_right.start()

            # self.reset_mode()

        elif evt.key == K_UP:
            # go forward (up arrow)
            progress("KEY: UP")
            # self.back.set_pos(-1000)
            self.forward.start()

        elif evt.key ==K_DOWN:
            pass

        elif (evt.key == K_w ):
            progress("KEY: W")
            front_pos = self.front.get_pos()
            self.front.set_pos( angle_limit_check(front_pos - MANUAL_FRONT_STEP_SIZE ))
        elif (evt.key == K_s):
            progress("KEY: S")
            front_pos = self.front.get_pos()
            self.front.set_pos( angle_limit_check(front_pos + MANUAL_FRONT_STEP_SIZE ))
        elif (evt.key == K_a):
            progress("KEY: A")
            back_pos = self.back.get_pos()
            self.back.set_pos( angle_limit_check(back_pos + MANUAL_BACK_STEP_SIZE ))
        elif (evt.key == K_d):
            progress("KEY: D")
            back_pos = self.back.get_pos()
            self.back.set_pos( angle_limit_check(back_pos - MANUAL_BACK_STEP_SIZE ))
        elif (evt.key == K_r):
            progress("KEY: R")
            self.forward.stop()
            self.reset_mode()
        elif evt.key == K_q:
            progress("KEY: Q")
            self.stop()

        # Hide robot position events
        elif evt.type==CKBOTPOSITION:
            return

        # Send events to JoyApp if not recognized
        JoyApp.onEvent(self,evt)

    def onStop(self):
        progress("P0App: onStop called")

#main function
if __name__=="__main__":
    app = P0App()
    app.run()
