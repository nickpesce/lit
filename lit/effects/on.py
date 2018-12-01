#DO NOT CHANGE THESE#
SPEED = 0b10        #
COLOR = 0b1         #
NONE = 0b0          #
#####################

#This is what will appear in all interfaces
name = "On"

#This is what the user will see after the effect starts
start_string = "The lights have been turned on!"

#This is what will appear in tips and help menus
description = "Turns all of the lights on to a specfied color"

#This defines which additional arguments this effect can take.
#Combine multiple options with a '|'
modifiers = COLOR

#This is the function that controls the effect. Look at the included effects for examples.
#Params:
#   lights: A reference to the light controls (the only way to make anything happen).
#   stop_event: A threading event that allows this effect to be stopped by the parent.
#   color: The color if passed, otherwise the default color. REMOVE IF COLOR IS NOT A MODIFIER.
#   speed: The speed multiplier if passed, otherwise the default speed. REMOVE IF SPEED IS NOT A MODIFIER.
#   **extras: Any other parameters that may have been passed. Do not use, but do not remove.
def update(lights, stop_event, color = [255, 255, 255], **extras):
    lights.set_all_pixels(color[0], color[1], color[2])
    lights.show()
