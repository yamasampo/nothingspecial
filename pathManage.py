import os
import fnmatch
import gzip
import bz2
import re

__version__ = '1.1'
__author__ = 'Haruka Yamashita'

def gen_find_file(filepat, top):
    '''Find all filenames in a directory tree that match a shell wildcard pattern'''
    for path, _, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def gen_find_dir(filepat, top):
    '''Find all directory names in a directory tree that contain files matching a shell wildcard pattern'''
    for path, _, filelist in os.walk(top):
        if len(fnmatch.filter(filelist, filepat)) > 0:
            yield path

def gen_opener(filenames):
    '''Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.'''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    '''Chain a sequence of iterators together into a single sequence.'''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''Look for a regex pattern in a sequence of lines'''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line
