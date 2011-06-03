import string

def seq_filter(raw):

    remove=string.whitespace+string.digits+string.punctuation

    filtered_sequence = ''.join( [c for c in raw if c not in remove] )

    return filtered_sequence

if __name__=="__main__":

    raw='''
    1 aga3gca
108 atgt8acg'''

    tests=[]
    tests.append(raw)
    tests.append(seq_filter(raw))
    for test in tests:
        print test


