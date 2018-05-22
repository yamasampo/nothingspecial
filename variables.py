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
    'AG': ['GA', 'AG'],
    'TC': ['CT', 'TC'],
    'AC': ['CA', 'AC'],
    'TG': ['GT', 'TG'],
    'AT': ['AT', 'TA'],
    'WS': ['SW', 'WS'],
    'SS': ['WW', 'SS']
}

class GeneticCode(object):
    def __init__(self):
        ####
        self.__version__ = '0.1'
        self.__updated__ = '180522'
        self.__author__ = 'Haruka Yamashita'
        ####
        self.csv_path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/genetic_code_coddig_aadig_180522.csv'
        self.bases = ['A', 'C', 'G', 'T']
        self.cod_dict = {
            1: 'TTC', 2: 'TTT', 3: 'TTA', 4: 'TTG', 5: 'CTA', 6: 'CTC', 7: 'CTG', 8: 'CTT',
            9: 'ATA', 10: 'ATC', 11: 'ATT', 12: 'ATG', 13: 'GTA', 14: 'GTC', 15: 'GTG', 16: 'GTT',
            17: 'TCA', 18: 'TCC', 19: 'TCG', 20: 'TCT', 21: 'CCA', 22: 'CCC', 23: 'CCG', 24: 'CCT',
            25: 'ACA', 26: 'ACC', 27: 'ACG', 28: 'ACT', 29: 'GCA', 30: 'GCC', 31: 'GCG', 32: 'GCT',
            33: 'TAC', 34: 'TAT', 35: 'TAA', 36: 'TAG', 37: 'CAC', 38: 'CAT', 39: 'CAA', 40: 'CAG',
            41: 'AAC', 42: 'AAT', 43: 'AAA', 44: 'AAG', 45: 'GAC', 46: 'GAT', 47: 'GAA', 48: 'GAG',
            49: 'TGC', 50: 'TGT', 51: 'TGA', 52: 'TGG', 53: 'CGA', 54: 'CGC', 55: 'CGG', 56: 'CGT',
            57: 'AGA', 58: 'AGG', 59: 'AGC', 60: 'AGT', 61: 'GGA', 62: 'GGC', 63: 'GGG', 64: 'GGT'
        }
        self.codons = list(self.cod_dict.values())
        self.coddigits = list(self.cod_dict.keys())
        self.aa_dict = {
            -9: ('-', 'term'), 1: ('F', 'Phe'), 2: ('L', 'Leu'), 3: ('I', 'Ile'),
            4: ('M', 'Met'), 5: ('V', 'Val'), 6: ('S', 'Ser4'), 7: ('P', 'Pro'),
            8: ('T', 'Thr'), 9: ('A', 'Ala'), 10: ('Y', 'Tyr'), 11: ('-', 'term'),
            12: ('H', 'His'), 13: ('Q', 'Gln'), 14: ('N', 'Asn'), 15: ('K', 'Lys'),
            16: ('D', 'Asp'), 17: ('E', 'Glu'), 18: ('C', 'Cys'), 19: ('W', 'Trp'),
            20: ('R', 'Arg'), 21: ('G', 'Gly'), 22: ('Z', 'Ser2')
        }
        self.aadigits = list(self.aa_dict.keys())
        self.aa1 = list(zip(*list(self.aa_dict.values())))[0]
        self.aa3 = list(zip(*list(self.aa_dict.values())))[1]
        self.aa_cod_dict = {
            -9: [35, 36], 1: [1, 2], 2: [5, 6, 7, 8, 3, 4], 3: [9, 10, 11],
             4: [12], 5: [13, 14, 15, 16], 6: [17, 18, 19, 20], 7: [21, 22, 23, 24],
             8: [25, 26, 27, 28], 9: [29, 30, 31, 32], 10: [33, 34], 11: [51],
             12: [37, 38], 13: [39, 40], 14: [41, 42], 15: [43, 44],
             16: [45, 46], 17: [47, 48], 18: [49, 50], 19: [52],
             20: [57, 58, 53, 54, 55, 56], 21: [61, 62, 63, 64], 22: [59, 60]
        }

    def load_csv(self):
        import pandas as pd
        self.df = pd.read_csv(csv_path, **kwargs)

    def get_coddigit(self, codon):
        from myBasic import text
        return text.get_key_by_value(dict=self.cod_dict, value=codon)

    def get_aadigit(self, aa):
        for k,v in self.aa_dict.items():
            if aa in v:
                return k
            else:
                raise KeyError('{} is not in "aa1" or "aa3" columns.'.format(aa))

    def get_2f_codon(self, opt, csv_path=''):
        from myBasic import num
        if 'df' not in self.__dir__():
            self.load_csv(csv_path)
        return num.search_items_df(self.df, opt=1)

    def get_4f_codon(self, csv_path=''):
        from myBasic import num
        col='4f6'
        if 'df' not in self.__dir__():
            self.load_csv(csv_path)
        return num.search_items_df(self.df, col=1)

    def translate(self, dna):
        return protein

    def __repr__(self):
        return 'GeneticCode object: v.{} {} {}'.format(self.__version__, self.__updated__, self.__author__)


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
