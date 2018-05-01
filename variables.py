import pandas as pd
import os

__version__ = '1.3'
__updated__ = '180502'
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

mutation_compare_set = {
    'AG': ['AG', 'GA'],
    'TC': ['TC', 'CT'],
    'AC': ['AC', 'CA'],
    'TG': ['TG', 'GT'],
    'AT': ['AT', 'TA'],
    'WS': ['WS', 'SW']
}

cds_seq_df_path='/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/databases/cds/cds_seq_df_180329.csv'

int_seq_df_path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/databases/intron/int_seq_df_m18y22_180330.csv'

mel_site_df_path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/Dmel_ref_info/Dmel_info/site_type_info/site_type_df_180330.csv'

class MelExprData(object):
    def __init__(self):
        self.path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/Dmel_ref_info/Dmel_expression/tis_tab_m5_ast12_v6f3_pr_PMo_rnk_prt_per_expr b_HY.csv'
        self.version = '120904'
        self.tissue_type = {
            't1': 'Ad hindgut',
            't2': 'Ad midgut',
            't3': 'Ad male ac gl',
            't4': 'Ad brain',
            't5': 'Ad crop',
            't6': 'Lv wd fat body * cut *',
            't7': 'Ad head * cut *',
            't8': 'Lv wd Tubules * cut *',
            't9': 'Ad ovary',
            't10': 'Ad testis',
            't11': 'Ad wh fly',
            't12': 'Ad Salivary gl',
            't13': 'Ad carcass',
            't14': 'Ad TA ganglion * cut *',
            't15': 'Lv fd hindgut',
            't16': 'Lv fd midgut',
            't17': 'Lv fd Salivary gl',
            't18': 'Ad M spermatheca   * cut *',
            't19': 'Ad V spermatheca   * cut *',
            't20': 'Lv fd tubule',
            't21': 'Lv fd fat body',
            't22': 'Lv fd carcass',
            't23': 'Lv fd CNS',
            't24': 'Lv fd trachea',
            't25': 'S2 cells gr  * cut *',
            't26': 'Ad fat body',
            't27': 'Ad eye',
            't28': 'Ad heart',
            't29': 'Ad male Ej Dt',
            't30': 'Lv wh fd',
            't31': 'Ad female',
            't32': 'Ad male',
            't33': 'Sp mitotic',
            't34': 'Sp meiotic',
            't35': 'Sp p-meiotic',
            't36': 'embryo_0_2',
            't37': 'embryo_4_6',
            't38': 'embryo_8-10',
            't39': 'embryo_4_10',
            't40': 'larval_fed',
            't41': 'larval_st'
        }
        self.data = None

    def load_data(self):
        if self.data:
            raise Exception('Data is already loaded.')
        else:
            self.data = pd.read_csv(self.path)

    def __repr__(self):
        return 'ver: {0}\t file_name: {1}'.format(self.version, os.path.basename(self.path))
