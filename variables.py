
__version__ = '1.1'
__updated__ = '180406'
__author__ = 'Haruka Yamashita'

chr_name_dict_all = {
    '1': 'YHet',
    '2': 'dmel_mitochondrion_genome',
    '3': '2L',
    '4': 'X',
    '5': '3L',
    '6': '4',
    '7': '2R',
    '8': '3R',
    '9': 'Uextra',
    '10': '2RHet',
    '11': '2LHet',
    '12': '3LHet',
    '13': '3RHet',
    '14': 'U',
    '15': 'XHet'
}

chr_name_dict_auto = {
    '3': '2L',
    '5': '3L',
    '6': '4',
    '7': '2R',
    '8': '3R',
    '10': '2RHet',
    '11': '2LHet',
    '12': '3LHet',
    '13': '3RHet',
}

mel_freq_group = {
    'frequency':{
        1: [1], 2: [2], 3: [3], 4:[4, 5], 5:[6, 7],
        6: [8, 9, 10], 7: [11, 12, 13], 8: [14]
    }
}

sim_freq_group = {
    'frequency':{
        1: [1], 2: [2], 3: [3], 4: [4, 5], 5: [6, 7], 6: [8, 9, 10],
        7: [11, 12, 13, 14], 8: [15, 16, 17, 18, 19, 20], 9:[21]
    }
}

ws_mutation_group = {
    'mutation':{
        'WS': ['AC', 'AG', 'TC', 'TG'],
        'SW': ['CA', 'CT', 'GA', 'GT'],
        'WW': ['AT', 'TA'],'SS': ['CG', 'GC']
    }
}
