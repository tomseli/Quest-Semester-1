import odrive as odr
import odrive.pyfibre.fibre as fb
from odrive.enums import *
from odrive.config import *
import time
from defs import *

Vcc = 20    #[V]
Ampy = 2.5  #[A]
Vel = 10     #[turns/s]

odrv = odr.find_any(timeout=5)
print("ARNweb(TM) debug print: ", type(odrv))

print(str(odrv.vbus_voltage))

# time.sleep(1)

#THIS IS A FIX, DON'T GET ATTACHED
############################################################################
print("Erasing old config")
try:
    odrv.erase_configuration()
except :
    pass
time.sleep(3)

print("Rebooting")
try:
    odrv.reboot()
except :
    pass
time.sleep(3)
odrv = odr.find_any(timeout=5)
############################################################################

#SUPPLY CONFIG
############################################################################
odrv.config.dc_bus_overvoltage_trip_level = int(Vcc*1.2)
odrv.config.dc_max_positive_current = int(Ampy*0.8)
odrv.config.dc_max_negative_current = -0.01
odrv.axis0.config.motor.calibration_current = 10

print("Calibrating motor")
odrv.axis0.requested_state = AxisState.MOTOR_CALIBRATION
WAITFOR(odrv) # [wait for motor to calibrate]

odrv.config.brake_resistor0.resistance = 2
odrv.config.brake_resistor0.enable = True
odrv.clear_errors()
############################################################################


#MOTOR CONFIG
############################################################################
odrv.axis0.config.motor.motor_type = MotorType.HIGH_CURRENT
odrv.axis0.config.motor.pole_pairs = 7
odrv.axis0.config.motor.torque_constant = 8.27/270
odrv.axis0.config.motor.resistance_calib_max_voltage = Vcc*0.4
odrv.axis0.config.calibration_lockin.current = 10
# odr.utils.dump_errors(odrv)
# odrv.save_configuration()

odrv.axis0.motor.motor_thermistor.config.enabled = True
odrv.axis0.motor.motor_thermistor.config.r_ref = 10000
odrv.axis0.motor.motor_thermistor.config.beta = 3435
odrv.clear_errors()
# odrv.save_configuration()
#############################################################################


#LIMITS
############################################################################
odrv.axis0.config.motor.current_soft_max = 65
odrv.axis0.config.motor.current_hard_max = 85

odrv.axis0.controller.config.vel_limit = Vel

odrv.axis0.motor.motor_thermistor.config.temp_limit_lower = 110
odrv.axis0.motor.motor_thermistor.config.temp_limit_upper = 130

odrv.axis0.config.torque_soft_min = -0.3981851851851852
odrv.axis0.config.torque_soft_max = 0.3981851851851852
############################################################################


#ENCODER CONFIG
############################################################################
odrv.inc_encoder0.config.cpr = 20480
odrv.inc_encoder0.config.enabled = True
odrv.axis0.config.load_encoder = EncoderId.INC_ENCODER0
odrv.axis0.config.commutation_encoder = EncoderId.INC_ENCODER0
odrv.config.gpio10_mode = GpioMode.DIGITAL
odrv.axis0.commutation_mapper.config.use_index_gpio = True
odrv.axis0.commutation_mapper.config.index_gpio = 10
odrv.axis0.pos_vel_mapper.config.use_index_gpio = True
odrv.axis0.pos_vel_mapper.config.index_gpio = 10
odrv.axis0.pos_vel_mapper.config.index_offset = 0
odrv.axis0.pos_vel_mapper.config.index_offset_valid = True
odrv.axis0.config.load_encoder = EncoderId.INC_ENCODER0
odrv.axis0.config.commutation_encoder = EncoderId.INC_ENCODER0
############################################################################

#CONTROL-MODE SETUP
############################################################################
# VELOCITY(odrv, Vel)
############################################################################


#CALIBRATION
############################################################################
print("Saving config")
try:
    odrv.save_configuration()
except :
    pass
time.sleep(3) # [wait for ODrive to reboot]
odrv = odr.find_any(timeout=5)

print("Index search Encoder")
odrv.axis0.requested_state = AxisState.ENCODER_INDEX_SEARCH
WAITFOR(odrv) # [wait for motor to stop]
print("Encoder offset calibration")
odrv.axis0.requested_state = AxisState.ENCODER_OFFSET_CALIBRATION
WAITFOR(odrv) # [wait for motor to stop]

print("Saving config")
try:
    odrv.save_configuration()
except :
    pass
time.sleep(3) # [wait for ODrive to reboot]
odrv = odr.find_any(timeout=5)

print("Index search Encoder")
odrv.axis0.requested_state = AxisState.ENCODER_INDEX_SEARCH
WAITFOR(odrv) # [wait for motor to stop]
# print(odr.connected_devices)
############################################################################

#CONTROL-MODE
############################################################################
# VELOCITY(odrv,Vel)
VELOCITY_RAMPED(odrv, Vel, 1.5)
# WAITFOR(odrv)
# time.sleep(5)
# odrv.axis0.controller.input_vel = Vel
odr.utils.dump_errors(odrv)

# print(odrv.axis0.current_state)
while(1):
    time.sleep(3)
    print("Velocity:",odrv.encoder_estimator0.vel_estimate)
    print("Current:",odrv.ibus)
    print("Voltage",odrv.vbus_voltage)
############################################################################

# """