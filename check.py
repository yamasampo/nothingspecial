import os

def check_item_number(obs_itemnum, exp_itemnum):
    msg = f'Wrong number of items found: {obs_itemnum}. {exp_itemnum} was expected.'
    assert obs_itemnum == exp_itemnum, msg
        
def check_item_divisor(item_divisor):
    assert isinstance(item_divisor, str)
    assert item_divisor != ''

def check_dir_exists(dir_path):
    """Raises FileNotFoundError if a given directory does not exist. 
    """
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(dir_path)
    
def check_dir_not_exist(dir_path):
    """Raises FileExistsError if a given directory exists. 
    """
    if os.path.isdir(dir_path):
        raise FileExistsError(dir_path)

