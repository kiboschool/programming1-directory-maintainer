# Directory Maintainer
# Organizes the files within a directory
# Usage: python3 main.py [path/to/directory] [--log-window=N] [--size-threshold=M]
import argparse


def clean_directory(directory, log_window, size_threshold):
    # Implement the directory cleaning functionality here
    pass



# You've been provided with the argument-handling code that reads the
# `directory`, `--log-window`, and `--size-threshold` values from the command line
# It calls the clean_directory function and passes in the values
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean up a messy data directory')
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
    log_window = parser.parse_args().log_window
    size_threshold = parser.parse_args().size_threshold

    clean_directory(directory, log_window, size_threshold)


