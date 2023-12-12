import odrive as odr
import time as tm
from odrive.enums import *

def WAITFOR(odrv):
    while(odrv.axis0.procedure_result == ProcedureResult.BUSY):
        tm.sleep(0.5)
    odr.utils.dump_errors(odrv)

#VELOCITY-CONTROL SETUP
############################################################################
def VELOCITY(odrv, Vel):
    print("Entering VELOCITY_CONTROL")
    odrv.axis0.controller.config.input_mode = InputMode.PASSTHROUGH
    odrv.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
    odrv.axis0.controller.config.enable_vel_limit = True
    odrv.axis0.controller.config.vel_limit = int(Vel+5)
    odrv.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
    WAITFOR(odrv)
    odrv.axis0.controller.input_vel = Vel
############################################################################

#RAMPED-VELOCITY-CONTROL SETUP
############################################################################
def VELOCITY_RAMPED(odrv, Vel, Acc):
    print("Entering VELOCITY_CONTROL")
    odrv.axis0.controller.config.input_mode = InputMode.VEL_RAMP
    odrv.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
    odrv.axis0.controller.config.enable_vel_limit = True
    odrv.axis0.controller.config.vel_limit = int(Vel+5)
    odrv.axis0.controller.config.vel_ramp_rate = Acc
    odrv.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
    WAITFOR(odrv)
    odrv.axis0.controller.input_vel = Vel
############################################################################
