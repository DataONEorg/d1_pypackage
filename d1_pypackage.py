#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
:mod:`get_and_display_data_package`
===================================

:Synopsis:
  This is an example on how to use the DataONE Client Library to retrieve a data package on your system. It
  shows how to:

  - Download a Resource Map (Data Package)
  - Parse and display the Resource Map on local system.
  - Remove data package from system (commented out currently)

:Author:
  USGS (Serna)

:Created:
  2015-02-06

:Requires:
  - Python 2.7
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
'''

# Stdlib.
import codecs
import datetime
import hashlib
import logging
import os
import sys
import shutil
import re

# 3rd party.
import pyxb
import bagit

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.const
import d1_client.data_package
import d1_client.mnclient


# Config.

# The identifier (PID) of the DataONE Data Package (Resource Map) to download
# and display. Data packages have Format ID
# http://www.openarchives.org/ore/terms.
SCIENCE_OBJECT_PID = 'dakoop_test-PKG'

# BaseURL for the Member Node on which the science object resides. If the script
# is run on the same server as the Member Node, this can be localhost.
MN_BASE_URL = 'https://mn-demo-6.test.dataone.org/knb/d1/mn'
#MN_BASE_URL = 'https://localhost/mn'

# Paths to the certificate and key to use when retrieving the object. This is
# required if the object is not publicly accessible. If the certificate has the
# key embedded, the _KEY setting should be set to None. If the objects have
# public access, these can both be set to None.
CERTIFICATE_FOR_CREATE = None
CERTIFICATE_FOR_CREATE_KEY = None

msg = ''

def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  # Create a Member Node client that can be used for running commands against
  # a specific Member Node.
  client = d1_client.mnclient.MemberNodeClient(MN_BASE_URL,
    cert_path=CERTIFICATE_FOR_CREATE, key_path=CERTIFICATE_FOR_CREATE_KEY)

  # Use the client to get a data package as a string (Format ID
  # http://www.openarchives.org/ore/terms).
  resource_map_xml = client.get(SCIENCE_OBJECT_PID).read()

  # Create a resource map parser.
  resource_map_parser = d1_client.data_package.ResourceMapParser(resource_map_xml)

  
  # Make bag directory named after PID.
  os.makedirs(resource_map_parser.get_resource_map_pid())

  # Create bag structure and assign contact.
  bag = bagit.make_bag(resource_map_parser.get_resource_map_pid(), {'contact-name': 'test'})


  # Create pid-mapping.txt file.
  # Fill with corresponding names.
  os.chdir(resource_map_parser.get_resource_map_pid())
  outFile = open('pid-mapping.txt', 'w')

  for pid in resource_map_parser.get_aggregated_pids():
    myList = resource_map_parser.get_aggregated_pids()

  # Loop through list to get total results. 
  # First item for map needs PID, the rest are assigning new values mapped locally. 
  # Regex to sort special characters for linux, win and osx. Replace with hyphen. 
  i = 0
  for instance in myList: 
    if i == 0:
      writeVar = resource_map_parser.get_resource_map_pid() +' ' + 'ONEDrive_Data_Files/' + myList[i] +'\n'
      formattedOutput = re.sub('[<>:"|?*&$;!(){}%^=]','-',writeVar)
      outFile.write(formattedOutput)
      i += 1
    elif i <= len(myList) and i > 0:
      writeBody = myList[i] +' ' + 'ONEDrive_Data_Files/' + myList[i] +'\n'
      formattedOutput = re.sub('[<>:"|?*&$;!(){}%^= ]','-',writeBody)
      outFile.write(writeBody)
      i += 1
 
  outFile.close()
  

  # Move into bag 
  os.chdir('data')

  # Create file objects to fill our 'data'
  for pid in resource_map_parser.get_aggregated_pids():
    fileObj = open(pid, 'w+')

  # Rename our data directory
  def getParentDirectory(directory):
    return os.path.dirname(directory)
  myDirectorysParent = getParentDirectory(os.getcwd())

  os.chdir(myDirectorysParent)
  os.rename("data", "ONEDrive_Data_Files")

  # Walk back up to package top level
  getParentDirectory(msg)
  myDirectorysParent = getParentDirectory(os.getcwd())
  os.chdir(myDirectorysParent)

  # Delete generated directory. Later option
  # shutil.rmtree(resource_map_parser.get_resource_map_pid())


if __name__ == '__main__':
  main()
