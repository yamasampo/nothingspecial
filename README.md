# NothingSpecial

A collection of Python codes I (Haruka Yamashita) use frequently everywhere. 

## General modules

### file_IO

Functions to read contents of several types of data formats, as follows. 

##### 1D list

```
itemnum: 3
item1
item2
item3
```

- "itemnum:" line, which indicates the number of items in the list, may or may not exist.

#### 2D list

```
>item1 key
item1 value - line1
item1 value - line2
item1 value - line3
>item2 key
item1 value - line1
>item3 key
...
```

- No assumption of the number of lines in a value field for one item

- "itemnum:" line, which indicates the number of items in the list, may or may not exist. (this is not requirement, but if itemnum line exist, the number is used as an expected number of items for testing if read number of items is the same.)

- Requires character(s) that indicates item divisions. ">" for the example above.

- Assumes the item divisor to be at the beginning of a line. 

- Optionally a value parser can be passed. If not given, value field will be a built-in list object. 

## For Biological Data

### classes

A collection of data structures.

#### FASTA file

Based on 2D list

#### Gene annotation data

- if NIG evogen-format of geneinfo file is given, read as 2D list
- if a standard gff file is given, read as tab separarted file maybe using pandas

### constants

A collection of constants. 

#### Nucleotide bases
