## Using `dirs_dataset.sh` to generate DataSet dirs for training. 

The script will create virtual links and gather all the directories' subdirectories into one folder, and rename the subdirectories' name into `subdirectory_from_directory`


## Using `tryCSV.py` to generate labels for training.

The script will create label file containing two columns for the given training folder. Please put all data which should be trained into one folder. The folder's structure will be as following, which could be gathered(if initially separated by a larger category) by the given `dirs_dataset.sh`

The Main Directory 
|-- Subdirectory 1
|-- Subdirectory 2
|-- .....
