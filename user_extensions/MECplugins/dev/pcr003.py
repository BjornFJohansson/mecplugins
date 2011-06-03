import                              string
import                              re
from os                             import linesep as ls
from math                           import log10,log
from Bio                            import SeqIO
from Bio.Seq                        import Seq, reverse_complement
from Bio.Alphabet.IUPAC             import unambiguous_dna
from Bio.SeqRecord                  import SeqRecord
from cStringIO                      import StringIO
from parse_string2                  import parse_string_into_formatted_records
from Bio.SeqUtils                   import GC
from Bio.SeqUtils.MeltingTemp       import Tm_staluc

def annealing_positions(first_sequence,second_sequence,direction="forward",limit=13):
    
    assert type(direction) == str
    assert type(limit)     == int
    
    second_sequence=str(second_sequence).lower()
    three_end_part_of_first_sequence = str(first_sequence[-limit:]).lower()

    if direction =="forward":
        regex = '(?='+three_end_part_of_first_sequence+')'
        offset = limit
    elif direction =="reverse":
        regex = '(?='+reverse_complement(three_end_part_of_first_sequence)+')'
        offset=0
    else:
        raise Exception
    
    return [m.start()+offset for m in re.finditer(regex,second_sequence)]

class Primer(Seq):
    def __init__(self, primer, annealing_position):
        Seq.__init__(self, str(primer), unambiguous_dna)
        self.annealing_position = annealing_position

class ForwardPrimer(Primer):
    def __init__(self, primer, annealing_position):
        Primer.__init__(self, primer, annealing_position)

class ReversePrimer(Primer):
    def __init__(self, primer, annealing_position):
        Primer.__init__(self, primer, annealing_position)

class Amplicon:
    def __init__(self,forward_primer, reverse_primer, product_size, product_sequence):
        self.forward_primer   = forward_primer
        self.reverse_primer   = reverse_primer
        self.product_size     = product_size
        self.product_sequence = product_sequence
        self.forward_covered_template = "aaa"
        self.reverse_covered_template = "bbb"
        
        #self.flankup                    = flankup
        #self.flankdn                    = flankdn

class anneal:

    def __init__(self, primers, template, topology="linear", homology_limit=13):

        assert type(primers)                            == list
        assert type(template)                           == SeqRecord

        self.template = template
        self.homology_limit = homology_limit
        
        if topology=="circular":
            self.circular_template=True
        else:
            self.circular_template=False       

        assert(template.seq) # check if empty template record

        for primer in primers:
            assert(primer.seq) # check if empty sequence records in primers
            
        self.fwd_primers = []
        self.rev_primers = []    
   
        for primer in primers:  # add annealing forward and reverse primers
            
            annealing_positions_on_watson_strand = annealing_positions(primer.seq, template.seq,"forward",homology_limit)
            for position in annealing_positions_on_watson_strand:
                self.fwd_primers.append(ForwardPrimer(primer.seq, position))
                
            annealing_positions_on_crick_strand = annealing_positions(primer.seq, template.seq,"reverse",homology_limit)
            for position in annealing_positions_on_crick_strand:
                self.rev_primers.append(ReversePrimer(primer.seq, position))


    def define_amplicons(self,fprim="all",rprim="all"):
        amplicons,sizes = [],[]
        for forward_primer in self.fwd_primers:
            for reverse_primer in self.rev_primers[::-1]:
                
                product_size = len(forward_primer)+len(reverse_primer)+reverse_primer.annealing_position-forward_primer.annealing_position
                sizes.append(product_size)
                product_sequence = forward_primer + self.template[forward_primer.annealing_position:reverse_primer.annealing_position] + reverse_primer.reverse_complement()
                amplicons.append(Amplicon(forward_primer, reverse_primer, product_size, product_sequence))
        
        self.amplicons = sorted(amplicons,key=lambda Amplicon: Amplicon.product_size)
        return sorted(sizes)
    
    def detailed_figure(self,alternative_image=2):

            forward_annealing_pins   = "|"*len(self.forward_annealing_zone)
            reverse_annealing_pins   = "|"*len(self.reverse_annealing_zone)

            tmf = Tm_staluc(str(self.forward_annealing_zone))
            tmr = Tm_staluc(str(self.reverse_annealing_zone))

            K = 0.050 # 50 mM
            L = len(self.product)
            GC_prod=GC(str(self.product.seq))
            tmp = 81.5 + 0.41*GC_prod + 16.6*log10(K) - 675/L
            tml = min([tmf,tmr])
            ta = 0.3*tml+0.7*tmp-14.9

            f = ""

            if alternative_image==1:
                f += str("5"+self.forward_annealing_zone).rjust(1+len(self.forward_primer.primer.seq)) + "..."
                f += self.reverse_annealing_zone + "3\n"
                f += " "+reverse_annealing_pins.rjust(len(self.forward_primer.primer.seq)+3+len(self.reverse_annealing_zone)) + "\n"
                f += str("3"+self.reverse_primer.primer.seq[::-1]).rjust(1+len(self.forward_primer.primer.seq)+3+len(self.reverse_primer.primer.seq)) +"5\n"
                f +=  "5"+self.forward_primer.primer.seq + "3\n"
                f += " "+forward_annealing_pins.rjust(len(self.forward_primer.primer.seq)) + "\n"
                f += str("3"+self.forward_annealing_zone.complement()).rjust(1+len(self.forward_primer.primer.seq)) + "..."
                f += self.reverse_annealing_zone.complement() + "5\n"

            if alternative_image==2:
                f += "5"+self.forward_primer.primer.seq + "3\n"
                f += " "+forward_annealing_pins.rjust(len(self.forward_primer.primer.seq)) + " tm "+str(round(tmf,1))+"C\n"
                f += str("5"+self.forward_annealing_zone).rjust(1+len(self.forward_primer.primer.seq)) + "..."
                f += self.reverse_annealing_zone + "3\n"
                f += str("3"+self.forward_annealing_zone.complement()).rjust(1+len(self.forward_primer.primer.seq)) + "..."
                f += self.reverse_annealing_zone.complement() + "5\n"
                f += " "+reverse_annealing_pins.rjust(len(self.forward_primer.primer.seq)+3+len(self.reverse_annealing_zone)) + " tm "+str(round(tmr,1))+"C\n"
                f += str("3"+self.reverse_primer.primer.seq[::-1]).rjust(1+len(self.forward_primer.primer.seq)+3+len(self.reverse_primer.primer.seq)) +"5    "
                f += "ta  "+str(round(ta))+"C\n"

            return f
    
    
    
if __name__=="__main__":

    import textwrap
    
    raw=textwrap.dedent('''
    >fp
    atcgacaactgactgagacact

    >rp
    agtcatgcatgcaggctgggcgta

    >99_CRE_cds_r_BsiWI
    NNNGTCAAGCTTCGTACGATCGCCATCTTCCAG

    >98_CRE_cds_f_Acc65I
    GATCGGTACCATGTCCAATTTACTG

    >CRE
    AAatcgacaactgactgagacactAAatcgccatcttccagcaggcgcaccattgcccctttggtgtacggtcagtaaattggacatCCCtacgcccagcctgcatgcatgactC

    ''')

    new_sequences = parse_string_into_formatted_records(raw)
    
    template = new_sequences.pop().record
    
    primer_sequences  = [sequence.record for sequence in new_sequences]
    
    topology="linear"
    
    homology_limit=13

    aobj = anneal(primer_sequences, template, topology, homology_limit)

    #print aobj.fwd_primers[1]

    #print aobj.rev_primers[1]
 
    aaa = aobj.define_amplicons()
    
    print aaa
    
    for a in aobj.amplicons:
        print  a.product_size
        




'''
New command line interface to PCR.py

Input:

one ore more textfiles with primer sequences in gb or fasta format

if there are not delimiter, last sequence is template, otherwise all seqs after delimiter

this indata is processed into one or more templates and primer sequences stored as lists of 
primer and template objects.

anneal:

test annealing of all primers against one templates.
add annealing primers and positions to the template object

sort primers by annealing position

product:


import argparse

parser = argparse.ArgumentParser(description='Process opts')
parser.add_argument('-c','--circ','--circular', action='store_true')
parser.add_argument('-s','--split',     action='store_true')
parser.add_argument('-f','--files',     nargs='+')
parser.add_argument('-p','--primers',   nargs='+')    
parser.add_argument('-t','--templates', nargs='+')   


##                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')


args = parser.parse_args('-c -s'.split())

print args



# PCR --primers primers.txt --templates templates.txt --output prod.txt -verbose 3

# -o, --output                  use as output file
# -v, --verbose                 verbose
# -a, --anneal-only             report primer annealing only

'''










