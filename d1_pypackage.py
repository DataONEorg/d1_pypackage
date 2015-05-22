#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
# Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
:Synopsis:
  This is an example on how to use the DataONE Client Library to retrieve a data package on your system. It
  shows how to:

  - Download a Resource Map (Data Package)
  - Parse and display the Resource Map on local system.
  - Remove data package from system

:Author:
  USGS (Brandon Serna)

:Created:
  2015-02-06

:Requires:
  - Python 2.7
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
"""
# Stdlib.
import logging
import os
import shutil
import re

# 3rd party.
# import pyxb
import bagit

# DataOne.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.const
import d1_client.data_package
import d1_client.mnclient

# Import GUI function
from pypackage_gui import *

# Import file system in user space function
from fuse import sshfs_mount

# Config.

# The identifier (PID) of the DataONE Data Package (Resource Map) to download
# and display. Data packages have Format ID
# http://www.openarchives.org/ore/terms.
# Original variable to declare if GUI not in use.
# SCIENCE_OBJECT_PID = 'dakoop_test-PKG'

# BaseURL for the Member Node on which the science object resides. If the script
# is run on the same server as the Member Node, this can be localhost.
# MN_BASE_URL = 'https://mn-demo-6.test.dataone.org/knb/d1/mn'

MN_BASE_URL = 'https://mn-demo-6.test.dataone.org/knb/d1/mn'

# MN_BASE_URL = 'https://localhost/mn'

# Paths to the certificate and key to use when retrieving the object. This is
# required if the object is not publicly accessible. If the certificate has the
# key embedded, the _KEY setting should be set to None. If the objects have
# public access, these can both be set to None.
CERTIFICATE_FOR_CREATE = None
CERTIFICATE_FOR_CREATE_KEY = None

# Variable to hold the parents directory path.
msg = ''

# Create a Member Node client that can be used for running commands against
# a specific Member Node.
client = d1_client.mnclient.MemberNodeClient(MN_BASE_URL,
                                             cert_path=CERTIFICATE_FOR_CREATE,
                                             key_path=CERTIFICATE_FOR_CREATE_KEY)

# Use the client to get a data package as a string (Format ID
# http://www.openarchives.org/ore/terms).
# Variable commented out for GUI encapsulation.
# resource_map_xml = client.get(SCIENCE_OBJECT_PID).read()

# Create a resource map parser.
# Variable commented out for GUI encapsulation.
# resource_map_parser = d1_client.data_package.ResourceMapParser(resource_map_xml)


# Create data_package class
class Usgs_Data_Pkg:
    # Create a Member Node client that can be used for running commands against
    # a specific Member Node.
    client = d1_client.mnclient.MemberNodeClient(MN_BASE_URL,
                                                 cert_path=CERTIFICATE_FOR_CREATE,
                                                 key_path=CERTIFICATE_FOR_CREATE_KEY)

    # Testing PID title and reassigning to science_object_pid
    pid_title = 'dakoop_test-PKG'
    science_object_pid = pid_title

    # global resource_map_xml
    resource_map_xml = client.get(science_object_pid).read()
    # global resource_map_parser
    resource_map_parser = d1_client.data_package.ResourceMapParser(resource_map_xml)

    # def __init__(self):

    def create_pid(self):
        result = self.pid_title.encode('utf-8')
        return result

    def make_bag(self):
        # Make bag directory named after PID.
        os.mkdir(self.resource_map_parser.get_resource_map_pid())
        # Create bag structure and assign contact.
        bag = bagit.make_bag(self.resource_map_parser.get_resource_map_pid(), {'contact-name': 'test'})

    def map_pid(self):
        # Create pid-mapping.txt file.
        # Fill with corresponding names.
        os.chdir(self.resource_map_parser.get_resource_map_pid())
        out_file = open('pid-mapping.txt', 'w')

        for _ in self.resource_map_parser.get_aggregated_pids():
            my_list = self.resource_map_parser.get_aggregated_pids()

        i = 0

        # Loop through list to get total results.
        # First item for map needs PID, the rest are assigning new values mapped locally.
        # Regex to sort special characters for linux, win and osx. Replace with hyphen.
        for _ in my_list:
            if i == 0:
                write_var = self.resource_map_parser.get_resource_map_pid() + '' + "ONEDrive_Data_Files/" + my_list[
                    i] + '\n'
                formatted_output = re.sub('[<>:"|?*&$;!(){}%^=]', '-', write_var)
                out_file.write(formatted_output)
                i += 1
            elif i <= len(my_list) and i > 0:
                write_body = my_list[i] + ' ' + 'ONEDrive_Data_Files/' + my_list[i] + '\n'
                formatted_output = re.sub('[<>:"|?*&$;!(){}%^= ]', '-', write_body)
                out_file.write(write_body)
                i += 1

        out_file.close()

    def dir_process(self):
        # Move into bag
        os.chdir('data')
        # Create file objects to fill our 'data'
        for pid in self.resource_map_parser.get_aggregated_pids():
            file_obj = open(pid, 'w+')

        # Rename our data directory
        def get_parent_directory(dir):
            return os.path.dirname(dir)

        my_directory_parent = get_parent_directory(os.getcwd())

        os.chdir(my_directory_parent)
        os.rename("data", "ONEDRIVE_DATA_FILES")

        # Walk back up to package top level
        get_parent_directory(msg)
        my_directory_parent = get_parent_directory(os.getcwd())
        os.chdir(my_directory_parent)

        # Completed process
        print "Complete"

    def run_data(self):
        self.create_pid()
        self.make_bag()
        self.map_pid()
        self.dir_process()

        # FUSE
        sshfs_mount()

        return self.resource_map_parser

    def data_delete(self):
        # Delete generated directory. Later option
        shutil.rmtree(self.pid_title)


example = Usgs_Data_Pkg()


def main():
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.DEBUG)

    example = Usgs_Data_Pkg()

    # Create window
    make_window(MN_BASE_URL)


if __name__ == '__main__':
    main()