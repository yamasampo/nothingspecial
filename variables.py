
import os
import re
import pickle
import glob
import pandas as pd

from collections.abc import Mapping

from . import num, pathManage

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
    def __init__(self, csv_path, description=''):
        self.csv_path = csv_path
        self.table = pd.read_csv(csv_path)
        self.description = description

    def aadig(self, **kwargs):
        tmp_df = num.search_items_df(self.table, **kwargs)\
                    .loc[:, ['aa1', 'aa3', 'aadig']]
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

class Database(Mapping):
    """ This class inherits Mapping class. __iter__, __getitem__ and __len__ 
    functions are overwritten. """
    def __init__(self, df, description=''):
        self.df = df
        self.description = description
        
    def filter(self, sort_by='', ascending=True, **kwargs):
        '''
        Search rows which have specifies items from a given dataframe.
        Please pass key words for searching to **kwargs.
        For example, if you want to get items that is greater than equal (>=)
        100 in column "A", please specify **kwargs as "A=gte100". 
        Please see below for details.
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
                If you pass tuple to value, this function search and filter 
                items recursively.
        Dependencies
        ------------
            pandas
            re
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
            if isinstance(v, list): # "or"
                res_df_list = []
                for i in v:
                    res_df_list.append(f(res_df, k, i))
                res_df = pd.concat(res_df_list)
            if isinstance(v, tuple): # "and"
                res_df_list = []
                for i in v:
                    tmp_res_df = f(res_df, k, i)
                    res_df = pd.merge(res_df, tmp_res_df, how='inner')
            elif isinstance(v, str):
                res_df = f(res_df, k, v)
            elif isinstance(v, int):
                res_df = res_df[res_df[k] == v]
        if sort_by:
            res_df.sort_values(by=sort_by, ascending=ascending, inplace=True)
            
        return res_df
    
    def head(self, *kwargs):
        return self.df.head(*kwargs)

    def tail(self, *kwargs):
        return self.df.tail(*kwargs)

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

class DirMap(Database):
    '''This class inherits Database class. This is for pointing directories locating 
    at different branches withing folder tree but having same attributes 
    (ex. species, AA type, aadig).'''
    
    def __init__(self, filepat, top, description=''):
        self.df, self._d = self.get_DirMap(filepat, top)
        self.description = description
    
    def gen_dir(self, sort_by='', ascending=True, **kwargs):
        res_df = self.filter(sort_by, ascending, **kwargs)
        id_list = list(res_df.index)
        
        for i in id_list:
            yield i, self._d[i]

    def get_DirMap(self, filepat, top, description=''):
        i = 0
        dir_dict = {}
        tmp_df = None

        for dir_name in pathManage.gen_find_dir(filepat, top):
            i += 1
            dir_dict[i] = dir_name

            info_path = glob.glob(
                os.path.join(dir_name, 'data', '*_info.pickle'))[0]
            with open(info_path, 'rb') as f:
                info = pickle.load(f)

            key, value = zip(*sorted(info.items(), key=lambda x: x[0]))
            if i == 1:
                tmp_df = pd.DataFrame(columns=[], index=key)
            tmp_df[i] = list(value)
        
        info_df = tmp_df.T
        return info_df, dir_dict

class SeqDB(Database):
    '''This class inherits Database class. This is for pointing directories locating 
    at different branches withing folder tree but having same attributes 
    (ex. species, AA type, aadig).'''
    
    def __init__(self, df, seq_path='', description=''):
        super().__init__(df, description)
        if seq_path:
            self.load_seq(seq_path, format='pickle')
        else:
            self._d = {}
    
    def gen_seq(self, sort_by='', ascending=True, **kwargs):
        """ Generate registered nucleotide sequences. kwargs accepts options 
        for filtering CDS. 
        
        Returns
        -------
        i: int
            index of DataFrame
        seq_id: int
            key of sequence dictionary
        sequence: str
            nucleotide sequence registered in a dictionary
        """
        res_df = self.filter(sort_by, ascending, **kwargs)
        seq_id_list = res_df['seq_id'].tolist()
        id_list = list(res_df.index)
        
        for i, seq_id in zip(id_list, seq_id_list):
            yield i, seq_id, self._d[seq_id]

    def to_fasta(self, fasta_path, seq_name_encoder=None, itemnum=False, 
                 sort_by='', ascending=True, **kwargs):
        if not seq_name_encoder:
            seq_name_encoder = lambda x: str(x['info_id'])

        fasta_lines = []
        for _, item in enumerate(self.gen_seq(sort_by, ascending, **kwargs)):
            i, seq_id, seq = item
            seq_name = seq_name_encoder(self[i])
            fasta_lines.append('>{}\n{}'.format(seq_name, seq))

        with open(fasta_path, 'w') as f:
            if itemnum:
                print('itemnum: {}'.format(len(fasta_lines)), file=f)
            print('\n'.join(fasta_lines), file=f)


    def load_seq(self, seq_path, format='pickle'):
        if format == 'pickle':
            with open(seq_path, 'rb') as f:
                d = pickle.load(f)

        self._d = d

class ExprData(object):
    def __init__(self, data=None, version='', tissue_types={}):
        self.version = version
        self.tissue_type = tissue_types # e.g. constants.TISSUE_TYPES_a
        self.data = data
    
    @classmethod
    def load_data_from_table(cls, data_path, version='', tissue_types={}):
        data = pd.read_csv(data_path)

        return cls(data, version, tissue_types)

    def __repr__(self):
        return f'ver: {self.version}'
