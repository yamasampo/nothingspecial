import os
import sys
import re
import pandas as pd

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
