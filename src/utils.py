#! usr/bin/env Python3
#======================================Dependencies========================================
import sys
import os
import datetime
import shutil
#======================================Functions===========================================
def get_f_pathlist_from_folder(folder_path, ext = None):
    """takes an input path to a folder and returns a list containing
    paths to files in the folder. if <ext> is None, all paths are returned
    regardless of the file extension. if ext is e.g. ['.txt'] the function
    will return paths for all file names with .txt as the extension.
    
    note that only paths in the top-level directory are returned.
    
    parameters
    ----------
    folder_path: str
       path to folder to fetch paths to files
    ext: None or list
       specifies whether to fetch files with a particular extension
  
    returns
    -------
    list"""
    
    list_of_files = []
        
    try:
        assert os.path.isdir(folder_path) == True
    except:
        print('\tError in get_f_pathlist_from_folder')
        print('\t\tpath to folder was invalid')
        return -1 
    
    try: 
        assert ext == None or isinstance(ext, list)
    except:
        print('\tError in get_f_pathlist_from_folder')
        print('\t\tinput for <ext> was invalid. can only be None or list type')
        return -1 
    try:          
        folder_path  = os.path.abspath(folder_path)
        folder_items = os.listdir(folder_path)

        # loop over folder items
        for item in folder_items:
            # get item path
            path_to_item = os.path.join(folder_path, item) 
            # check path validity
            if os.path.isfile(path_to_item) == True: 
                # check ext setting and append path to item as necessary 
                if ext != None:   
                    if type(ext) == list: 
                        for extension in ext:
                            if item.endswith(extension):
                                list_of_files.append(path_to_item)
                    else:
                        item.endswith(ext)
                        list_of_files.append(path_to_item)
                else:
                    list_of_files.append(path_to_item)
    except Exception as error:
        print('\tError in get_f_pathlist_from_folder')
        print('\t\tgot: {}'.format(error))
        return -1 
    return list_of_files
#------------------------------------------------------------------------------------------
def make_new_folder(path_to_folder, folder_name):
    """creates a a new folder
    
    parameters
    ----------
    path_to_folder: str
        path to the folder where a new folder should be created
    folder_name: str
        name of the new folder
    
    returns 
    -------
    str"""
    try:
        assert isinstance(path_to_folder, str)
    except:
        print('\tError in make_new_folder')
        print('\t\t<path_to_folder> was not a string. got: {}'.format(type(path_to_folder)))
        return -1
    try:
        assert os.path.isdir(path_to_folder) == True
    except:
        print('\tError in make_new_folder')
        print('\t\tinput folder path was an invalid. got: {}'.format(path_to_folder))
        return -1
    
    # new folder name
    new_folder_path = os.path.join(path_to_folder, folder_name)
    # check if new_folder_path already exists
    try:
         assert os.path.isdir(new_folder_path) == False
    except:
        print('\tError in make_new_folder')
        print('\t\tCannot create new folder. A folder with the same name exists: {}'.format(folder_name))
        return -1

    # make folder
    try:
        os.makedirs(new_folder_path, exist_ok = False)
    except Exception as error: 
        print('\tError in make_new_folder')
        print('\t\tGot: {}'.format(error))
        return -1
        
    return new_folder_path
#------------------------------------------------------------------------------------------
def write_flist_for_folder(path_to_folder): 
    """creates a file containing the number of files in a folder
    and the names of the files. the output file is named 00_filelist.txt.
    This file name is excluded from file counts.
    
    parameters
    ----------
    path_to_folder: str
        path to the folder to fetch file names
    
    returns
    -------
    None"""
    
    try:
        assert isinstance(path_to_folder, str)
    except:
        print('\tError in write_flist_for_folder')
        print('\t\t<path_to_folder> was not a string. got: {}'.format(type(path_to_folder)))
        return -1
                    
    # extract file paths
    try:
        file_path_list = get_f_pathlist_from_folder(path_to_folder)
    except Exception as error: 
        print('\tError in write_flist_for_folder')
        print('\t\tgot: {}'.format(error))
    
    try:
        # retain file names
        file_name_list = [os.path.basename(i) for i in file_path_list]
        file_name_list = [i for i in file_name_list if not i == '00_filelist.txt']

        # create a file called 00_filelist.txt and write file names
        with open(path_to_folder + '/00_filelist.txt', 'w') as file:
            file.write('# files: {}\n'.format(len(file_name_list)))
            for file_name in file_name_list:
                file.write(file_name  + '\n')
    except Exception as error:
        print('\tError in write_flist_for_folder')
        print('\t\tgot: {}'.format(error))
#------------------------------------------------------------------------------------------
def copy_files_to_folder(list_of_paths, output_folder):
    """takes an input list of paths and a path to
    an output folder, copies files to folder"""
    
    try:
        os.path.isdir == True
    except AssertionError:
        print('your input dir path was not a directory')    
 
    for path in list_of_paths:
        file_name = os.path.basename(path)
        new_file_path = os.path.join(output_folder, file_name)
        shutil.copy(path, new_file_path)
        
    #print('Done\n')
#------------------------------------------------------------------------------------------
def get_current_date():
    """returns current date YMD"""
    current_date = datetime.datetime.now()
    return '{}-{}-{}'.format(current_date.year,current_date.month,current_date.day)
#------------------------------------------------------------------------------------------
