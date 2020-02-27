'''
Created on Dec 24, 2019
@author: Diyor.Zakirov
'''
from netCDF4 import Dataset
import numpy as np
import os
import argparse
import varTest as vt
import statTest as st
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="pyect")
    parser.add_argumnet("path", help="Full path to a folder with ensemble data")
    args = parser.parse_args()
    
    
        
    