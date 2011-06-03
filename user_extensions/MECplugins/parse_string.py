#!/usr/bin/env python
# -*- coding: latin-1 -*-
import string
from os                     import linesep
from StringIO               import StringIO
from Bio                    import SeqIO
from Bio.SeqRecord          import SeqRecord
from Bio.Alphabet           import SingleLetterAlphabet
from sequence_filter        import seq_filter
from guess_alpha            import guess_alphabet


class formatted_record:

    def __init__(self,sequence_record,format="not defined"):

        assert type(sequence_record)    == SeqRecord
        assert type(format)             == str
        self.format                     = format
        self.record                     = sequence_record

        if isinstance(self.record.seq.alphabet, SingleLetterAlphabet):
            self.record.seq.alphabet = guess_alphabet(str(sequence_record.seq))

def parse_string_into_formatted_records(raw_string):
    '''
    This function parses a given string for sequences
    in fasta, embl and genbank format and  returns a
    list of formatted_record objects
    '''
    sequences = []

    handle = StringIO(raw_string)
    embl_sequences = list(SeqIO.parse(handle, "embl"))
    if embl_sequences:
        for seq_record in embl_sequences:
            sequences.append(formatted_record(seq_record,"embl"))
    handle.close()

    handle = StringIO(raw_string)
    genbank_sequences = list(SeqIO.parse(handle, "genbank"))
    if genbank_sequences:
        for seq_record in genbank_sequences:
            sequences.append(formatted_record(seq_record,"genbank"))
        handle.close()

    handle = StringIO(raw_string)

#    try: #parse seqs in tab format
#        tab_sequences = list(SeqIO.parse(handle, "tab"))
#        if tab_sequences:
#            for seq_record in tab_sequences:
#                seq_record.description = str(len(seq_record.seq))+" bp"
#                sequences.append(formatted_record(seq_record,"tab"))
#            handle.close()
#    except:
#        pass

    if not embl_sequences or genbank_sequences:
        handle = StringIO(raw_string)
        fasta_sequences = list(SeqIO.parse(handle, "fasta", SingleLetterAlphabet()))
        if fasta_sequences:
            for seq_record in fasta_sequences:
                sequences.append(formatted_record(seq_record,"fasta"))
        handle.close()

    else:
        return "only embl,genbank and fasta formats supported"

    return sequences


def parse_text_into_list_of_seqs(rawstring):
    '''

    '''
    seqs=[]
    lines=(rawstring).splitlines()
    index=0
    length=len(lines)
    while index<length:
        line=lines[index]
        if line:
            if line[0]==">":
                t=index+1
                while t<length:
                    if lines[t]:
                        t+=1
                    else:
                        break
                seqs.append("\n".join(lines[index:t]))
                index=t
            elif line[0:5]=="LOCUS" or line[0:2]=="ID":
                t=index+1
                while t<length:
                    if lines[t]!="//":
                        t+=1
                    else:
                        break
                seqs.append("\n".join(lines[index:t+1]))
                index=t
        index+=1
    parsedseqs=[]
    for seq in seqs:
        #print "--->",seq
        parsedseqs.extend(parse_string_into_formatted_records(seq))
    return parsedseqs

def parse_raw_sequence_into_fasta(raw_string):

    fasta_string = seq_filter(raw_string)
    fasta_string = ">Sequence_"+str(len(fasta_string))+"bp\n" + fasta_string
    sequences=[]
    handle = StringIO(fasta_string)
    fasta_sequences = list(SeqIO.parse(handle, "fasta"))
    if fasta_sequences:
        for seq_record in fasta_sequences:
            sequences.append(formatted_record(seq_record,"raw"))
    handle.close()

    return sequences

if __name__=="__main__":

    raw='''
====================================================================================
MumMX4_MunI_fw       Unmodified Oligos Ã  la Carte                         38.35 EUR
                     5'-aatgtgcgcggaacccctatttgtttatttttctaaatacaCaat
                     tGCGTACGCTGCAGGTCGAC-3'  HPS 0.05

MumMX4rv             Unmodified Oligos Ã  la Carte                         37.76 EUR
                     5'-atttatcagggttattgtctcatgagcggatacatatttgaaGCA
                     TAGGCCACTAGTGGATCTG-3'  HPS 0.05

                     Printed Synth. Report                                 0.00 EUR
====================================================================================

>482_PrimerFwdACLB1 (32-mer)
'''

    new_sequences = parse_mwg_primers_into_formatted_records(raw)

    if new_sequences:
        for f_record in new_sequences:
            print "id  : ",f_record.record.id
            print "seq : ",f_record.record.seq
            print "alph: ",f_record.record.seq.alphabet
            print "form: ",f_record.format
            print

 
