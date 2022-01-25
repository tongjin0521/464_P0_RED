'''
FILE demo-helloJoy.py

This demonstrates basic joyapp programming and it converts your mouse postion to y-value and prints it on your screen
'''
from joy.decl import *
from joy import JoyApp

class HelloJoyApp( JoyApp ):
  """HelloJoyApp

     The "hello world" of JoyApp programming.
     This JoyApp pipes the y coordinate of mouse positions (while left
     button is pressed) to a specified setter. By default this setter is
     given by "#output " -- i.e. it is a debug message.

     See JoyApp.setterOf() for a specification of possible outputs

     This file is intended to introduce you to our joy library
  """
  def __init__(self,robot = dict(count=3),*arg,**kw):

    JoyApp.__init__(self,robot = robot, *arg,**kw)

  def onStart(self):
    progress("Start")

  def onStop(self):
    progress("Stop")

  def angle_limit_check(input_angle):
    if (input_angle > 9700 ):
      proocess("---------------------------")
      process("WARNING: ANGLE LIMIT ACHIEVEDC")
      proocess("---------------------------")
      return 9700
    elif (input_angle < -9700):
      proocess("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      process("WARNING: ANGLE LIMIT ACHIEVEDC")
      proocess("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return -9700
    else:
      return input_angle
  
  def onEvent(self,evt):
    progress("----------")
    # nx17_pos = self.robot.at.Nx17.get_pos()
    # nx10_pos = self.robot.at.Nx10.get_pos()
    # progress("10 pos: "+str(nx10_pos))
    # progress("17 pos: "+str(nx17_pos))
    # progress(str(evt.type) +str(evt.key))
    if (evt.type == KEYDOWN):
      # keyboard input
      if (evt.key == K_w ):
        self.robot.at.Nx10.set_pos(2500)
        self.robot.at.Nx17.set_pos(2500)
      elif (evt.key == K_s):
        self.robot.at.Nx10.set_pos(-2500)
        self.robot.at.Nx17.set_pos(-2500)
      elif (evt.key == K_LEFTBRACKET):
        # "[" to stop
        self.stop()
      

if __name__=="__main__":
  app = HelloJoyApp(robot=dict(count=2))
  app.run()
