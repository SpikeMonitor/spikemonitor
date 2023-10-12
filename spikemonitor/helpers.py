import json
import tkinter as tk
from tkinter import filedialog

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

# Neuronexus recording details are stored in JSON files. We want to extract the sample rate, total # of channels, # of probes, # of channels in each probe, the depth information, and the channel offset of each probe.
# An example JSON file from a NeuroNexus recording is available here: https://drive.google.com/file/d/1T1_pEUKCY1Ovkwt61lfP7ww5hKReVmDX/view?usp=drive_link
# The sample rate is located in the "sample_freq" field.
# The total # of channels is located in the "total" field of the "signals" object. The "pri" field contains the total # of probe channels. The "aux", "din", and "dout" fields contain the # of analog input, digital input, and digital output channels, respectively. Each block of data is stored in this order.
# The # of probes can be discovered from the "port" array. Look at the first "pri" elements in the array and count the unique values. For each unique value, count the number of occurrences and you'll get the # of channels in that probe.
# The depth information is located in the "site_ctr_y" array. For each probe, store the depth information in an array. We want to store the depth information of each probe so we can sort the display by depth.
# The channel offset is where that specific probe's data starts in each block of data. For example, if we have two probes, A and B, both having 64 channels, probe A's offset will be 0, because it starts at the beginning of the block, and probe B's offset will be 64, because it starts directly after probe A in the block.
# You should create a class that holds the probe information (port, # of channels, depth, offset).
# You should create a class that holds the recording information (sample rate, total # of channels, # of probes, array of probe objects)
# Create a function 'read_nnexus' that takes in the file name and returns a recording information object with all of the data listed above.
def read_nnexus(filename):
  return
