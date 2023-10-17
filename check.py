import os

def check_item_number(obs_itemnum, exp_itemnum):
    msg = f'Wrong number of items found: {obs_itemnum}. {exp_itemnum} was expected.'
    assert obs_itemnum == exp_itemnum, msg
        
def check_item_divisor(item_divisor):
    assert isinstance(item_divisor, str)
    assert item_divisor != ''

def check_dirs_exist(*dir_paths):
    """Raises FileNotFoundError if any of given directories does not exist. 
    """
    for dir_path in dir_paths:
        if not os.path.isdir(dir_path):
            raise FileNotFoundError(dir_path)
    
def check_dirs_not_exist(*dir_paths):
    """Raises FileExistsError if any of given directories exists. 
    """
    for dir_path in dir_paths:
        if os.path.isdir(dir_path):
            raise FileExistsError(dir_path)

def check_files_exist(*file_paths):
    """Raises FileNotFoundError if any of given files does not exist. 
    """
    for file_path in file_paths:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
    
def check_files_not_exist(*file_paths):
    """Raises FileExistsError if any of given files exists. 
    """
    for file_path in file_paths:
        if os.path.isfile(file_path):
            raise FileExistsError(file_path)
