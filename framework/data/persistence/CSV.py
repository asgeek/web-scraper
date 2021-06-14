import csv
import os
import time
from framework.util.project.Project import Project
from framework.util.logger.Log import Log
from enum import Enum


class SourceType(Enum):
    INPUT = 'input'
    OUTPUT = 'output'


class CSV:
    file_name = ''
    fq_file_name = ''

    def __init__(self, file_name, source_type):
        self.file_name = file_name
        self.set_fq_file_name(file_name, source_type)

    def set_fq_file_name(self, file_name, source_type):
        if source_type is SourceType.INPUT:
            self.fq_file_name = Project.INPUT + file_name + ".csv"
        elif source_type is SourceType.OUTPUT:
            self.fq_file_name = Project.OUTPUT + file_name + ".csv"

    def create_new(self):
        Log.info("Creating new CSV file {0} ...".format(self.fq_file_name))
        try:
            with open(self.fq_file_name, 'w'):
                pass
        except PermissionError as excep:
            Log.fatal("Exception {0}".format(excep))
            exit(1)

    def create_new_and_backup_old(self):
        if os.path.exists(self.fq_file_name):
            self.backup_old_file()
        self.create_new()

    def create_new_if_not_exist(self):
        if os.path.exists(self.fq_file_name):
            Log.info("{0} file already exists!".format(self.fq_file_name))
            Log.info("No need to create new file!")
        else:
            self.create_new()

    def set_header(self, value_set):
        if os.path.exists(self.fq_file_name):
            Log.info('Writing header to {0} ...'.format(self.fq_file_name))
            try:
                with open(self.fq_file_name, 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(value_set)
            except PermissionError as excep:
                Log.fatal("Exception {0}".format(excep))
                exit(1)
        else:
            Log.fatal("{0} file does not exist!".format(self.fq_file_name))
            Log.fatal("Cannot write to the file {0}".format(self.fq_file_name))
            exit(1)

    def append_array(self, value_set):
        if os.path.exists(self.fq_file_name):
            Log.info('Writing data to {0} ...'.format(self.fq_file_name))
            try:
                with open(self.fq_file_name, 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(value_set)
            except PermissionError as excep:
                Log.fatal("Exception {0}".format(excep))
                exit(1)
        else:
            Log.fatal("{0} file does not exist!".format(self.fq_file_name))
            Log.fatal("Cannot write to the file {0}".format(self.fq_file_name))
            exit(1)

    def append_dict(self, dict):
        if os.path.exists(self.fq_file_name):
            Log.info('Writing data to {0} ...'.format(self.fq_file_name))
            try:
                with open(self.fq_file_name, 'a', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, dict.keys())
                    writer.writerow(dict)
            except PermissionError as excep:
                Log.fatal("Exception {0}".format(excep))
                exit(1)
        else:
            Log.fatal("{0} file does not exist!".format(self.fq_file_name))
            Log.fatal("Cannot write to the file {0}".format(self.fq_file_name))
            exit(1)

    def read_file(self):
        if os.path.exists(self.fq_file_name):
            Log.info('Reading data from {0} ...'.format(self.fq_file_name))
            columns = self.read_header()
            try:
                first_line = True
                with open(self.fq_file_name, 'r') as csv_file:
                    reader = csv.DictReader(csv_file, columns)
                    for row in reader:
                        if first_line:
                            first_line = False
                            Log.debug("Header line skipped from CSV")
                            pass
                        else:
                            diction = dict(row)
                            yield diction

            except PermissionError as excep:
                Log.fatal("Exception {0}".format(excep))
                exit(1)
        else:
            Log.fatal("{0} file does not exist!".format(self.fq_file_name))
            Log.fatal("Cannot read the file {0}".format(self.fq_file_name))
            exit(1)

    def read_header(self):
        if os.path.exists(self.fq_file_name):
            Log.info('Reading header from {0} ...'.format(self.fq_file_name))
            try:
                with open(self.fq_file_name, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    return next(reader)
            except PermissionError as excep:
                Log.fatal("Exception {0}".format(excep))
                exit(1)
        else:
            Log.fatal("{0} file does not exist!".format(self.fq_file_name))
            Log.fatal("Cannot read the file {0}".format(self.fq_file_name))
            exit(1)

    def backup_old_file(self):
        file_time = os.path.getmtime(self.fq_file_name)
        time_tuple = time.gmtime(file_time)
        time_list = list(time_tuple)
        backup_file_name = self.file_name + "_{0}{1}{2}{3}{4}{5}".format(time_list[0], time_list[1], time_list[2],
                                                                         time_list[3], time_list[4], time_list[5])
        fq_backup_file_name = Project.OUTPUT + backup_file_name + ".csv"
        Log.info("Backup existing CSV file as {0}".format(fq_backup_file_name))
        try:
            os.rename(self.fq_file_name, fq_backup_file_name)
        except PermissionError as excep:
            Log.fatal("Exception {0}".format(excep))
            exit(1)
