import os
import subprocess
import shutil
import sys
import time

script_directory = os.path.dirname(os.path.abspath(__file__))
dependencies_folder = os.path.join(script_directory, "dist")
os.environ["PATH"] += os.pathsep + dependencies_folder

input_folder = os.path.join(script_directory, "Input")
output_folder = os.path.join(script_directory, "Output")
temp_folder = os.path.join(script_directory, "Temp")
ffmpeg_folder = os.path.join(script_directory, "ffmpeg")
target_text_file = os.path.join(temp_folder, "list.txt")

# Check if the input folder is empty
file_names = os.listdir(input_folder)
if not file_names:
    print("Input folder is empty. Nothing to process.")
    exit(0)

print("Starting Script — ")
is_windows = os.name == "nt"
is_linux = os.name == "posix"

if is_windows:
    print("Windows OS Detected...\nExecuting Script based on that...")
else:
    print("Linux OS Detected...\nChecking if ffmpeg is installed...")

# Check if FFmpeg is installed on Linux
ffmpeg_installed = False
if is_linux:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        ffmpeg_installed = True
    except subprocess.CalledProcessError:
        pass

if not is_windows and not ffmpeg_installed:
    print("FFmpeg is not installed on your Linux system.")
    print("You can install FFmpeg by running the following command:")
    print("sudo apt-get install ffmpeg")
    exit(1)

# Determine the FFmpeg executable based on the OS
if is_windows:
    ffmpeg_executable = os.path.join(ffmpeg_folder, "ffmpeg.exe")
else:
    ffmpeg_executable = "ffmpeg"

try:
    output_index = 1
    output_file = os.path.join(output_folder, "output.mp4")
    while os.path.exists(output_file):
        output_index += 1
        output_file = os.path.join(output_folder, f"output({output_index}).mp4")

    # Creating Temp folder, if not exists
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Write the file list with proper escaping
    with open(target_text_file, "w", encoding='utf-8') as f:
        for file_name in sorted(file_names):
            file_path = os.path.join(input_folder, file_name)
            # Escape the path for FFmpeg
            escaped_path = file_path.replace("\\", "/")
            escaped_path = escaped_path.replace("'", "'\\''")
            f.write(f"file '{escaped_path}'\n")

    ffmpeg_command = [
        ffmpeg_executable,
        "-f", "concat",
        "-safe", "0",
        "-i", target_text_file,
        "-c", "copy",
        output_file
    ]

    process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print("Processing", end="", flush=True)
    dots = 0
    while process.poll() is None:
        dots = (dots % 3) + 1
        sys.stdout.write('\r' + 'Processing' + '.' * dots + ' ' * (3 - dots))
        sys.stdout.flush()
        time.sleep(0.5)

    process.wait()

    if process.returncode != 0:
        stderr_output = process.stderr.read().decode('utf-8', errors='replace')
        raise subprocess.CalledProcessError(process.returncode, ffmpeg_command, stderr_output)

    print("\nProcessing completed!")

except Exception as e:
    print("\nAn error occurred:", str(e))

finally:
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

print("\nScript Completed Successfully. Check Output folder.")