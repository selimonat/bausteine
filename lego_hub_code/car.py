from pybricks.iodevices import XboxController
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import Car

# Set up all devices.
# front = Motor(Port.A, Direction.CLOCKWISE)
rear = Motor(Port.B, Direction.CLOCKWISE)
steer = Motor(Port.D, Direction.CLOCKWISE)
car = Car(steer, rear)
controller = XboxController()

# The main program starts here.
while True:
    # Steer with the right joystick.
    horizontal, _ = controller.joystick_right()

    # Drive using the trigger inputs.
    brake, acceleration = controller.triggers()

    car.drive_power(acceleration - brake)
    car.steer(-horizontal)