#!/usr/bin/env python
# -*- coding: latin-1 -*-
import string
import textwrap
from os                     import linesep
from StringIO               import StringIO
from Bio                    import SeqIO
from Bio.SeqRecord          import SeqRecord
from Bio.Alphabet           import SingleLetterAlphabet
from sequence_filter        import seq_filter
from guess_alpha            import guess_alphabet
from Bio.Seq import Seq


class formatted_record:

    def __init__(self,raw_string,sequence_record,format="not defined"):

        assert type(sequence_record)    == SeqRecord
        assert type(format)             == str
        self.raw                        = raw_string #"".join([c for c in raw_string if 31<ord(c)<126 or ord(c) == 9])
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
    
    from Bio.Data               import IUPACData
    from Bio.Seq                import Seq
        
    permitted_letters ="".join(set( IUPACData.protein_letters +\
                                    IUPACData.extended_protein_letters +\
                                    IUPACData.ambiguous_dna_letters +\
                                    IUPACData.unambiguous_dna_letters +\
                                    IUPACData.ambiguous_rna_letters +\
                                    IUPACData.unambiguous_rna_letters +\
                                    IUPACData.extended_dna_letters))
    
    permitted_letters +=  permitted_letters.lower()
    
    sequences = []
    
    raw_string = textwrap.dedent(raw_string)

    handle = StringIO(raw_string)
    embl_sequences = list(SeqIO.parse(handle, "embl"))
    if embl_sequences:
        for seq_record in embl_sequences:
            filtered = "".join([char for char in seq_record.seq if char in permitted_letters])
            if filtered:
                seq_record.seq = Seq(filtered)
                sequences.append(formatted_record(raw_string,seq_record,"embl"))
    handle.close()

    handle = StringIO(raw_string)
    genbank_sequences = list(SeqIO.parse(handle, "genbank"))
    if genbank_sequences:
        for seq_record in genbank_sequences:
            filtered = "".join([char for char in seq_record.seq if char in permitted_letters])
            if filtered:
                seq_record.seq = Seq(filtered)           
                sequences.append(formatted_record(raw_string,seq_record,"genbank"))
        handle.close()

    handle = StringIO(raw_string)

    if not embl_sequences or genbank_sequences:
        handle = StringIO(raw_string)
        fasta_sequences = list(SeqIO.parse(handle, "fasta", SingleLetterAlphabet()))
        if fasta_sequences:
            for seq_record in fasta_sequences:                
                filtered = "".join([char for char in seq_record.seq if char in permitted_letters])
                if filtered:
                    seq_record.seq = Seq(filtered)
                    sequences.append(formatted_record(raw_string,seq_record,"fasta"))
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
        parsedseqs.extend(parse_string_into_formatted_records(seq))
    return parsedseqs

def parse_raw_sequence_into_fasta(raw_string):
    fasta_string = seq_filter(raw_string)
    fasta_string = ">sequence_"+str(len(fasta_string))+"bp\n" + fasta_string
    handle = StringIO(fasta_string)
    fasta_sequences = list(SeqIO.parse(handle, "fasta",SingleLetterAlphabet()))
    sequences=[]
    if fasta_sequences:
        for seq_record in fasta_sequences:
            sequences.append(formatted_record(fasta_string,seq_record,"raw"))
    handle.close()

    return sequences

if __name__=="__main__":
    
    '''
        >zzz
    aaa

    >xxx
    ccc

    LOCUS       xxx                        3 bp    DNA              UNK 01-JAN-1980
    DEFINITION  xxx
    ACCESSION   xxx
    VERSION     xxx
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 aaa
    //
    '''
    raw='''



>Seq3a
5�: ATCTCGGTTCTGACAGAAAAGCTTCCGGCGTTGGcagatagaaagtatg aattcaggccaaaattTAACGG AATTCAGCCATGGTTGTGAGTGTCAAAGACCCAGGATTTTCCGGCTAACAACGGTTC




'''

    new_sequences = parse_text_into_list_of_seqs(raw)

    for f_record in new_sequences:
            print "id  : ",f_record.record.id
            print "seq : ",f_record.record.seq
            print "alph: ",f_record.record.seq.alphabet
            print "form: ",f_record.format
            print "raw:\n",f_record.raw
            
            

 
