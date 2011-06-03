#!/usr/bin/python

from Bio.Restriction import *
from Bio.Seq import Seq, reverse_complement
from Bio.Alphabet.IUPAC import IUPACAmbiguousDNA



amb = IUPACAmbiguousDNA()
myseq = Seq('TTTTGGATCCAAAAGGTACCTTTTCCCGGGAAAA', amb)

sit=BamHI.search(myseq)
a=BamHI.size-BamHI.fst5-1
b=BamHI.fst5+1

for s in sit:
    print myseq[:s+a], myseq[s-b:]

sit=KpnI.search(myseq)
a=KpnI.size-KpnI.fst5-1
b=KpnI.fst5+1

for s in sit:
    print myseq[:s+a], myseq[s-b:]

sit=SmaI.search(myseq)
a=SmaI.size-SmaI.fst5-1
b=SmaI.fst5+1

for s in sit:
    print myseq[:s+a], myseq[s-b:]


