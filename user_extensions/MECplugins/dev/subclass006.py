from Bio.Alphabet.IUPAC import ambiguous_dna
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

#Subclassing of of the SeqRecord class

class Primer(SeqRecord):
    def __init__(self, seq, annealing_position=None, *args, **kwargs):
        assert isinstance(seq,Seq)
        seq.alphabet = ambiguous_dna  
        SeqRecord.__init__(self, seq, *args, **kwargs)
        self.annealing_position = annealing_position

a = SeqRecord(Seq("aaa"),"id1","name1")

print type(a)

b= Primer(Seq("aaa"),33,"id2","name2")

print b.annealing_position

print b.reverse_complement().seq











