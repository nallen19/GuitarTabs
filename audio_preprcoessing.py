import os
import subprocess

def convert_to_wav(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_file]
    subprocess.run(command, check=True)

def process_file(file_name, input_dir, output_dir, license_key, separate):
    full_input_path = os.path.join(input_dir, file_name)
    full_output_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + '.wav')

    if separate:
        # File that requires separation, process with lalalai_splitter
        parts = file_name.rsplit('_', 1)
        stem = parts[0]
        subprocess.run([
            'python3', 'lalalai_splitter.py',
            '--input', full_input_path,
            '--license', license_key,
            '--output', output_dir,
            '--stem', stem,
        ], check=True)
    else:
        # Directly convert mp3 to wav
        convert_to_wav(full_input_path, full_output_path)

input_separate_dir = './Input/Audio/Separation'
input_nonseparate_dir = './Input/Audio/NonSeparation'
output_dir = './Output'
license_key = 'e785344ccf324f0a'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each file in the input directory
for file_name in os.listdir(input_separate_dir):
    if file_name.endswith('.mp3'):
        process_file(file_name, input_separate_dir, output_dir, license_key, True)
for file_name in os.listdir(input_nonseparate_dir):
    if file_name.endswith('.mp3'):
        process_file(file_name, input_nonseparate_dir, output_dir, license_key, False)
