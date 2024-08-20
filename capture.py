import subprocess
def capture():
    # Command to capture an image using libcamera-jpeg
    command = "libcamera-jpeg --timeout 3000 -o capture.jpg"

    # Execute the command
    subprocess.run(command, shell=True)
# capture()