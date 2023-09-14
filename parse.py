""" A collection of file parser functions. All the functions in this module 
takes a file path as input and output an object (object types depend on data
types). 
"""

from warnings import warn
from typing import List, Dict, Union, Callable, Any

from .text import get_itemnum, do_nothing
from .check import check_item_number, check_item_divisor

# =============== Primary Functions [start] =============== #

def read_1D_list(
        file_path       : str, 
        comments        : List[str] = ['/*', '#'], 
        itemnum         : Union[str, int] = 'infer',
        apply_func      : Callable[[str], Any] = do_nothing, 
        skip_empty_lines: bool = True,
        skip_headers    : int = 0, 
        header_parser   : Callable[[List[str]], Any] = do_nothing
        # cut_inline_comment = False # TODO: Implement in the future
        ) -> List[Any]:
    """Read a plain-text file containing 1D list data. 

    The expected number of items is read from a line starting with 'itemnum:'. 
    If such line does not exist, this function does not item number checking. 

    Parameter
    ---------
    file_path: str
        Path to input file. 
    comments: List[str], optional (default: ['/*', '#'])
        Strings that indicate comment lines.
    apply_func: Callable[[str], Any], optional (default: text.do_nothing)
        Function applied to each of value lines.
    skip_empty_lines: bool, optional (default: True)
        Whether to skip empty lines. 

    Return
    ------
    List[Any]
        List containing each line in the input file as an element. Elements in 
        the list may not be string object depending on apply_func argument. 
    """
    # Initialize a list that will be returned from this function
    items: List[str] = []
    exp_itemnum = None
    line_count = 0
    header_lines = []

    # Open the input file by a read mode
    with open(file_path, 'r') as f:
        # For each line
        for l in f:
            # Remove empty characters (e.g., space, tab or next line) on both 
            # left and right ends
            line = l.rstrip('\n')

            # If a line is empty
            if line == '':
                # If skip_empty_lines option is True
                if skip_empty_lines:
                    # Go to the next line
                    continue
            else:
                line_count += 1

                if line_count <= skip_headers:
                    header_lines.append(line)
                    continue

            # If a line starts with 'itemnum:'
            if itemnum == 'infer':
                if line.startswith('itemnum:'):
                    # Get the expected number of items
                    exp_itemnum = get_itemnum(line)
                    # Go to the next line
                    continue

            elif isinstance(itemnum, int):
                exp_itemnum = itemnum                

            # Check if this a comment line
            full_line_comment = [
                comment # Character indicating that this is a comment line 
                for comment in comments if line.startswith(comment)
            ]
            # If a line starts with one of the comment, 
            if len(full_line_comment) > 0:
                # Go to the next line
                continue

            items.append(apply_func(line))

    if exp_itemnum != None:
        # Raise Assertion error if the observed number of items is different 
        # from the expected. 
        check_item_number(len(items), exp_itemnum)
    else:
        if itemnum == 'infer':
            msg = 'itemnum could not be inferred because a line starting from '\
                  '"itemnum:" was not found.'
            warn(msg)
    
    return items, header_parser(header_lines)

def read_2D_list(
        file_path           : str, 
        item_divisor        : str = '>',
        comments            : List[str] = ['/*', '#'], 
        apply_func          : Callable[[str], Any] = do_nothing, 
        join_value_lines    : bool = False,
        include_key_order   : bool = False,
        skip_headers        : int = 0, 
        skip_empty_lines    : bool = True, 
        read_values         : bool = True
        # cut_inline_comment = False # TODO: Implement in the future
        ) -> Dict[str, Union[str, List[Any]]]:
    """Read a plain-text file containing 2D list data. 

    This function requires a string specifies a division of items (item_divisor). 
    itemnum can be included. 

    Parameters
    ----------
    file_path: str
        Path to input file.
    item_divisor: str, optional (default: '>')
        String specifies a division of items. If a line starts with item_divisor, 
        then the line is considered a start of a new item, therefore the last 
        item is stored as a separate element in an output dictionary. 
    comments: List[str], optional (default: ['/*', '#'])
        Strings that indicate comment lines.
    apply_func: Callable[[str], Any], optional (default: text.do_nothing)
        Function applied to each of value lines.
    join_value_lines: bool, optional (default: False)
        Whether to combine elements of a value into one string. For example, 
        give True when reading a multi-FASTA file. 
    skip_headers: int, opetional (default: 0)
        The number of header lines to skip reading. header lines may or may not 
        be comment out. Empty lines are not counted as headers. 
    skip_empty_lines: bool, optional (default: True)
        Whether to skip empty lines. 
    read_values: bool, optional (default: True)
        Whether to read non-key lines (e.g., nucleotide sequences in FASTA file).
        If a user wants to get only sequence IDs, set read_values = False. 

    Return
    ------
    Dict[str, Union[str, List[Any]]]
        Dictionary of items. A string following to item_divisor is a key and 
        lines until the next item_divisor is stored as value. 
    """
    
    # Initialize a list that will be returned from this function
    items: Dict[str, List[str]] = {}
    key = ''
    key_id = 0
    value = []
    exp_itemnum = None
    line_count = 0

    # Check if item_divisor is a string and is not empty. 
    check_item_divisor(item_divisor)

    # Open the input file by a read mode
    with open(file_path, 'r') as f:
        # For each line
        for l in f:
            # Remove empty characters (e.g., space, tab or next line) on both 
            # left and right ends
            line = l.rstrip('\n')

            # If a line is empty
            if line == '':
                # If skip_empty_lines option is True
                if skip_empty_lines:
                    # Go to the next line
                    continue
            # If the line is not empty
            else:
                # Increment line count
                line_count += 1
                if line_count <= skip_headers:
                    continue

            # If a line starts with 'itemnum:'
            if line.startswith('itemnum:'):
                # Get the expected number of items
                exp_itemnum = get_itemnum(line)
                # Go to the next line
                continue

            # Check if this a comment line
            full_line_comment = [
                comment # Character indicating that this is a comment line 
                for comment in comments if line.startswith(comment)
            ]
            # If a line starts with one of the comment, 
            if len(full_line_comment) > 0:
                # Go to the next line
                continue

            # If a line starts with the item_divisor, 
            if line.startswith(item_divisor):
                # If this is not empty (meaning that this is not the first item)
                if key != '':
                    # Assign key and value to the items dictionary
                    if read_values:
                        if join_value_lines:
                            items[key] = ''.join(value)
                        else:
                            items[key] = value
                    else:
                        # Assign None if read_values is False.
                        items[key] = None
                
                # Get item key from the current line
                if include_key_order:
                    key = (line.split(item_divisor)[1], key_id)
                else:
                    key = line.split(item_divisor)[1]
                
                # Check if key is not empty
                assert key != '', 'Empty key for 2D list is not supported.'
                value = []
                # Increment key ID    
                key_id += 1
                
            else:
                value.append(apply_func(line))
    
    if key != '':
        # Assign key and value to the items dictionary
        if read_values:
            if join_value_lines:
                items[key] = ''.join(value)
            else:
                items[key] = value
        else:
            items[key] = None

    if exp_itemnum != None:
        # Raise Assertion error if the observed number of items is different 
        # from the expected. 
        check_item_number(len(items), exp_itemnum)

    return items

# =============== Primary Functions [end] =============== #

