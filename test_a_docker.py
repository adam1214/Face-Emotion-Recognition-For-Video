# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:47:42 2020

@author: Chun-Yu Chen
"""

import subprocess as sp
from distutils.dir_util import copy_tree
import platform
import pandas as pd
import pytest
import os
import shutil
import sys

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
    
def subprocess_cmd(CMD):
    """
    Execute the command in a shell script and print the output
    >>> subprocess_cmd('./{}'.format(script.sh))
    'Do stuff in script.sh'
    """
    p = sp.Popen(CMD, stdout=sp.PIPE, shell=True, universal_newlines=True)
    # Grab stdout line by line as it becomes available.
    # This will loop until p terminates.
    while p.poll() is None:
        print(p.stdout.readline())
        
def remove_subdirectory(folder):
    """
    Remove the subdirectories inside the folder
    NOT tested for multiple levels
    """
    for root, dirs, files in os.walk(folder):
        for dir_ in dirs:
            if dir_ != "":
                shutil.rmtree(os.path.join(root, dir_))

@pytest.fixture(scope = 'module')
def set_up():
    ''' Move test image to fer_input '''
    copytree('fer_verification/input', 'fer_input')
    files = folders = 0
    for _, dirnames, filenames in os.walk('fer_input'):
        files += len(filenames)
        folders += len(dirnames)    
    yield files

    print("\n Teardown...")
    if platform.system() == 'Windows':
        remove_subdirectory('feri_input')
        remove_subdirectory('feri_finished')
        remove_subdirectory('feri_result')
        remove_subdirectory('feri_output')
    else:
        subprocess_cmd('bash tear_down_linux.sh')


def test_mode_1(set_up):
    # Run the specific folder: mode 1  
    n_uids = set_up
    if platform.system() == 'Windows':
        subprocess_cmd('docker_run.bat folder1')
    else:
        subprocess_cmd('sudo bash docker_run.sh folder1')
    
    bools = [False for i in range(n_uids)]
    print(bools)
    j = 0
    for root, dirs, files in os.walk('fer_verification/result/folder1'): 
        for file_ in files:
            veri_df = pd.read_csv('fer_verification/result/folder1/' + file_)
            test_df = pd.read_csv('fer_result/folder1/' + file_)
            bools[j] = veri_df.equals(test_df)
            print('fer_result/folder1/' + file_)
            print(veri_df.equals(test_df))
            j = j + 1

    assert all(x == True for x in bools) == True

def test_mode_2(set_up):
    n_uids = set_up
    if platform.system() == 'Windows':
        subprocess_cmd('docker_run.bat')
    else:
        subprocess_cmd('sudo bash docker_run.sh')
    
    bools = [False for i in range(n_uids)]
    print(bools)
    j = 0
    for root, dirs, files in os.walk('fer_verification/result/'):
        for file_ in files:
            test_path = os.path.join(root, file_)[23:]
            test_path = "fer_result" + test_path
            veri_df = pd.read_csv(os.path.join(root, file_))
            test_df = pd.read_csv(test_path)
            bools[j] = veri_df.equals(test_df)
            print(test_path)
            print(veri_df.equals(test_df))
            j = j + 1

    assert all(x == True for x in bools) == True

if __name__ == "__main__":
    pytest.main(['-vv','--html=test_a_docker.html','--self-contained-html','--durations=2', "test_a_docker.py"])
    # py.test -vv --html=report.html --self-contained-html --durations=2 test_a_docker.py
    # sys.exit()


