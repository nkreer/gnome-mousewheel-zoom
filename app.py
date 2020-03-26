import subprocess

# Define gsettings commands for retrieving and setting a new magnification level
command_get = "gsettings get org.gnome.desktop.a11y.magnifier mag-factor"
command_set = "gsettings set org.gnome.desktop.a11y.magnifier mag-factor"

# Get the current magnification factor from GNOME
# Cast it to float for further processing
current_mag_factor = float(subprocess.Popen(command_get, shell=True, stdout=subprocess.PIPE).stdout.read())

print(current_mag_factor)

