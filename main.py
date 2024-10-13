# Directory Maintainer
# Organizes the files within a directory
# Usage: python3 main.py [path/to/directory] [--log-window=N] [--size-threshold=M]
import argparse


def clean_directory(directory, log_window, size_threshold):
    # Implement the directory cleaning functionality here
    pass



# This code reads the command line arguments and passes them into the
# clean_directory function.
# It sets the defaults for the log window and the size threshold
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean up a messy data directory')
    parser.add_argument('directory', help='the directory to clean')
    parser.add_argument('--log-window',
            dest='log_window',
            default=30, # retain 30 log files by default
            type=int, 
            help='log retention policy: how many most recent log files to keep')
    parser.add_argument('--size-threshold',
            dest='size_threshold',
            default=50, # 50KB default
            type=int, 
            help='file size threshold: how large is a large text file')
    directory = parser.parse_args().directory
    log_window = parser.parse_args().log_window
    size_threshold = parser.parse_args().size_threshold

    clean_directory(directory, log_window, size_threshold)
