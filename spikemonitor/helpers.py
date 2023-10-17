#!/usr/bin/env python
# coding: utf-8

# Neuronexus recording details are stored in JSON files. We want to extract: 
# 
# 1) the sample rate, located in the "sample_freq" field
# 
# 2) total # of channels, located in the "total" field of the "signals" object
# 
# 
# The "pri" field contains the total # of probe channels. 
# The "aux", "din", and "dout" fields contain the # of analog input, digital input, and digital output channels, respectively. Each block of data is stored in this order.
# 
# 3) # of probes, can be discovered from the "port" array
# 
# 4) # of channels in each probe; Look at the first "pri" elements in the array and count the unique values. For each unique value, count the number of occurrences and you'll get the # of channels in that probe.
# 
# 5) the depth information, located in the "site_ctr_y" array; For each probe, store the depth information in an array. We want to store the depth information of each probe so we can sort the display by depth.
# 
# 6) the channel offset of each probe, where that specific probe's data starts in each block of data, For example, if we have two probes, A and B, both having 64 channels, probe A's offset will be 0, because it starts at the beginning of the block, and probe B's offset will be 64, because it starts directly after probe A in the block.
# 
# 
# You should create a class that holds the probe information (port, # of channels, depth, offset).
# 
# You should create a class that holds the recording information (sample rate, total # of channels, # of probes, array of probe objects)
# 
# Create a function 'read_nnexus' that takes in the file name and returns a recording information object with all of the data listed above.
# 
# An example JSON file from a NeuroNexus recording is available here: https://drive.google.com/file/d/1T1_pEUKCY1Ovkwt61lfP7ww5hKReVmDX/view?usp=drive_link
# 

import json
import tkinter as tk
from tkinter import filedialog
import numpy as np


def read_header():
    
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    if file_path:
        
        if ".xdat.json" in file_path:
            return read_nnexus(file_path)
        else:
            raise Exception("Unsupported file type selected.")
            
    else:
        
        raise Exception("Header file not selected.")
    

class probe:
    
    def __init__(self, port, channel_number, depth, offset):
        
        self.port = port
        self.channels = channel_number
        self.depth = depth
        self.offset = offset


class recording:
    
    def __init__(self, data):
        
        self.sample_freq = data['status']['samp_freq']
        self.stride = data['status']['signals']['total']
        self.channel_number = data['status']['signals']['pri']
            
        port = data['sapiens_base']['biointerface_map']['port'][:self.channel_number]
        port_name, channel_offset, channel_per_probe = np.unique(port,return_index=True,return_counts=True)

        depth_all = data['sapiens_base']['biointerface_map']['site_ctr_y'][:self.channel_number]
        depth_per_probe = np.split(np.array(depth_all),channel_offset[1:])  # probe_channel_index[0] is 0, exclude for splitting

        self.probe_number = len(port_name)
        self.probes = [[] for x in range(self.probe_number)]
        
        for index in range(self.probe_number):
            self.probes[index] = probe(port_name[index],channel_per_probe[index],depth_per_probe[index],channel_offset[index])


def read_nnexus(filename):
    
    with open(filename) as f:
        data = json.load(f)
    
    return recording(data)


