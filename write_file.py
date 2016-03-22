'''
Created on 22 Mar 2016

@author: steve
'''
def write_to_file(combined_list, out_file):
    """
    Write to tab delimited text file
    """
    with open(out_file,'w') as f:
        for lfc_bin in combined_list:
            line = '{0}\t{1}\t{2}\t{3}\n'.format(lfc_bin[0],
                                               lfc_bin[1],
                                               lfc_bin[2],
                                               lfc_bin[3])
            f.write(line)
    f.close()