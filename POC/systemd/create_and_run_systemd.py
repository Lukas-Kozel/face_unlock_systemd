#!/usr/bin/env python3
import os
import subprocess

def create_file(filepath):
    try:
        # Check if the script is running with root privileges
        if os.geteuid() != 0:
            print("This script requires root privileges. Please run it with 'sudo'.")
            return

        # Create and open the file with write permissions
        with open(filepath, 'w') as file:
            file.write("")
        
        print(f"File '{filepath}' created successfully with root privileges.")  

    except Exception as e:
        print(f"An error occurred: {e}")


def copy_text(source_file, destination_file):
    try:
        
        with open(source_file, 'r') as src:
            content = src.read()

        
        with open(destination_file, 'w') as dest:
            dest.write(content)
        
        print(f"Content successfully copied from {source_file} to {destination_file}")
    
    except FileNotFoundError:
        print(f"The file {source_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def start_service():
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'face_unlock.service'])
    subprocess.run(['sudo', 'systemctl', 'start', 'face_unlock.service'])
    

if __name__ == '__main__':
    create_file("/etc/systemd/system/face_unlock.service")
    source_file = 'face_unlock_systemd.service'       # Replace with your source file path
    destination_file = '/etc/systemd/system/face_unlock.service'  # Replace with your destination file path

    copy_text(source_file, destination_file)
    start_service()