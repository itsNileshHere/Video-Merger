import os
import subprocess
# import zipfile
import shutil

# Installing required packages
# print("Installing Dependencies...")
# subprocess.check_call(['pip', 'install', '-q', 'tqdm'])
# subprocess.check_call(['pip', 'install', '-q', 'gitpython'])

from tqdm import tqdm
# from git import Repo

script_directory = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_directory, "Input")
output_folder = os.path.join(script_directory, "Output")
temp_folder = os.path.join(script_directory, "Temp")
ffmpeg_folder = os.path.join(script_directory, "ffmpeg")
target_text_file = os.path.join(temp_folder, "list.txt")

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

output_index = 1
output_file = os.path.join(output_folder, "output.mp4")
while os.path.exists(output_file):
    output_index += 1
    output_file = os.path.join(output_folder, "output({}).mp4".format(output_index))

# Creating Temp folder, if not exists
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

file_names = os.listdir(input_folder) # Getting file names from Input Folder

# Creating list.txt file
# with open(target_text_file, "w") as f:
#     for file_name in file_names:
#         f.write("file ..//Input//'" + file_name + "'\n")

with open(target_text_file, "w") as f:
    for file_name in file_names:
        f.write("file '" + os.path.join(input_folder, file_name) + "'\n")



total_files = len(file_names)
print(target_text_file)
print(output_file)
ffmpeg_command = [
    ffmpeg_executable,
    "-f", "concat",
    "-safe", "0",
    "-i", target_text_file,
    "-c", "copy",
    output_file
]

# Progress bar
with tqdm(total=total_files, desc="Processing", ncols=100) as pbar:
    subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pbar.update(total_files)

# Removing Temp folder
shutil.rmtree(temp_folder)

print("\nScript Completed Successfully. Check Output folder.")
input("Press Enter to exit...")