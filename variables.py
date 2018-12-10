import pandas as pd
import os, re, pickle, glob
from myBasic import num, pathManage
from collections.abc import Mapping

__version__ = '2.0'
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

class MutationCompSet(object):
    def __init__(self):
        self.comp_dict = {
            'AG': ['AG', 'GA'],
            'TC': ['TC', 'CT'],
            'AC': ['AC', 'CA'],
            'TG': ['TG', 'GT'],
            'GC': ['GC', 'CG'],
            'AT': ['AT', 'TA'],
            'WS': ['WS', 'SW'],
            'SS': ['SS', 'WW']
        }
    def get_key_mut(self, mutation):
        if mutation == 'GA' or mutation == 'AG':
            return 'AG'
        elif mutation == 'CT' or mutation == 'TC':
            return 'TC'
        elif mutation == 'CA' or mutation == 'AC':
            return 'AC'
        elif mutation == 'GT' or mutation == 'TG':
            return 'TG'
        elif mutation == 'CG' or mutation == 'GC':
            return 'GC'
        elif mutation == 'TA' or mutation == 'AT':
            return 'AT'
        elif mutation == 'SW' or mutation == 'WS':
            return 'WS'
        elif mutation == 'WW' or mutation == 'SS':
            return 'SS'

    def __repr__(self):
        return str(self.comp_dict)

class GeneticCode(object):
    def __init__(self):
        self.__version__ = '1.1'
        self.__updated__ = '180612'
        self.__author__ = 'Haruka Yamashita'
        self.csv_path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/1_Data_Analysis/_data/genetic_code_coddig_aadig_180611.csv'
        self.bases = ['T', 'C', 'A', 'G']
        self.table = pd.read_csv(self.csv_path)

    def aadig(self, **kwargs):
        tmp_df = num.search_items_df(self.table, **kwargs).loc[:, ['aa1', 'aa3', 'aadig']]
        tmp_df.drop_duplicates(inplace=True)
        if len(tmp_df.index) != 1:
            raise Exception('Given keyword arguments cannot specify aa')
        return tmp_df.iloc[0]['aadig']

    def aa1(self, dig):
        return num.search_items_df(self.table, aadig=dig).iloc[0]['aa1']

    def aa3(self, dig):
        return num.search_items_df(self.table, aadig=dig).iloc[0]['aa3']

    def codon(self, dig):
        return num.search_items_df(self.table, coddig=dig).iloc[0]['codon']

    def codons(self, **kwargs):
        return num.search_items_df(self.table, **kwargs)['codon'].tolist()

    def filter_table(self, **kwargs):
        return num.search_items_df(self.table, **kwargs)

    def get_2f_mutation(self, cod_type, out='key', **kwargs):
        # filter table by codon type (2f20cD, 2f10, ...)
        kwargs[cod_type] = 1
        table = self.filter_table(**kwargs)
        # get a list of codons
        codons = num.search_items_df(table, **kwargs)['codon'].tolist()
        # synonymous site mutation
        mutation = codons[0][2] + codons[1][2]
        # search a key of mutation comparison set
        mutcomp = MutationCompSet()
        key = mutcomp.get_key_mut(mutation)
        if out=='key':
            return key
        elif out=='set':
            return mutcomp.comp_dict[key]

    def __repr__(self):
        return self.table


cds_seq_df_path='/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/databases/cds/cds_seq_df_180329.csv'

int_seq_df_path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/databases/intron/int_seq_df_m18y22_180330.csv'

mel_site_df_path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/011_Programming/_data/Dmel_ref_info/Dmel_info/site_type_info/site_type_df_180330.csv'

class Database(Mapping):
    def __init__(self, df, description=''):
        self.df = df
        self.description = description
        
    def filter(self, sort_by='', ascending=True, **kwargs):
        '''
        Search rows which have specifies items from a given dataframe.
        Please pass key words for searching to **kwargs.
        For example, if you want to get items that is greater than equal (>=)
        100 in column "A", please specify **kwargs as "A=gte100". Please see below for details.
        If nothing passed to **kwargs, return input dataframe.
        Paramters
        ---------
            df: DataFrame (pandas)
                input dataframe
            **kwargs:
                key is for column, value is for filtering values (items)
                You can use indicators below for filtering way.
                "gt" for ">"
                "gte" for ">="
                "lt" for "<"
                "lte" for "<="
                "ne" for "!="
                "c/" for "contains"
                "" for "=="
                If you pass tuple to value, this function search and filter items recursively.
        '''
        res_df = self.df
        def f(res_df, k, v):
            if isinstance(v, str):
                if v == '*':
                    pass
                elif re.search('^gt\d+', v):
                    v = float(re.search('^gt(\d+\.*\d*)$', v).group(1))
                    res_df = res_df[res_df[k] > v]
                elif re.search('^gte\d+', v):
                    v = float(re.search('^gte(\d+\.*\d*)$', v).group(1))
                    res_df = res_df[res_df[k] >= v]
                elif re.search('^lt\d+', v):
                    v = float(re.search('^lt(\d+\.*\d*)$', v).group(1))
                    res_df = res_df[res_df[k] < v]
                elif re.search('^lte\d+', v):
                    v = float(re.search('lte(\d+\.*\d*)$', v).group(1))
                    res_df = res_df[res_df[k] <= v]
                elif re.search('^ne\d+', v):
                    v = float(re.search('ne(\d+\.*\d*)$', v).group(1))
                    res_df = res_df[res_df[k] != v]
                elif re.search('^c\/', v):
                    v = re.search('^c\/(.+)\/$', v).group(1)
                    res_df = res_df[res_df[k].str.contains(v)]
                elif re.search('^nc\/', v):
                    v = re.search('^nc\/(.+)\/$', v).group(1)
                    res_df = res_df[~res_df[k].str.contains(v)]
                else:
                    res_df = res_df[res_df[k] == v]
            else:
                res_df = res_df[res_df[k] == v]
            return res_df

        for k,v in kwargs.items():
            if isinstance(v, (tuple, list)):
                res_df_list = []
                for i in v:
                    res_df_list.append(f(res_df, k, i))
                res_df = pd.concat(res_df_list)
            elif isinstance(v, str):
                res_df = f(res_df, k, v)
            elif isinstance(v, int):
                res_df = res_df[res_df[k] == v]
        if sort_by:
            res_df.sort_values(by=sort_by, ascending=ascending, inplace=True)
            
        return res_df
    
    def head(self, *kwargs):
        return self.df.head(*kwargs)

    def __len__(self):
        return len(self.df.index)
    
    def __iter__(self):
        return self.df.iterrows()
    
    def __getitem__(self, key):
        if key == '*':
            return self.df
        else:
            return self.df.loc[key, :]
        # elif isinstance(key, (tuple, list)):
        #     for k in key:
        #         yield self.df.loc[k, :]
    
    def __repr__(self):
        return '<{name}: {desc} ({size} records)>'.format(
            name=type(self).__name__, desc=self.description, size=self.__len__()
        )

class SFSDirMap(Database):
    '''This class inherits Database class. This is for pointing directories locating 
    at different branches withing folder tree but having same attributes 
    (ex. species, AA type, aadig).'''
    
    def __init__(self, filepat, top, description=''):
        self.df, self._d = self.get_SFSDirMap(filepat, top)
        self.description = description
    
    def gen_sfs_dir(self, sort_by='', ascending=True, **kwargs):
        res_df = self.filter(sort_by, ascending, **kwargs)
        id_list = list(res_df.index)
        
        for i in id_list:
            yield i, self._d[i]

    def get_SFSDirMap(self, filepat, top, description=''):
        i = 0
        dir_dict = {}
        tmp_df = None

        for sfs_dir in pathManage.gen_find_dir(filepat, top):
            i += 1
            dir_dict[i] = sfs_dir

            info_path = glob.glob(os.path.join(sfs_dir, 'data', '*_info.pickle'))[0]
            with open(info_path, 'rb') as f:
                info = pickle.load(f)

            key, value = zip(*sorted(info.items(), key=lambda x: x[0]))
            if i == 1:
                tmp_df = pd.DataFrame(columns=[], index=key)
            tmp_df[i] = list(value)
        
        info_df = tmp_df.T
        return info_df, dir_dict

class MelExprData(object):
    def __init__(self):
        self.path = '/Volumes/1TB_4TB_GG/Dropbox/Documents_DB/01_Projects/1_Data_Analysis/_data/Dmel_ref_info/Dmel_expression/tis_tab_m5_ast12_v6f3_pr_PMo_rnk_prt_per_expr b_HY.csv'
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
