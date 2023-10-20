#functions: move robot arm position
stepDistance = 10

def MoveRobotArm_Up(laser_pos):
    global stepDistance
    laser_pos = laser_pos + stepDistance 
    return laser_pos

def MoveRobotArm_Down(laser_pos):
    global stepDistance
    laser_pos = laser_pos - stepDistance 
    return laser_pos