from pybricks.iodevices import XboxController
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import Car

# Set up all devices.
rear = Motor(Port.B, Direction.CLOCKWISE)
steer = Motor(Port.D, Direction.CLOCKWISE)
car = Car(steer, rear)
controller = XboxController()

# The main program starts here.
while True:
    # Steer with the right joystick.
    horizontal, _ = controller.joystick_right()

    # Read the triggers.
    brake_trigger, accel_trigger = controller.triggers()

    # Read the left joystick vertical axis.
    _, vertical_left = controller.joystick_left()  # up = -100, down = +100

    # Apply drive and steering.
    car.drive_power(vertical_left - brake_trigger + accel_trigger)
    car.steer(-horizontal)
