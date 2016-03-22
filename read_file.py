'''
Created on 22 Mar 2016

@author: steve
'''
def read_bin(in_file_1, chromosome):
    """Read bin file
    """
        
    bin_list=[]    
    header_line = True
    with open(in_file_1, 'r') as f:
        for bin_count in f:
            if header_line:
                header_line = False
            else:
                bin_count = bin_count.strip().split(',')
                single_bin = [chromosome, bin_count[1], bin_count[2], 
                              float(bin_count[3])]
                bin_list.append(single_bin)  
    f.close()
    return bin_list

