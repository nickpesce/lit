#DO NOT CHANGE THESE#
SPEED = 0b10        #
COLOR = 0b1         #
NONE = 0b0          #
#####################

#This is what will appear in all interfaces
name = "Christmas Lights"

#This is what the user will see after the effect starts
start_string = name + " started!"

#This is what will appear in tips and help menus
description = "Colors of traditional colored christmas lights"

#This defines which additional arguments this effect can take.
#Combine multiple options with a '|'
modifiers = NONE

#This is the function that controls the effect. Look at the included effects for examples.
#Params:
#   lights: A reference to the light controls (the only way to make anything happen).
#   stop_event: A threading event that allows this effect to be stopped by the parent.
#   color: The color if passed, otherwise the default color. REMOVE IF COLOR IS NOT A MODIFIER.
#   speed: The speed multiplier if passed, otherwise the default speed. REMOVE IF SPEED IS NOT A MODIFIER.
#   **extras: Any other parameters that may have been passed. Do not use, but do not remove.
def start(lights, stop_event, **extras):
    lights.set_all_other_pixels(0, 0, 0)

    for i, n in lights.all_lights_with_count():
        seq = n%5
        if seq == 0:
            lights.set_pixel(i, 100, 0, 0)
        elif seq == 1:
            lights.set_pixel(i, 100, 0, 50)
        elif seq == 2:
            lights.set_pixel(i, 0, 100, 0)
        elif seq == 3:
            lights.set_pixel(i, 150, 100, 0)
        elif seq == 4:
            lights.set_pixel(i, 0, 0, 100)
    lights.show()