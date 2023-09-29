import abb

def connectYumi():
    try: 
        yumi = abb.Robot()
        return yumi
    except:
        return None

def initialPos(robot):

    if robot != None:
        # get joints data
        print(robot.get_joints())
        print(robot.get_external_axis())

        #reset to initial pose
        robot.set_joints([0, 0, 0, 0, 0, 0])
        robot.set_external_axis(0)

        # get joints data
        print(robot.get_joints())
        print(robot.get_external_axis())

        #We get two times joints because we need to confirm the moving is done 
        #If they are not the same, then return False

        return True
    else:
        return False


