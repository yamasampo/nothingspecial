import os
import sys
import re
import pandas as pd
import pickle

def get_fasta_df(fasta_path):
    ## dataframe for mfa database
    # get paths
    dname = os.path.basename(os.path.dirname(fasta_path))
    fname = os.path.basename(fasta_path)

    # collect data
    seq_name = ''
    seq=''
    dname_list = []
    fname_list = []
    seqname_list = []
    seq_list = []

    with open(fasta_path, 'r') as f:
        aligned = 0

        for line in f.readlines():

            if line.startswith('>'):
                seq_name = line[1:-1]

            else:
                seq = line.rstrip()

                dname_list.append(dname)
                fname_list.append(fname)
                seqname_list.append(seq_name)
                seq_list.append(seq)

    # create dataframe
    fasta_df = pd.DataFrame({'dir_name': dname_list,
                           'file_name': fname_list,
                           'seqname': seqname_list,
                           'seq': seq_list
                           })
    # rearrange columns
    return fasta_df.ix[:,['dir_name',
                          'file_name',
                          'seqname',
                          'seq']]

def to_filelist(dir_path):

    l1 = os.listdir(dir_path)
    l2= [a for a in l1 if not a.startswith('.')]
    flist = [a for a in l2 if not a.startswith('0')]

    with open(os.path.join(dir_path, '0.filelist'), 'w') as f:
        print('itemnum: '+str(len(flist)), file=f)
        print('\n'.join(flist), file=f)


def get_file_list(path, avoid='itemnum', prefix=None, sufix=None):

    fname = ''
    flist = []

    with open(path, 'r') as f:

        for line in f.readlines():

            if line.startswith(avoid):
                continue

            if prefix:
                if sufix:
                    fname = prefix+line.rstrip()+sufix
                else:
                    fname = prefix+line.rstrip()

            else:
                fname = line.rstrip()

            flist.append(fname)

    print('{0}: # files is {1}'.format(os.path.basename(os.path.dirname(path)), len(flist)))

    return flist

def read_big_pickle(pickle_path):

    bytes_in = bytearray(0)
    max_bytes = 2**31 - 1
    input_size = os.path.getsize(pickle_path)

    with open(pickle_path, 'rb') as f_in:

        for _ in range(0, input_size, max_bytes):
            bytes_in += f_in.read(max_bytes)

    return pickle.loads(bytes_in)

def write_big_pickle(pickle, out_path):

    n_bytes = sys.getsizeof(pickle)
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(pickle)

    with open(out_path, 'wb') as f_out:

        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])
