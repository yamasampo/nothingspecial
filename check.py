
def check_item_number(obs_itemnum, exp_itemnum):
    msg = f'Wrong number of items found: {obs_itemnum}. {exp_itemnum} was expected.'
    assert obs_itemnum == exp_itemnum, msg
        
def check_item_divisor(item_divisor):
    assert isinstance(item_divisor, str)
    assert item_divisor != ''
