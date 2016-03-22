'''
Created on 22 Mar 2016

@author: steve
'''

import glob
import subprocess
import os
import tracks as tr
import write_file as wr


def tomato_circos_LFC_raw(file_path, mutant, WT, data_out_dir):
    """
    This is for tomato with 12 chromosomes
    
    Only works if filename are correctly formatted:
    
    ie. /Users/steve/seq/UQCbioinf15/ana/SL_analysis/tomato/SL2.50ch01.fa_Sl_demDs_ret_MD_pollen_1_21_bin.csv
    
    where the chromosome number is the 2 digits after SL2.50ch
    and the sample name (including sRNA len) is after .fa_ and before nt_bin.csv
    
    out_dir should be where the out_dir/data/ is located
    """
    #Tomato chromosome numbers
    total_chr_list=['01','02','03','04','05','06','07','08','09','10','11','12']
    
    #sRNA lengths to analyse
    sRNA_len_list=['21','22','24']
    
    file_list=glob.glob(file_path)
    
    
    
    #data for output
    combined_list=[]
    raw_list= []
    
    for sRNA_len in sRNA_len_list:
        for chromosome in total_chr_list:
            #list of correct files for that sRNA_len.
            chr_list = []
            #raw list

            mutant_filename=''
            WT_filename=''
            chromosome_name = 'chr'+chromosome
            for lfc_file in file_list:
                if lfc_file.split('SL2.50ch')[1][:2] == chromosome:
                    chr_list.append(lfc_file)
            
            for lfc_chr_file in chr_list:
                mutant_name =  "{0}_{1}".format(mutant, sRNA_len)
                WT_name = "{0}_{1}".format(WT, sRNA_len)
                if lfc_chr_file.split('.fa_')[1][:-8] == mutant_name:
                    mutant_filename = lfc_chr_file
                elif lfc_chr_file.split('.fa_')[1][:-8] == WT_name:
                    WT_filename = lfc_chr_file
                    #Inner track raw data
                    if sRNA_len == '24':
                        raw_list += tr.raw_count_track(lfc_chr_file, 
                                                    chromosome_name)
                        
                else:
                    pass
            combined_list += tr.LFC_tracks(mutant_filename,
                                           WT_filename, 
                                           chromosome_name)
       
        out_file = "{0}_{1}_{2}nt.txt".format(mutant,WT,sRNA_len)
        wr.write_to_file(combined_list, data_out_dir+out_file)
    
    wr.write_to_file(raw_list, '{0}{1}_raw_24nt.txt'.format(data_out_dir,mutant))
    
def mod_template_conf_tomato(out_dir):
    """
    Out_dir must be full path
    
    """
    subprocess.call(["mkdir" , out_dir])
    subprocess.call(["mkdir",out_dir+"/plots"])
    subprocess.call(["mkdir",out_dir+"/etc"])
    subprocess.call(["mkdir",out_dir+"/data"])
    
#     #for notebook
#     template_files = glob.glob(os.getcwd()+"/conf_template_tomato/*")
    #for real
    template_files = glob.glob(os.path.dirname(os.path.realpath(__file__))\
                               +"/conf_template_tomato/*")
    
    for template_file in template_files:
        subprocess.call(["cp", template_file,out_dir+"/etc/"])
        
def bulk_circos_plot(paired_in_list, path_to_bin_files, out_dir):
    """
    paired_in_list should be a tab delimited text file with analysis pairs on each row
    ie. 
    path/to/mutant    path/to/WT 
    
    out_dir is where the LFC files will be located along with plots
    
    path_to_bin_files should be in this format:
    'path/to/bin/files/*_bin.csv'
    
    """
    path_to_bin_files = path_to_bin_files + "/*_bin.csv"
    print path_to_bin_files
    #prepare directory structure
    mod_template_conf_tomato(out_dir)
    
    data_out_dir = out_dir+"/data/"
    
    with open(paired_in_list, 'r') as f:    
        for analysis_pair in f:
            analysis_pair = analysis_pair.strip().split("\t")
            tomato_circos_LFC_raw(path_to_bin_files, 
                                  analysis_pair[0], 
                                  analysis_pair[1], 
                                  data_out_dir)
            mod_conf_and_circos_tomato(out_dir, analysis_pair[0],
                                       analysis_pair[1] )
    f.close()
    
def mod_conf_and_circos_tomato(path_to_conf, mutant, WT):
    """
    Modify the tomato conf template for each analysis
    """
    line_count = 1
    LFC_file_name = "{0}_{1}".format(mutant,WT)
    
    path_to_conf_template = path_to_conf+"/etc"
    #path_to_data = path_to_conf+"/data"
    #path_to_plots = path_to_conf+"/plots" 
    
    
    out_conf = path_to_conf+"/"+LFC_file_name+".conf"
    with open(path_to_conf_template+"/circos_template_tomato.conf", 'r') as f:
        with open(out_conf, 'w') as g:
            for line in f:
                if line_count ==6:
                    new_line = "    dir* = {0}/plots/\n".format(path_to_conf)
                    g.write(new_line)
                elif line_count == 7:
                    new_line = "    file* = {0}.png\n".format(LFC_file_name)
                    g.write(new_line)
                elif line_count == 50:
                    new_line = "        file    = data/{0}_24nt.txt\n"\
                    .format(LFC_file_name)
                    g.write(new_line)
                elif line_count == 78:
                    new_line = "        file    = data/{0}_22nt.txt\n"\
                    .format(LFC_file_name)
                    g.write(new_line)
                elif line_count == 107:
                    new_line = "        file    = data/{0}_21nt.txt\n"\
                    .format(LFC_file_name)
                    g.write(new_line)
                elif line_count == 133:
                    new_line = "        file    = data/{0}_raw_24nt.txt\n"\
                    .format(mutant)
                    g.write(new_line)
                else:
                    g.write(line)
                line_count+=1
    f.close()
    g.close()
    subprocess.call(["circos" , "-conf",  out_conf])
