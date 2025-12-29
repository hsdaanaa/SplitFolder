#!/usr/bin/env python3
###########################################################################################
# Functions to split a folder into several parts (i.e. files are copied in to subfolders)
# Version 0.0.2 – by Hassan Sibroe Abdulla Daanaa
###########################################################################################
#======================================Dependencies========================================
import sys
import os
import time
import shutil
import pandas as pd
from utils import get_f_pathlist_from_folder, make_new_folder, write_flist_for_folder, get_current_date, copy_files_to_folder
#============================================Main==========================================
def splitfolder(path_to_input_folder,
                out_folder_ct, 
                path_to_output_folder, 
                file_exts, 
                verbose = 1): 
    """takes an input path to a directory that contains files and creates new
    directories, each containing a random sample (without replacement) of the 
    files in the input directory. 'partitions' specifies the number of new directories 
    to create. 'file_suffix' specifies the extension name of the files to sample. if 
    file_suffix is '' all files in the directory will used for sampling. 
    
    parameters
    ----------
    path_to_input_folder: str
        path to the input directory containing files
    partitions: int
        number of partitions
    path_to_output_folder: str
        path to the output directory
    file_suffix: str
        extension name of the files
    verbose: int 0, 1 
        set to 1 for debugging outputs
        
    return
    ------
    str"""
    
    log_path = os.path.join(path_to_output_folder, 'log.txt')
    
    #TODO: create outfodler for program make_new_folder(path_to_output_folder, '')  # create output folder if it does not exist

    # function to write 
    # TODO: sep func
    with open(log_path, 'w') as file: 
        file.write('---------------------------------------\n')    
        file.write('SplitFolder v0.0.1 (Hassan S.A. Daanaa)\n')       
        file.write('---------------------------------------\n')    
        file.write('Start time                  : {}\n'.format(time.ctime()))
        file.write('Path to input folder        : {}\n'.format(path_to_input_folder))
        file.write('Output subfolder count      : {}\n'.format(out_folder_ct))
        file.write('Path to output folder       : {}\n'.format(path_to_output_folder))
        file.write('Input file extension names  : {}\n'.format(file_exts))
        file.write('Verbose                     : {}\n'.format(verbose))
        file.write('------------------processing------------------------\n')    

        # extract dir name 
        folder_name = path_to_input_folder.split('/')[-1]
        if verbose == 1:
            print('Folder name: {}\n'.format(folder_name))

        # check ext
        if file_exts == '': 
            path_df = pd.DataFrame(get_f_pathlist_from_folder(path_to_input_folder, ext = None), columns = ['path_list']).sort_values(by = 'path_list')
        else:
            path_df = pd.DataFrame(get_f_pathlist_from_folder(path_to_input_folder, ext = file_exts), columns = ['path_list']).sort_values(by = 'path_list')

        path_ct = len(path_df)
        if verbose == 1:
            print('file count: {}'.format(path_ct))

        # Set file count per folder
        files_per_folder   = int(path_ct/out_folder_ct)
        if verbose == 1:
            print('Approx. files per output subfolder: {}'.format(files_per_folder))
        
        # Split folder
        copy_of_path_df = path_df.copy()
        rem_filenum     = len(copy_of_path_df)
        
        for subfolder_id in range(1,  out_folder_ct + 1): 

            # make dir 
            sub_folder_name = 'pt{}_{}'.format(subfolder_id if subfolder_id >=10 else '0' + str(subfolder_id), folder_name) #'pt{}_{}'.format(_parts, folder_name)
            sub_dir         = make_new_folder(path_to_output_folder, sub_folder_name)
            file.write('current partition: {}\n'.format(sub_dir))

            # check remaining files in the dataframe 
            file.write('remaining file num: {}\n'.format(rem_filenum))

            if rem_filenum == 0:
                break
                print('could only create {} partitions'.format(_parts - 1))

            elif rem_filenum > files_per_folder: 
                file.write('remaining file num is greater than the expected file number per sub folder\n')
                file.write('files adding to partition: {}\n'.format(files_per_folder))
                
                # if remaining files is greater than the files per dir by more than 10 files
                # sample files randomly
                path_sample_df  = copy_of_path_df.iloc[0:files_per_folder,].copy() #sample(n = files_per_folder, replace = False)
                sample_indexes  = path_sample_df.index

                # copy these files to the directory 
                copy_files_to_folder(path_sample_df.path_list.to_list(), sub_dir)

                # write file list 
                write_flist_for_folder(sub_dir)

                # remove sampled files from original df 
                copy_of_path_df = copy_of_path_df[~copy_of_path_df.index.isin(sample_indexes)].copy()
                rem_filenum      = len(copy_of_path_df)

        rem_filenum <= files_per_folder
        file.write('remaining file num is less than the expected file number per sub folder\n')
        file.write('files adding to partition: {}\n'.format(len(copy_of_path_df)))
        # otherwise, add all remaining files to this directory
        copy_files_to_folder(copy_of_path_df.path_list.to_list(), sub_dir)

        # write file list for directory
        write_flist_for_folder(sub_dir)

        file.write('----\n')
        
        file.write('end time: {}'.format(time.ctime()))
                
        print('Done. check: {}'.format(path_to_output_folder))
        return path_to_output_folder
#------------------------------------------------------------
if __name__ == '__main__': 
    path_to_input_folder    = sys.argv[1]
    out_subfolder_ct        = int(sys.argv[2])
    file_ext                = sys.argv[3].split(',')  # list of file extensions
    path_to_output_folder   = sys.argv[4]
    verbose                 = int(sys.argv[5])
    
    splitfolder(path_to_input_folder      = path_to_input_folder,
                out_folder_ct             = out_subfolder_ct,
                file_exts                 = file_ext,
                path_to_output_folder     = path_to_output_folder,
                verbose                   = verbose)