## SplitFolder
Storing a great many files (e.g., 10,000 files or above) in a single folder can slow down computer performance dramatically in many respects
(e.g., file indexing) and can be risky. SplitFolder addresses this issue by creating dividing an input folder into subfolders.

### Required data
    A folder containing one or more files.
    The program does not currently process subfolders within the input folder. 
    Only files in the top-level directory (i.e. path_to_input_folder) can be processed.
    
### Output data
    Subfolders of the input folder.
    A log file containing user arguments and processing information.

### Process overview
    1. Extract file paths from input folder. 
        Only files with specified extensions are retained.
    2. Determine the approximate file count per output subfolder (X)
        X = total file count / number of output subfolders
        this value is rounded down to the nearest integer. (using "int" function)
    3. Create an output subfolder within the main output folder
    4. Copy X files to the subfolder
    5. Repeat steps 3 and 4 until all files are copied.

    Further details are provided in "SplitFolder.py".

### How to run (from terminal)
    > cd <directory to SplitFolder.py>
    > python3 SplitFolder.py <path_to_input_folder> <out_folder_ct> <path_to_output_folder> <file_exts> <verbose>

    # path_to_input_folder: Path to a directory containing one or more files
                            Can be absolute or relative to scr directory

    # out_folder_ct: Number of output subfolders to create

    # path_to_output_folder: Path to the output folder
                            Can be absolute or relative to scr directory

    # file_exts: extension names for files to be copied. Please use comma to delimit names as:
                 aln,txt,faa
                
    # verbose: Flag for whether to output information to screen. 1 (recommended)

### Program folder structure
    >SplitFolder
        >src # source code
        >Examples # Two example runs of SplitFolder program
        LICENSE
        README.md

### Dependencies 
    Python ≥3.x
    pandas ≥1.1.3

### Notes 
    - Please do not name files in the input folder "00_filelist.txt". This name is reserved for 
      the file list created in each output subfolder.