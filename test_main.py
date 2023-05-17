import io
import logging
import os
from os import path
import subprocess
from shutil import rmtree
from tempfile import mkdtemp
from unittest.mock import patch
from unittest import TestCase
import unittest

ONE_KB = 1024  # bytes


class TestDirectoryMaintainer(TestCase):

    def setUp(self):
        # create test directory
        self.test_directory = mkdtemp(suffix='_kibo_tests')
        self.dir_maintainer_dir = os.path.dirname(__file__)
        self.dir_maintainer_file = os.path.join(self.dir_maintainer_dir, 'main.py')
        print(self.test_directory)

    def tearDown(self):
        # delete test directory
        rmtree(self.test_directory)

    def _create_files(self, destination_path, file_list):
        assert isinstance(destination_path, str)
        assert isinstance(file_list, list)
        assert all([isinstance(filename, str) and isinstance(filesize, float) and os.sep not in filename
                   for filename, filesize in file_list])

        for filename, file_size in file_list:
            full_file_path = os.path.join(self.test_directory, filename)
            with open(full_file_path, 'w') as outfile:
                final_filesize = max(int(file_size * ONE_KB), 0)
                outfile.write('a' * final_filesize)

    def _run_dir_maintainer(self, log_window=None, size_threshold=None):
        python_exec = ['python3']
        log_window_arg = ['--log-window', str(log_window)] if log_window else []
        size_threshold_arg = ['--size-threshold', str(size_threshold)] if size_threshold else []
        cmd  = python_exec + [self.dir_maintainer_file] + log_window_arg + size_threshold_arg + [self.test_directory] 

        print(cmd)
        subprocess.run(cmd)

    def test_csv_files_are_moved(self):
        file_list = [
          # ('file_name', file_size(kb))
            ('file1.csv', 1.),
            ('file2.csv', 2.),
            ('file3.csv', 0.5),
            ('file4.csv', 0.1),
        ]
        self._create_files(self.test_directory, file_list)
        self._run_dir_maintainer()
        self.assertTrue(path.isdir(path.join(self.test_directory, 'csv')))
        for filename, filesize in file_list:
            self.assertTrue(path.exists(path.join(self.test_directory, 'csv', filename)))


    def test_txt_files_are_moved(self):
        file_list = [
          # ('file_name', file_size(kb))
            ('file1.txt', 1.),
            ('file2.txt', 2.),
            ('file3.txt', 0.5),
            ('file4.txt', 0.1),
        ]
        self._create_files(self.test_directory, file_list)
        self._run_dir_maintainer()
        self.assertTrue(path.isdir(path.join(self.test_directory, 'txt')))
        for filename, filesize in file_list:
            self.assertTrue(path.exists(path.join(self.test_directory, 'txt', filename)))

    def test_large_txt_files_are_identified(self):
        pass

    def test_log_files_are_moved(self):
        file_list = [
          # ('file_name', file_size(kb))
            ('file1.log', 1.),
            ('file2.log', 2.),
            ('file3.log', 0.5),
            ('file4.log', 0.1),
        ]
        self._create_files(self.test_directory, file_list)
        self._run_dir_maintainer()
        self.assertTrue(path.isdir(path.join(self.test_directory, 'log')))
        for filename, filesize in file_list:
            self.assertTrue(path.exists(path.join(self.test_directory, 'log', filename)))

    def test_log_files_log_window_honoured(self):
        file_list = [
          # ('file_name', file_size(kb))
            ('20230110file1.log', 1.),
            ('20230111file2.log', 2.),
            ('20230112file3.log', 0.5),
            ('20230113file4.log', 0.1),
        ]
        self._create_files(self.test_directory, file_list)
        self._run_dir_maintainer(log_window=3)
        self.assertTrue(path.isdir(path.join(self.test_directory, 'log')))
        for i, (filename, filesize) in enumerate(file_list):
            print(i)
            if i == 0:
                self.assertFalse(path.exists(path.join(self.test_directory, 'log', filename)))
            else:
                self.assertTrue(path.exists(path.join(self.test_directory, 'log', filename)))

    def test_log_files_fewer_files_than_log_window_handled(self):
        file_list = [
          # ('file_name', file_size(kb))
            ('20230110file1.log', 1.),
            ('20230111file2.log', 2.),
            ('20230112file3.log', 0.5),
            ('20230113file4.log', 0.1),
        ]
        self._create_files(self.test_directory, file_list)
        self._run_dir_maintainer(log_window=31)
        self.assertTrue(path.isdir(path.join(self.test_directory, 'log')))
        for filename, filesize in file_list:
            self.assertTrue(path.exists(path.join(self.test_directory, 'log', filename)))

    def test_files_moved_and_not_copied(self):
        file_list = [
          # ('file_name', file_size(kb))
            ('20230110file1.log', 1.),
            ('20230111file2.log', 2.),
            ('20230112file3.log', 0.5),
            ('20230113file4.log', 0.1),
            ('file1.txt', 1.),
            ('file2.csv', 2.),
            ('file9.txt', 0.5),
            ('file4.txt', 0.1),
        ]
        self._create_files(self.test_directory, file_list)
        for filename, filesize in file_list:
            self.assertTrue(path.exists(path.join(self.test_directory, filename)))
        self._run_dir_maintainer()
        self.assertTrue(path.isdir(path.join(self.test_directory, 'log')))
        for filename, filesize in file_list:
            self.assertFalse(path.exists(path.join(self.test_directory, filename)))

    def test_unknown_file_extensions_left_untouched(self):
        valid_extensions_file_list = [
          # ('file_name', file_size(kb))
            ('file1.log', 1.),
            ('file2.txt', 2.),
            ('file3.csv', 0.5),
            ]
        invalid_extensions_file_list = [
          # ('file_name', file_size(kb))
            ('file1.pdf', 1.),
            ('file2.png', 2.),
            ('file3.xlsx', 0.5),
            ]

        file_list = valid_extensions_file_list + invalid_extensions_file_list
        self._create_files(self.test_directory, file_list)
        self._run_dir_maintainer()
        for filename, filesize in valid_extensions_file_list:
            file_ext = filename.split('.')[-1]
            self.assertTrue(path.exists(path.join(self.test_directory, file_ext, filename)))
            self.assertFalse(path.exists(path.join(self.test_directory, filename)))

        for filename, filesize in invalid_extensions_file_list:
            file_ext = filename.split('.')[-1]
            self.assertTrue(path.exists(path.join(self.test_directory, filename)))


if __name__ == '__main__':
    unittest.main()
