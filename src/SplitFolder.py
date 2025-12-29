#!/usr/bin/env python3
###########################################################################################
# Functions to split a folder into several parts (i.e. files are copied in to subfolders)
# Written by Hassan Sibroe Abdulla Daanaa
###########################################################################################
# TODO: func_name_mod, fold_proc_mod
###########################################################################################
VERSION = '0.0.2' 
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
    """
    Divides files in an input folder into several output subfolders.
    Files from the input folder are copied into output subfolders (the count is specified by the user).
    
    Basic flow of copying process
    -----------------------------
    1. Extract file paths from input folder. 
        Only files with specified extensions are retained.
    2. Determine the approximate file count per output subfolder (X)
        X = total file count / number of output subfolders
        this value is rounded down to the nearest integer. (using "int" function)
    3. Create an output subfolder within the main output folder
    4. Copy X files to the subfolder
    5. Repeat steps 3 and 4 until all files are copied.
    
    Function body (below) has further details

    CAVEATS
    -------
      - This function does not currently process subfolders within the input folder. 
        Only files in the top-level directory (i.e. path_to_input_folder) can be processed.
      - Do not name files in the input folder "00_filelist.txt". This name is reserved for 
        the file list created in each output subfolder.
    
    parameters
    ----------
    path_to_input_folder: str
        Path to a directory containing one or more files
        Can be absolute or relative to scr directory
    out_folder_ct: int
        Number of output subfolders to create
    path_to_output_folder: str
        Path to the output folder
        Can be absolute or relative to scr directory
    file_exts: list
        List of extension names for files to be copied
    verbose: int 0, 1 
        Flag for whether to output information to screen.
        1 (recommended)
        
    return
    ------
    int
        1 if process completed successfully, -1 otherwise
    """

    # 1) Record time
    func_start  = time.time()
    
    # 2) Check argument data type and value
    usr_args = [path_to_input_folder, out_folder_ct, 
                path_to_output_folder, file_exts, verbose]    
    if not chk_args(usr_args) == 1:
        print('\tError in SplitFolder')
        print('\t\tGot one or more invalid arguments. Please see Traceback.')
        return -1

    # 3) Create main output folder
    main_output_folder = make_new_folder(path_to_output_folder, '{}_SplitFolder_output'.format(get_current_date()))

    # 4) Create log file and write arguments
    logfile_path            = os.path.join(main_output_folder, 'log.txt') 
    logfile_obj             = open(logfile_path, 'w')
    args2log(usr_args, logfile_obj, version = VERSION) 

    logfile_obj.write('====================Process Start======================\n')   
    logfile_obj.write('Data type and values successfully passed initial checks\n')   
    
    # 5) Get folder info and file paths
    folder_name = path_to_input_folder.split('/')[-1]
    if verbose == 1:
        print('Folder name: {}\n'.format(folder_name))

    if file_exts == '': 
        path_df = pd.DataFrame(get_f_pathlist_from_folder(path_to_input_folder, ext = None), columns = ['path_list'])
    else:
        path_df = pd.DataFrame(get_f_pathlist_from_folder(path_to_input_folder, ext = file_exts), columns = ['path_list'])
    path_df = path_df.sort_values(by = 'path_list')

    path_ct = len(path_df)
    if verbose == 1:
        print('file count: {}'.format(path_ct))
    logfile_obj.write('Input file count: {}\n'.format(path_ct))
    
    # 6) Create subfolders and copy files
    files_per_folder   = int(path_ct/out_folder_ct) # Set file count per folder
    if verbose == 1:
        print('\tApprox. files count per output subfolder: {}'.format(files_per_folder))
        print("\tdividing folder into parts")
    logfile_obj.write('Approx. files count per output subfolder: {}\n'.format(files_per_folder))
    
    copy_of_path_df = path_df.copy()  # modified in loop block below
    rem_filenum     = len(copy_of_path_df) # modified in loop block below
    
    logfile_obj.write('---------Start of copying-----------\n')
    for subfolder_id in range(1,  out_folder_ct + 1): 

        #print("\t\tCount of files to be copied: {}".format(rem_filenum))
        if rem_filenum == 0:
            print('Could not divide folder into {} parts. Created {} parts'.format(out_folder_ct, subfolder_id - 1))
            break

        elif rem_filenum >= files_per_folder: 
            #file.write('\t\tCount of files is greater than the file count per folder\n')
            logfile_obj.write('Count of files being added to output subfolder: {}\n'.format(files_per_folder))

            # Create subfolder
            sub_folder_name = 'pt{}_{}'.format(subfolder_id if subfolder_id >=10 else '0' + str(subfolder_id), folder_name)
            sub_dir         = make_new_folder(main_output_folder, sub_folder_name)
            logfile_obj.write('Out subfolder name: {}\n'.format(sub_dir))
    
            # Retain first "files_per_folder" count of files for copying
            path_sample_df  = copy_of_path_df.iloc[0:files_per_folder,:].copy()
            sample_indexes  = path_sample_df.index

            # Copy these files to the output subfolder
            copy_files_to_folder(path_sample_df.path_list.to_list(), sub_dir)

            # Write file list 
            write_flist_for_folder(sub_dir)

            # Remove paths to copied files and get count of remaining files to be copied
            copy_of_path_df = copy_of_path_df[~copy_of_path_df.index.isin(sample_indexes)].copy()
            rem_filenum     = len(copy_of_path_df)

            logfile_obj.write('Remaining file num: {}\n'.format(rem_filenum))
            logfile_obj.write('---------------------------\n'.format(rem_filenum))
                
    # Create a new subfolder to add remaining files, if any
    if rem_filenum != 0:
        # file.write('remaining file num is less than the expected file number per sub folder\n')
        logfile_obj.write('files adding to last output subfolder: {}\n'.format(len(copy_of_path_df)))

        # Create subfolder
        sub_folder_name = 'pt{}_{}'.format(subfolder_id if subfolder_id >=10 else '0' + str(subfolder_id), folder_name)
        
        # otherwise, add all remaining files to this directory
        copy_files_to_folder(copy_of_path_df.path_list.to_list(), sub_dir)

        # write file list for directory
        write_flist_for_folder(sub_dir)

    logfile_obj.write('---------End of copying-----------\n')
    
    logfile_obj.write('====================Process End======================\n')    
    
    # record function end time
    func_end           = time.time()
    total_time_elapsed = round((func_end - func_start)/60, 6)
    logfile_obj.write("Elapsed time: ~{} minutes".format(total_time_elapsed))
    logfile_obj.close()
            
    print('Done. Please see outputs in: {}'.format(main_output_folder))

    return 1
#=========================================Subfunctions=====================================
def args2log(args, 
            logfile_obj, 
            version = VERSION): 
    """
    Writes user arguments to log file
    
    parameters
    ----------
    args: list
        list containing user arguments
    logfile_obj:  object
        file obejct for log file
    version: str
        program version. default is the global variable VERSION
    
    returns 
    -------
    None"""
    
    path_to_input_folder   = args[0]
    out_folder_ct          = args[1]
    path_to_output_folder  = args[2]
    file_exts              = args[3]
    verbose                = args[4]
    
    #with open(logfile_path, 'w') as logfile_obj: 
    logfile_obj.write('----------------------------------------\n')    
    logfile_obj.write('SplitFolder v{} (Hassan S. A. Daanaa)\n'.format(version))       
    logfile_obj.write('----------------------------------------\n')    
    logfile_obj.write('Start time                      : {}\n'.format(time.ctime()))
    logfile_obj.write('Path to input folder            : {}\n'.format(path_to_input_folder))
    logfile_obj.write('Output subfolder count          : {}\n'.format(out_folder_ct))
    logfile_obj.write('Path to output folder           : {}\n'.format(path_to_output_folder))
    logfile_obj.write('Extension names for processing  : {}\n'.format(file_exts))
    logfile_obj.write('Verbose                         : {}\n\n'.format(verbose))  
#-------------------------------------------------------------------------------------------
def chk_args(args): 
    """
    Check data type and value of user arguments
    
    parameters
    ----------
    args: list
        list containing user arguments

    returns
    -------
    int or None
        1 if all checks pass. otherwise None
    """

    path_to_input_folder   = args[0]
    out_folder_ct          = args[1]
    path_to_output_folder  = args[2]
    file_exts              = args[3]
    verbose                = args[4]
    
    # Data type check
    assert isinstance(path_to_input_folder, str), 'TypeError for <path_to_input_folder>. Expected str type. Got {} type'.format(type(path_to_input_folder))    
    assert isinstance(out_folder_ct, int) , 'TypeError for <out_folder_ct>. Expected int type. Got {}'.format(type(out_folder_ct))

    assert isinstance(file_exts, list), 'TypeError for <file_exts>. Expected list type. Got {} type'.format(type(file_exts))
    assert isinstance(path_to_output_folder, str), 'TypeError for <path_to_output_folder>. Expected str type. Got {} type'.format(type(path_to_output_folder))
    assert isinstance(verbose, int), 'TypeError for <verbose>. Expected int type. Got {} type'.format(type(verbose))
    
    # Data value check
    assert os.path.isdir(path_to_input_folder), 'ValueError for <path_to_input_folder>. Folder path is invalid: {}'.format(path_to_input_folder)
    assert os.path.isdir(path_to_output_folder), 'ValueError for <path_to_output_folder>. Folder path is invalid: {}'.format(path_to_output_folder)
   
    # number of partitions must be ≤ number of files

    input_path_ct = len(get_f_pathlist_from_folder(path_to_input_folder, ext = file_exts))
    assert out_folder_ct <= input_path_ct, 'ValueError for <out_folder_ct>. Argument must be less than or equal to file count in folder. Got {} subfolders for {} input files'.format(out_folder_ct, input_path_ct)

    return 1 
#-------------------------------------------------------------------------------------------
if __name__ == '__main__':
    arg_num = len(sys.argv)

    if len(sys.argv) != 6:
        print("Error. Got {} arguments: {} ".format(arg_num, sys.argv))
        print('Wrong number of arguments. Please provide:\n'
              '1) Path to input folder\n'
              '2) Number of output subfolders to create\n'
              '3) File extensions\n'
              '4) Path to output folder\n'
              '5) Verbose (0/1)')
        sys.exit(1)

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