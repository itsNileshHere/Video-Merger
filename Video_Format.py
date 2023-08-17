import os
import subprocess

script_directory = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_directory, "Input")
output_folder = os.path.join(script_directory, "Output")
ffmpeg_folder = os.path.join(script_directory, "ffmpeg")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# List all files in the input folder
input_files = os.listdir(input_folder)
input_files = [f for f in input_files if f.endswith('.ts')]

if not input_files:
    print("No .ts files found in the input folder.")
    exit(1)

# Detect the operating system
is_windows = os.name == "nt"
is_linux = os.name == "posix"

print("Starting Script — ")
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


print("Select the desired output format:")
print("1. MP4")
print("2. MKV")

choice = input("Enter the corresponding number: ")

if choice == "1":
    output_format = "mp4"
elif choice == "2":
    output_format = "mkv"
else:
    print("Invalid choice.")
    exit(1)

for input_file in input_files:
    input_path = os.path.join(input_folder, input_file)
    output_file = os.path.splitext(input_file)[0] + "." + output_format
    output_path = os.path.join(output_folder, output_file)

    ffmpeg_command = [
        ffmpeg_executable,
        "-i", input_path,
        "-c:v", "copy",
        "-c:a", "copy",
        output_path
    ]

    subprocess.run(ffmpeg_command)

    print(f"Converted {input_file} to {output_file}")

print("Conversion complete.")
