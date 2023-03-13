import subprocess
import time

# Run a Python script
# process = subprocess.Popen(['python3', '/home/orin2/PycharmProjects/CC_Face_Recognition_MVP02/flask_api_register.py'])

# Path to the script you want to run as sudo
script_path = "/home/orin2/PycharmProjects/CC_Face_Recognition_MVP02/flask_api_register.py"

# Command to run the script as sudo
cmd = ["sudo", "python3", script_path]
subprocess.call(cmd)
# Wait for a few seconds
time.sleep(20)

# Terminate the process
# process.terminate()

