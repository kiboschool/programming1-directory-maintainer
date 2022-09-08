# Directory Maintainer
# Organizes the files within a directory
# Usage: python3 main.py [path/to/directory] [--log-window=N] [--size-threshold=M]
import argparse
import os


def clean_directory(directory, log_window, size_threshold):
    # get list of files
    files = os.listdir(directory)

    # make directories
    csv_path = os.path.join(directory, "csv") 
    log_path = os.path.join(directory, "log") 
    txt_path = os.path.join(directory, "txt") 
    lg_txt_path = os.path.join(txt_path, "large_txt_files") 
    os.mkdir(csv_path)
    os.mkdir(log_path)
    os.mkdir(txt_path)
    os.mkdir(lg_txt_path)

    logs = []
    for file in files:
        _, ext = os.path.splitext(file)
        current_path = os.path.join(directory, file) 

        # handle csvs
        if ext == ".csv":
            new_path = os.path.join(csv_path, file)
            os.rename(current_path, new_path)

        # keep logs for later
        elif ext == ".log":
            logs.append(file)

        # handle txt files
        elif ext == ".txt":
            if os.path.getsize(current_path)/1000 > size_threshold:
                new_path = os.path.join(lg_txt_path, file)
            else:
                new_path = os.path.join(txt_path, file)
            os.rename(current_path, new_path)

        # handle other kinds of files with a warning
        else:
            print("Unknown extension: ", file)

    # handle logs
    ordered_logs = sorted(logs)
    for i in range(len(logs)):
        current_path = os.path.join(directory, ordered_logs[i])
        if i < log_window:
            new_path = os.path.join(log_path, ordered_logs[i])
            os.rename(current_path, new_path)
        else:
            os.remove(current_path)


# You've been provided with the argument-handling code that reads the
# `directory`, `--log-window`, and `--size-threshold` values from the command line
# It calls the clean_directory function and passes in the values
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
