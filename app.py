import mouse
import os, sys

# Perhaps some user configuration?
min_zoom_factor = 1.0 # zoom off, recommended
max_zoom_factor = 4.0

global executing_user
executing_user = sys.argv[1]

# Define gsettings commands for retrieving and setting a new magnification level
command_get = "gsettings get org.gnome.desktop.a11y.magnifier mag-factor"
command_set = "gsettings set org.gnome.desktop.a11y.magnifier mag-factor"


# Assemble a command to be run as the user even though we are root
def assemble_user_command(command, user):
    return 'sudo -u "' + user + '" dbus-launch --exit-with-session ' + command 


# Return the magnification factor reported by gsettings
def get_mag_factor():
    global executing_user
    return float(os.popen(assemble_user_command(command_get, executing_user)).read())


global current_mag_factor
current_mag_factor = get_mag_factor()
print(current_mag_factor)


# Hook mouse events and react to scrolling
def mouse_hook_listener(event):
    global current_mag_factor
    global executing_user

    # Only ever react to mousewheel changes
    if isinstance(event, mouse.WheelEvent):

        # Respond to the direction of movement accordingly
        if event.delta > 0:
            current_mag_factor += 0.1
        elif event.delta < 0:
            current_mag_factor -= 0.1

        # Cannot possibly go lower than minimum
        if current_mag_factor < min_zoom_factor:
            current_mag_factor = min_zoom_factor
            return
    
        # Respect the maximum zoom factor
        if current_mag_factor > max_zoom_factor:
            current_mag_factor = max_zoom_factor
            return

        # GNOME limits magnification precision to two decimal points
        current_mag_factor = round(current_mag_factor, 2)

        # Assemble the command to change the zoom factor & execute
        final_change_command = assemble_user_command(command_set + " " + str(current_mag_factor), executing_user)
        print(final_change_command)
        print(os.popen(final_change_command).read())


mouse.hook(mouse_hook_listener)

# Keep it running
while True:
    pass
