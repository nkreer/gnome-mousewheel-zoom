import subprocess, os
import mouse

# Define gsettings commands for retrieving and setting a new magnification level
command_get = "gsettings get org.gnome.desktop.a11y.magnifier mag-factor"
command_set = "gsettings set org.gnome.desktop.a11y.magnifier mag-factor"


# Get the current magnification factor from GNOME
# Cast it to float for further processing
def get_current_mag_factor():
    return float(subprocess.Popen(command_get, shell=True, stdout=subprocess.PIPE).stdout.read())


global current_mag_factor
current_mag_factor = get_current_mag_factor()


# Hook mouse events and react to scrolling
def mouse_hook_listener(event):
    global current_mag_factor
    if isinstance(event, mouse.WheelEvent):

        if event.delta > 0:
            current_mag_factor += 0.1
        elif event.delta < 0:
            current_mag_factor -= 0.1

        # Cannot possibly go lower than magnification factor 1 (no magnification
        if current_mag_factor < 1:
            return

        # GNOME limits magnification precision to two decimal points
        current_mag_factor = round(current_mag_factor, 2)

        final_setter_command = command_set + " " + str(current_mag_factor)
        print(final_setter_command)

mouse.hook(mouse_hook_listener)

# Keep it running
while True:
    pass
