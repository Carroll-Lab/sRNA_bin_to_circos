'''
Created on 22 Mar 2016

@author: steve
'''

import read_file as rf
import math

def LFC_tracks(in_file_1, in_file_2, chromosome):
    """
    Return a list --> [chr, start, end, LFC]
    
    LFC = log2(in_file_1/in_file_2)
    
    First and last position in output is LFC=0
    
    """
    bin_list=rf.read_bin(in_file_1, chromosome)
    
    calc_LFC(in_file_2, bin_list)
    
    return bin_list

def raw_count_track(WT_24nt, chromosome):
    """
    Raw RPRM for inner track
    """
    bin_list=rf.read_bin(WT_24nt, chromosome)
    
    return bin_list

def calc_LFC(in_file_2, bin_list):
    """
    Mods the count to L2FC in each bin
    """
    
    #for itereating through the bin list
    bin_no=0
    
    header_line = True
    with open(in_file_2, 'r') as f:
        for bin_count in f:
            if header_line:
                header_line = False
            else:
                bin_count = bin_count.strip().split(',')
                try:
                    FC = bin_list[bin_no][3]/float(bin_count[3])
                    LFC = math.log(FC, 2)
                except:
                    LFC = 0
                bin_list[bin_no][3] = round(LFC, 2)
                bin_no+=1
    return bin_list
                