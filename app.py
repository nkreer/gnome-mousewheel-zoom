from pynput.mouse import Listener
import os, sys

# Perhaps some user configuration?
min_zoom_factor = 1.0 # zoom off, recommended
max_zoom_factor = 4.0

global executing_user
executing_user = sys.argv[1]

# Define gsettings commands for retrieving and setting a new magnification level
command_get = "gsettings get org.gnome.desktop.a11y.magnifier mag-factor"
command_set = "gsettings set org.gnome.desktop.a11y.magnifier mag-factor"


# Return the magnification factor reported by gsettings
def get_mag_factor():
    global executing_user
    return float(os.popen(command_get).read())


global current_mag_factor
current_mag_factor = get_mag_factor()
print(current_mag_factor)


# Hook mouse events and react to scrolling
def scroll_hook_listener(x, y, dx, dy):
    global current_mag_factor
    global executing_user

    # Respond to the direction of movement accordingly
    if dy > 0:
        current_mag_factor += 0.1
    elif dy < 0:
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
    final_change_command = command_set + " " + str(current_mag_factor)
    print(final_change_command)
    print(os.popen(final_change_command).read())


# Register the listener with pynput
with Listener(on_scroll=scroll_hook_listener) as listener:
    print("listener activated")
    listener.join()

# Keep it running
while True:
    pass
