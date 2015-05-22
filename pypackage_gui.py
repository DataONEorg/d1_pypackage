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
"""
:Synopsis:
  This is a graphical user interface example on how to use the DataONE Client Library to retrieve a data package on
  your system. It shows how to:

  - Download a Resource Map (Data Package)
  - Parse and display the Resource Map on local system.
  - Remove data package from system

:Author:
  USGS (Brandon Serna)

:Created:
  2015-05-05

:Requires:
  - Python 2.7
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
"""
# Stdlib.
from Tkinter import *
from PIL import Image, ImageTk

# DataOne.
import d1_pypackage

import fuse

# Create window function, using grid layout
def make_window(url):
    # Define tk instance
    window = Tk()

    # Fix window size
    window.resizable(width=FALSE, height=FALSE)
    window.geometry('{}x{}'.format(540, 140))

    # Set Caption
    window.wm_title('DataONE ONEDrive')

    # Text labels
    Label(window, text='Please enter your PID title: ').grid(row=1, column=0)
    Label(window, text='Please enter URL:             ').grid(row=2, column=0)

    # Text fields
    pid_title = Entry(window, width=25)
    pid_url = Entry(window, width=40)

    # Default test instance
    title = 'dakoop_test-PKG'
    pid_title.insert(END, title)
    pid_url.insert(END, url)

    # Buttons
    # my_widget will invoke the run_data function container with the pid title parameter
    # del_data will invoke the data_delete function to remove the created directory
    my_widget = Button(window, text='Collect data', command=lambda: d1_pypackage.example.run_data())
    del_data = Button(window, text='Delete data collected', command=lambda: d1_pypackage.example.data_delete())

    # ONEDrive Logo
    logo = Image.open("onedrive_1.jpg")
    tk_img = ImageTk.PhotoImage(logo)
    logo_label = Label(window, image=tk_img)
    logo_label.img = tk_img

    # Grid layout
    pid_title.grid(row=1, column=1, sticky=W)
    pid_url.grid(row=2, column=1, sticky=W)
    my_widget.grid(row=3, column=0, sticky=W)
    del_data.grid(row=3, column=1, sticky=W)
    logo_label.grid(row=0, column=0, sticky=W)


    # Close function
    def on_close():
        fuse.sshfs_unmount()
        window.destroy()

    # Run loop
    mainloop()

    window.protocol('WM_DELETE_WINDOW', on_close())