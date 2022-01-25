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
    self.nx1E_pos = self.robot.at.Nx1E.get_pos()
    # self.nx10_pos = self.robot.at.Nx10.get_pos()
    # self.1E_keep_moving = False


  def onStart(self):
    progress("Start")

  def onStop(self):
    progress("Stop")

  def angle_limit_check(self,input_angle):
    if (input_angle > 9700 ):
      progress("---------------------------")
      progress("WARNING: ANGLE LIMIT ACHIEVEDC")
      progress("---------------------------")
      return 9700
    elif (input_angle < -9700):
      progress("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      progress("WARNING: ANGLE LIMIT ACHIEVEDC")
      progress("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return -9700
    else:
      return input_angle
  
  def onEvent(self,evt):
    progress("----------")
    # progress("10 pos: "+str(self.nx10_pos))
    # progress("1E pos: "+str(self.nx1E_pos))
    if (evt.type == KEYDOWN):
      # keyboard input
      print(str(evt.key))
      if (evt.key == K_q ):
        self.robot.at.Nx1E.set_pos(-3788)
        self.robot.at.Nx1E.set_pos(4212)
      elif (evt.key == K_w):
        self.robot.at.Nx1E.set_pos(-3788)
      elif (evt.key == K_s):
        self.robot.at.Nx1E.set_pos(4212)
      elif (evt.key == K_LEFTBRACKET):
        # "[" to stop
        self.stop()
      else:
        pass
      

if __name__=="__main__":
  app = HelloJoyApp(robot=dict(count=1))
  app.run()
