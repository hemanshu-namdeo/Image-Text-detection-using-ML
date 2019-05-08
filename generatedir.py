# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 02:48:07 2019

@author: Hemanshu Namdeo
"""

import os
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating Directory : ' + directory)
        os.makedirs(directory)