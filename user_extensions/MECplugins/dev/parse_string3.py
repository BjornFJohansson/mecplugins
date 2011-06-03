#!/usr/bin/env python
# -*- coding: latin-1 -*-
import string
import textwrap
from os                     import linesep
from StringIO               import StringIO
from Bio                    import SeqIO
from Bio.SeqRecord          import SeqRecord
from Bio.Seq                import Seq
from Bio.Alphabet           import SingleLetterAlphabet
from sequence_filter        import seq_filter
from guess_alpha            import guess_alphabet

class fSeqRecord(SeqRecord):
    def __init__(self,r,f="not defined"):
        self.parsed_from_format=f
        SeqRecord.__init__(self,r)

a=Seq("aaa")
b=SeqRecord(a)
c=fSeqRecord(b,"fasta")




"""
print type(c)
print c.format
print c.seq"""

