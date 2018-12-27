import os, sys, re, pickle
import pandas as pd
from myBasic import num

__author__ = 'Haruka Yamashita'

def parse_fasta(fasta_path):
    '''Parse a FASTA file and return a dictionary'''
    
    fasta = {}
    seq_name = ''
    tmp_seq = []
    
    with open(fasta_path, 'r') as f:
        for l in f:
            if l.startswith('>'):
                if seq_name:
                    fasta[seq_name] = ''.join(tmp_seq)
                    seq_name = ''
                    tmp_seq = []
                seq_name = l[1:-1]
                
            else:
                tmp_seq.append(l[:-1])
    if seq_name:
        fasta[seq_name] = ''.join(tmp_seq)
        
    return fasta

def to_fasta(fasta, out_path):
    '''Save fasta object as a FASTA file'''
    with open(out_path, 'w') as f:
        for seq_name, seq in fasta.items():
            print('>' + seq_name, file=f)
            print(seq, file=f)

def parse_fasta_in_dir(dir_path, filelist_name='0.filelist'):
    '''Parse Fasta files in a given directory'''
    flist = text.get_file_list(path=os.path.join(dir_path, filelist_name))
    fasta_dict = {}
    
    for file_name in flist:
        fasta_path = os.path.join(dir_path, file_name)
        fasta = parse_fasta(fasta_path)
        fasta_dict[file_name] = fasta
        
    return fasta_dict

def fasta_parser(fasta_path):
    ## dataframe for mfa database
    # get paths
    dname = os.path.basename(os.path.dirname(fasta_path))
    fname = os.path.basename(fasta_path)
    # collect data
    seq_name = ''
    dname_list = []
    fname_list = []
    seqname_list = []
    seq_list = []
    tmp_seq = []

    with open(fasta_path, 'r') as f:
        # aligned = 0
        for line in f.readlines():
            if line.startswith('>'):
                if seq_name:
                    dname_list.append(dname)
                    fname_list.append(fname)
                    seqname_list.append(seq_name)
                    seq_list.append(''.join(tmp_seq))

                seq_name = line[1:-1].split(' ')[0]
                tmp_seq = []
            else:
                tmp_seq.append(line[:-1])
        if seq_name:
            dname_list.append(dname)
            fname_list.append(fname)
            seqname_list.append(seq_name)
            seq_list.append(''.join(tmp_seq))

    # create dataframe
    fasta_df = pd.DataFrame({'dir_name': dname_list,
                           'file_name': fname_list,
                           'seqname': seqname_list,
                           'seq': seq_list
                           })
    print('{0} items in {1}.'.format(len(fasta_df.index), fasta_path))
    # rearrange columns
    return fasta_df.ix[:,['dir_name',
                          'file_name',
                          'seqname',
                          'seq']]

def fastq_parser(fastq_path):
    '''Returns a DataFrame(pandas) object.
    fastq_parser assumes that a sequence has 4 lines and there is no empty line.
    '''
    name_list = []
    seq_list = []
    name2_list = []
    qual_list = []
    n = 1

    with open(fastq_path, 'r') as f:
        for l in f.readlines():
            if n == 1:
                name_list.append(l[:-1])
                n += 1
            elif n == 2:
                seq_list.append(l[:-1])
                n += 1
            elif n == 3:
                name2_list.append(l[:-1])
                n += 1
            elif n == 4:
                qual_list.append(l[:-1])
                n = 1
    df = pd.DataFrame({'seqname': name_list,
                       'seq': seq_list,
                       'qualname': name2_list,
                       'qual': qual_list})
    print('{0} items in {1}.'.format(len(df.index), fastq_path))
    return df.ix[:, ['seqname', 'seq', 'qualname', 'qual']]

def seq_length(fasta_df, seqname):

    tmp_df = num.search_items_df(fasta_df, seqname=seqname)

    if len(tmp_df.index) != 1:
        raise Exception('data cannot be specified by seqname "{}".'.format(seqname))

    return len(tmp_df['seq'].iloc[0])

def to_fastq(fastq, file_name):
    '''
    Write to a fastq file.
    Parameters
    ----------
        fastq: DataFrame
            parsed fastq file to a DataFrame
        file_name: str
            data will be written in this file.
    '''
    fastq_lines = []
    cnt = 0

    for i, row in fastq.iterrows():
        fastq_lines.append(row['seqname'])
        fastq_lines.append(row['seq'])
        fastq_lines.append(row['qualname'])
        fastq_lines.append(row['qual'])

        cnt += 1
        if cnt % 1000 == 0:
            print('.', end='', flush=True)

    with open(file_name, 'w') as f:
        print('\n'.join(fastq_lines), file=f)
        print(' Written in {}'.format(file_name))

def to_filelist(dir_path):
    '''Return a file list in a given directory'''
    l1 = os.listdir(dir_path)
    l2= [a for a in l1 if not a.startswith('.')]
    flist = [a for a in l2 if not a.startswith('0')]

    with open(os.path.join(dir_path, '0.filelist'), 'w') as f:
        print('itemnum: '+str(len(flist)), file=f)
        print('\n'.join(flist), file=f)
    return flist

def get_file_list(path, avoid=['itemnum'], prefix='', sufix=''):
    '''
    Returns a list of file names that are written in a given file.
    Parameter
    ---------
        path: str
            a path to a file of file name list
        avoid: str
            a word you do not want to include in output file list
        prefix: str
            If "prefix" is specified, this word will be contained
            at the beginning of all file names in output list.
        sufix: str
            If "sufix" is specified, this word will be contained
            at the end of all file names in output list.
    Return
    ------
        flist: list
            a list that contains all file names listed in a given file.
    '''
    fname = ''
    flist = []
    with open(path, 'r') as f:
        for line in f:
            bad = 0

            for bad_char in avoid:
                if line.startswith(bad_char):
                    bad += 1
            if bad > 0:
                continue
                
            if prefix:
                if sufix:
                    fname = prefix+line.rstrip()+sufix
                else:
                    fname = prefix+line.rstrip()
            elif sufix:
                fname = line.rstrip()+sufix
            else:
                fname = line.rstrip()
            flist.append(fname)
    # print('{0} items in {1}'.format(len(flist), path))
    return flist

def match_2lists(query_list, ref_list, unmatch=False):
    '''
    Returns a list containing identical items between two given lists and
    a list containing items not in the reference list.
    '''
    match_list = []
    unmatch_list = []
    auxDict = dict.fromkeys(ref_list)

    for item in query_list:
        if item in auxDict:
            match_list.append(item)
            auxDict[item] = None
        else:
            unmatch_list.append(item)
            auxDict[item] = None
    if unmatch:
        return match_list, unmatch_list
    else:
        return match_list

def sort_strings_by_num(data):
    '''
    Sort a series of strings by embedded numbers that are in strnigs.
    '''
    re_digits=re.compile(r'(\d+)')

    def embedded_num(s):
        pieces = re_digits.split(s)
        pieces[1::2] = map(int, pieces[1::2])
        return pieces

    aux = [(embedded_num(s), s) for s in data]
    aux.sort()
    return [s for __, s in aux]

def get_key_by_value(dict, value):
    for k, v in dict.items():
        if v == value:
            return k

def read_big_pickle(pickle_path, max_bytes=2**31-1):

    bytes_in = bytearray(0)
    input_size = os.path.getsize(pickle_path)

    with open(pickle_path, 'rb') as f_in:

        for _ in range(0, input_size, max_bytes):
            bytes_in += f_in.read(max_bytes)

    return pickle.loads(bytes_in)

def write_big_pickle(obj, out_path):

    n_bytes = sys.getsizeof(obj)
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(obj)

    with open(out_path, 'wb') as f_out:

        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])

def pkg_version(pkg):
    import pkg_resources
    for dist in pkg_resources.working_set:
        if dist.project_name == pkg:
            print(dist.project_name, dist.version)

def get_last_dir_name(path):
    if os.path.basename(path) == '':
        get_last_dir_name(path[:-1])
    else:
        return os.path.basename(path)

def parse_HASeqFile(path):
    item_cnt = 0
    fasta_dict = {}
    gene_name = ''
    cds_len = 0

    with open(path, 'r') as f:
        for line in f:
            if re.match(r'\d+$', line[:-1]):
                continue
            
            if line.startswith('/*'):
                continue
            
            if line.startswith('>'):
                gene_name = line[1:-1]
                
            elif line.startswith('cod'):
                cds_len = int(line[:-1].split(':')[1])
                
            elif gene_name != '' and cds_len > 0:
                if re.match(r'[ATGC]', line):
                    seq = line.rstrip()[:-1]
                    assert cds_len == len(seq), gene_name
                    
                    fasta_dict[gene_name] = seq
                    item_cnt += 1
                    gene_name = ''
                    cds_len = 0

    assert len(fasta_dict) == item_cnt, 'Incorrect item number'
    return fasta_dict
    