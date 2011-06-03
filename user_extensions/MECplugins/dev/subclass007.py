from Bio.Alphabet.IUPAC import ambiguous_dna
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

#Subclassing of the SeqRecord class

class Primer(SeqRecord):
    def __init__(self, seq=None, annealing_position=None, *args, **kwargs):
        
        self.annealing_position = annealing_position
        
        if isinstance(seq,Seq):
            seq.alphabet = ambiguous_dna  
            SeqRecord.__init__(self, seq, *args, **kwargs)
        
        elif isinstance(seq,str):
            SeqRecord.__init__(self,Seq(seq,ambiguous_dna), *args, **kwargs)           
            
        elif isinstance(seq,SeqRecord):
            SeqRecord.__init__(self,
                               seq.seq,
                               seq.id,
                               seq.name,
                               seq.description,
                               seq.dbxrefs,
                               seq.features,
                               seq.annotations,
                               seq.letter_annotations)
        else:
            raise TypeError("the seq property needs to be a string, a Seq object or a SeqRecord object")
            

               
a = Primer("aaa",11,"id1","name1")

b = Primer(Seq("ccc"),22,"id2","name2")

c = Primer(SeqRecord(Seq("ttt")),33)


print a.annealing_position
print b.annealing_position
print c.annealing_position

print a.reverse_complement().seq
print b.reverse_complement().seq
print c.reverse_complement().seq






