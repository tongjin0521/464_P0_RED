#!/usr/bin/env python

'''
FILE RobotDriver.py

This file is used to control a robot with three servos. It is meant for a
configuration with three servos in a straight line. The front servo has a
leg on the left side, the middle servo has a leg on the right side, and the
rear servo has legs on both sides.

To move forward, both the front and middle servos are used in tandem. To turn
left, the middle servo is used and to turn right the front servo is used.

The rear servo is used to move backwards and is positioned the opposite direction
of the front two servos.
'''
from joy.plans import Plan
from joy.decl import *
from joy.misc import *
from joy import *
import ckbot

LEFT_STEP_SIZE = 500
RIGHT_STEP_SIZE = 500
FORWARD_STEP_SIZE = 100
LIFT_ANGLE = -3000
BACK_START_ANGLE = 0
FRONT_START_ANGLE = 2000
def angle_limit_check(input_angle):
    if (input_angle > 9700):
      return 9700
    elif (input_angle < -9700):
      return -9700
    else:
      return input_angle

class Servo (Plan):
    def __init__(self, app, servo, min_pos=-9780, max_pos=9780, pos_step=100, start_pos=0, run=True, *arg,**kw):
        """A helper class to handle servo interactions

        Args:
            servo: The physical servo from pyckbot
            min_pos: The minimum position the servo can be set to
            max_pos: The maximum position the servo can be set to
            pos_step: The amount to change the servo position each time
                change_pos is called
            start_pos: The position the servo should be set to when starting
                the plan.
            run: Whether the server should change its position after being set
                to the start position. If False, the servo will not take any
                further movement.

        Returns:
            An instance of a Servo class.
        """
        Plan.__init__(self,app,**kw)
        self.name = servo.name
        self.start_pos = start_pos
        self.max_pos = max_pos
        self.min_pos = min_pos
        self.pos_step = pos_step
        self.increase = True
        self.servo = servo
        self.run = run

    def increase_pos(self):
        """
        Increases the position of a servo by the position step.
        Only changes the position if self.run == True
        """
        if self.run:
            self.set_pos(self.current_pos + self.pos_step)

    def decrease_pos(self):
        """
        Decreases the position of a servo by the position step.
        Only changes the position if self.run == True
        """
        if self.run:
            self.set_pos(self.current_pos - self.pos_step)

    def set_pos(self, pos):
        """Sets the position of the servo to pos

        Args:
            pos: A positive or negative value to set the position to
        """
        self.servo.set_pos(angle_limit_check(pos))
        self.current_pos = pos

    def change_pos(self):
        """Decides how to change the position of the servo

        If the current position is greater than the maximum position,
        will set self.increase to be False. If the current position is less
        than the minimum position, will set self.increase to be True.

        If self.increase is True, it will call self.increase_pos otherwise
        it will call self.decrease_pos
        """
        if self.current_pos > self.max_pos:
            self.increase = False
        if self.current_pos < self.min_pos:
            self.increase = True

        act = self.increase_pos if self.increase else self.decrease_pos
        act()
    
    def behavior(self):
        """
        Will continiously change the servo's position until
        the plan is stopped.

        Yields control back to JoyApp to make sure any other events
        can be handled.
        """
        while True:
            yield
            self.change_pos()

    def onStop(self):
        self.set_pos(self.start_pos)
    
    def onStart(self):
        self.set_pos(self.start_pos)

class P0App( JoyApp ):
    '''
    The P0App handles keyboard events to stop or start plans.
    '''

    '''
    This searches for three servors named 'front', 'middle', and 'back'
    It overrides anything specified in the .yml file.

    Servos are initialized and plans are created.
    '''
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
        self.forwarding = False
        self.front_servo = Servo(self,self.front,min_pos = -4000, max_pos =2000, start_pos = 6000,pos_step = FORWARD_STEP_SIZE)

    def onStart(self):
        """
        Don't act until told to start moving forward
        Doesn't take any actions in onStart
        """
        self.back.set_pos(angle_limit_check(BACK_START_ANGLE))
        self.front.set_pos(angle_limit_check(FRONT_START_ANGLE))
        progress("Started program")

    def onEvent(self,evt):
        """
        Responds to keyboard events
            - left arrow: go left
            - right arrow: go right
            - up arrow: go forward
            - space key: pause/stop
        """
        if evt.type != KEYDOWN:
            return

        # assertion: must be a KEYDOWN event
        if evt.key == K_LEFT:
            # go left (left arrow)
            # if self.forwarding:
            #   self.forwarding = False
            #   self.front_servo.stop()
            curr_pos = self.back.get_pos()
            self.back.set_pos(angle_limit_check(curr_pos - LEFT_STEP_SIZE))

        elif evt.key == K_RIGHT:
            # go right (right arrow)
            # if self.forwarding:
            #   self.forwarding = False
            #   self.front_servo.stop()
            curr_pos = self.back.get_pos()
            self.back.set_pos(angle_limit_check(curr_pos + LEFT_STEP_SIZE))

        elif evt.key == K_UP:
            # go forward (up arrow)
            if not self.forwarding:
              self.forwarding = True
              self.front_servo.start()

        elif evt.key ==K_DOWN:
            if self.forwarding:
              self.forwarding = False
              self.front_servo.stop()

        elif evt.key == K_SPACE:
            # pause/stop (space bar)
            if self.forwarding:
              self.forwarding = False
              self.front_servo.stop()
            self.front.set_pos(angle_limit_check(LIFT_ANGLE))
        
        elif evt.key == K_q:
          self.stop()

        # Hide robot position events
        elif evt.type==CKBOTPOSITION:
            return

        # Send events to JoyApp if not recognized
        JoyApp.onEvent(self,evt)

    def onStop(self):
        """
        Stops any plans that may be running
        """
        progress("P0App: onStop called")

#main function
if __name__=="__main__":
    app = P0App()
    app.run()
