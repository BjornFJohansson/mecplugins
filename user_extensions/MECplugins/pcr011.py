import                              string
import                              re
import                              sys
import                              datetime
from Bio.SeqUtils.CheckSum          import seguid
from math                           import log10,log
from Bio                            import SeqIO
from Bio.Seq                        import Seq
from Bio.Seq                        import reverse_complement
from Bio.Alphabet.IUPAC             import unambiguous_dna,ambiguous_dna
from Bio.SeqRecord                  import SeqRecord
#from cStringIO                      import StringIO
from parse_string2                  import parse_string_into_formatted_records
from Bio.SeqUtils                   import GC
from Bio.SeqUtils.MeltingTemp       import Tm_staluc
from Bio.SeqFeature                 import SeqFeature, FeatureLocation, ExactPosition

def define_right_overlap(first_sequence,second_sequence):

    length = min(len(first_sequence),len(second_sequence))

    first_sequence  =  str(  first_sequence[ -( length) : ]).lower()
    second_sequence =  str( second_sequence[ -( length) : ]).lower()

    rghtpos=length
    leftpos=0

    while not (rghtpos-leftpos==1 or int(rghtpos)==0):

        if first_sequence[leftpos:rghtpos]==second_sequence[leftpos:rghtpos]:
            rghtpos=leftpos
            leftpos=(rghtpos)/2
        else:
            leftpos=(leftpos+rghtpos)/2

    if first_sequence[leftpos:rghtpos]==second_sequence[leftpos:rghtpos]:
        return length-leftpos
    else:
        return length-rghtpos

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

        self.features.append( SeqFeature(FeatureLocation(0,len(seq)),
                              strand=1,
                              type ="primer",
                              qualifiers = {"label":seq.name,
                                            "note" :["complete primer sequence","SEGUID:"+seguid(seq.seq)]}))

        self.annotations["date"] = datetime.datetime.now().strftime("%d-%b-%Y").upper()
        
        '''
        self.features.append(  SeqFeature(FeatureLocation(0,len(seq)),
                                        strand=1,
                                        type ="misc_feature",
                                        qualifiers = {"label":"SEGUID",
                                        "note" :seguid(seq.seq)}))'''

class Amplicon:
    def __init__(self,forward_primer, reverse_primer, template, flankup=0,flankdn=0):
        
        self.forward_primer = forward_primer
        self.reverse_primer = reverse_primer
        self.product_size   = len(forward_primer)+len(reverse_primer)+reverse_primer.annealing_position-forward_primer.annealing_position
        
        self.middle_sequence = template[forward_primer.annealing_position:reverse_primer.annealing_position]
        self.product_sequence = forward_primer + self.middle_sequence + reverse_primer.reverse_complement()

        #self.product_sequence.id = "12345678"
        self.product_sequence.annotations["date"] = datetime.datetime.now().strftime("%d-%b-%Y").upper()

        flankup  = template[:forward_primer.annealing_position]
        flankdn  = template[reverse_primer.annealing_position:]
        
        self.forward_covered_template = flankup.seq[-len(forward_primer):]
        self.reverse_covered_template = flankdn.seq[:len(reverse_primer)]
        
        self.flankup = flankup[-flankup:]
        self.flankdn = flankdn[-flankdn:]
        
        self.template_sequence = self.forward_covered_template + self.middle_sequence + self.reverse_covered_template
        self.template_sequence.annotations["date"] = datetime.datetime.now().strftime("%d-%b-%Y").upper()

    def __str__(self):
        repr = string.Template("PCR product $size by primers $fp and $rp").safe_substitute(size=str(self.product_size),fp=self.forward_primer.name,rp=self.reverse_primer.name) 
        return repr
        
    def detailed_figure(self, alternative_image=2):
        forward_annealing           = define_right_overlap(self.forward_primer.seq,self.forward_covered_template)
        forward_annealing_pins      = "|"*forward_annealing
        self.forward_annealing_zone = self.forward_covered_template[-forward_annealing:]
        
        reverse_annealing           = define_right_overlap(self.reverse_primer.seq,self.reverse_covered_template.reverse_complement())
        reverse_annealing_pins      = "|"*reverse_annealing
        self.reverse_annealing_zone = self.reverse_covered_template[:reverse_annealing]
        
        self.forward_primer.features.append(SeqFeature(FeatureLocation(len(self.forward_primer)-forward_annealing,len(self.forward_primer)),
                                                        strand=1,
                                                        type ="primer_bind",
                                                        qualifiers = {"label":self.forward_primer.name+" annealing",
                                                                      "note" :"annealing zone"}))
        self.reverse_primer.features.append(SeqFeature(FeatureLocation(len(self.reverse_primer)-reverse_annealing,len(self.reverse_primer)),
                                                        strand=1,
                                                        type ="primer_bind",
                                                        qualifiers = {"label":self.reverse_primer.name+" annealing",
                                                                      "note" :"annealing zone"}))
        
        self.product_sequence = self.forward_primer + self.product_sequence[len(self.forward_primer):len(self.product_sequence)-len(self.reverse_primer)] + self.reverse_primer.reverse_complement()
        self.product_sequence.id = "PCR product"
        self.product_sequence.description = str(self.product_size)+"bp amplified with primers "+ self.forward_primer.name+" and "+self.reverse_primer.name
         #= "PCR product ("+str(self.product_size)+"bp)"+ self.forward_primer.name+" "+self.reverse_primer.name
        self.product_sequence.annotations["date"] = datetime.datetime.now().strftime("%d-%b-%Y").upper()
        
        '''
        self.product_sequence.features.append(  SeqFeature(FeatureLocation(0,len(self.product_sequence)),
                                                strand=1,
                                                type ="misc_feature",
                                                qualifiers = {"note" :"SEGUID:"+seguid(self.product_sequence.seq)}))
        '''
        
        self.product_sequence.annotations["comment"] = "SEGUID:"+seguid(self.product_sequence.seq)
        
        tmf = Tm_staluc(str(self.forward_annealing_zone))
        tmr = Tm_staluc(str(self.reverse_annealing_zone))

        K = 0.050 # 50 mM
        L = len(self.product_sequence)
        GC_prod=GC(str(self.product_sequence))
        tmp = 81.5 + 0.41*GC_prod + 16.6*log10(K) - 675/L
        tml = min([tmf,tmr])
        ta = 0.3*tml+0.7*tmp-14.9

        f = ""

        if alternative_image==1:
            f += str("5"+self.forward_annealing_zone).rjust(1+len(self.forward_primer.seq.tostring())) + "..."
            f += self.reverse_annealing_zone + "3\n"
            f += " "+reverse_annealing_pins.rjust(len(self.forward_primer.seq.tostring())+3+len(self.reverse_annealing_zone)) + "\n"
            f += str("3"+self.reverse_primer.seq.tostring()[::-1]).rjust(1+len(self.forward_primer.seq.tostring())+3+len(self.reverse_primer.seq.tostring())) +"5\n"
            f +=  "5"+self.forward_primer.seq.tostring() + "3\n"
            f += " "+forward_annealing_pins.rjust(len(self.forward_primer.seq.tostring())) + "\n"
            f += str("3"+self.forward_annealing_zone.complement()).rjust(1+len(self.forward_primer.seq.tostring())) + "..."
            f += self.reverse_annealing_zone.complement() + "5\n"

        if alternative_image==2:
            f += "5"+self.forward_primer.seq.tostring() + "3\n"
            f += " "+forward_annealing_pins.rjust(len(self.forward_primer.seq.tostring())) + " tm "+str(round(tmf,1))+"C\n"
            f += str("5"+self.forward_annealing_zone).rjust(1+len(self.forward_primer.seq.tostring())) + "..."
            f += self.reverse_annealing_zone + "3\n"
            f += str("3"+self.forward_annealing_zone.complement()).rjust(1+len(self.forward_primer.seq.tostring())) + "..."
            f += self.reverse_annealing_zone.complement() + "5\n"
            f += " "+reverse_annealing_pins.rjust(len(self.forward_primer.seq.tostring())+3+len(self.reverse_annealing_zone)) + " tm "+str(round(tmr,1))+"C\n"
            f += str("3"+self.reverse_primer.seq.tostring()[::-1]).rjust(1+len(self.forward_primer.seq.tostring())+3+len(self.reverse_primer.seq.tostring())) +"5\n    "
            f += "ta  "+str(round(ta))+"C\n"

        #self.product_sequence.annotations["comment"] = ["." + a for a in str(f).splitlines()]
        return f

class Anneal:
    def __init__(self, primers, template, topology="linear", homology_limit=13):

        assert type(primers) == list
        assert topology=="linear" or topology=="circular"
        self.topology = topology
        
        if isinstance(template,SeqRecord):
            template.seq.alphabet = ambiguous_dna            
        elif isinstance(template,str):
            template = SeqRecord(Seq(template),"template","template")
        elif isinstance(template,Seq):
            template = SeqRecord(template,"template","template")
        else:
            raise TypeError("the template property needs to be a string, a Seq object or a SeqRecord object")

        assert template.seq
        template.seq.alphabet = ambiguous_dna
        
        self.template_size  = len(template) 
        self.template_name  = template.name

        self.template = template
        self.homology_limit = homology_limit
        #self.max_product_size = max_product_size

        for primer in primers:
            assert(primer.seq) # check if empty sequence records in primers
            
        self.fwd_primers = []
        self.rev_primers = []    
   
        for primer in primers:  # add annealing forward and reverse primers

            annealing_positions_on_watson_strand = annealing_positions(primer.seq, template.seq,"forward",homology_limit)            
            for position in annealing_positions_on_watson_strand:
                self.fwd_primers.append(Primer(primer, position))
                
            annealing_positions_on_crick_strand = annealing_positions(primer.seq, template.seq,"reverse",homology_limit)
            for position in annealing_positions_on_crick_strand:
                self.rev_primers.append(Primer(primer, position))

    def __str__(self):
        string = "Template " + self.template_name + " ("+self.topology+") "+str(self.template_size)+"bp :\n"
        if self.fwd_primers:
            for primer in self.fwd_primers:
                string += "Primer "+primer.name
                string += " anneals at position "
                string += str(primer.annealing_position)
                string += "\n"
        else:
            string += "No forward primers anneal...\n"
        string += ">---<\n"
        if self.rev_primers:
            for primer in self.rev_primers:
                string += "Primer "+primer.name
                string += " anneals reverse at position "
                string += str(primer.annealing_position)
                string += "\n"
        else:
             string += "No reverse primers anneal...\n"
        return string

    def define_amplicons(self,forward_primers=[],reverse_primers=[], max_product_size=20000, flank=0):
        
        self.max_product_size = max_product_size      
          
        if not forward_primers:
            forward_primers=self.fwd_primers        
        if not reverse_primers:
            reverse_primers=self.rev_primers
            
        amplicons,sizes = [],[]
       
        for forward_primer in forward_primers:
            for reverse_primer in reverse_primers:
                
                if 0 <= reverse_primer.annealing_position - forward_primer.annealing_position <= self.max_product_size:
                    
                    amplicons.append(Amplicon(forward_primer, reverse_primer, self.template, flank))
                    
                elif self.topology == "circular" and (0 <= forward_primer.annealing_position - reverse_primer.annealing_position <= self.max_product_size):

                    newtemplate = self.template[forward_primer.annealing_position-len(forward_primer):]+self.template[:forward_primer.annealing_position-len(forward_primer)]
                    
                    new_reverse_position = len(self.template) \
                                            - (forward_primer.annealing_position - reverse_primer.annealing_position)
                    forward_primer.annealing_position = len(forward_primer)
                    reverse_primer.annealing_position = forward_primer.annealing_position+new_reverse_position
                   
                    amplicons.append(Amplicon(forward_primer, reverse_primer, newtemplate, flank))
                

        self.amplicons = sorted(amplicons,key=lambda Amplicon: Amplicon.product_size)
        return self.amplicons    
    
    
if __name__=="__main__":

    import textwrap
    
    raw=textwrap.dedent('''
    >fp
    NNNtggtgtacggtcagtaaattggac

    >rp
    NNNtggcgatTTagtgtctcagtcagttg

    >CRE
    AAatcgacaactgactgagacactAAatcgccatcttccagcaggcgcaccattgcccctttggtgtacggtcagtaaattggacatCCCtacgcccagcctgcatgcatgactC
    ''')

    new_sequences = parse_string_into_formatted_records(raw)
    
    mytemplate = new_sequences.pop().record
    
    my_primer_sequences  = [sequence.record for sequence in new_sequences]
    
    my_topology="circular"
    
    my_homology_limit=13

    aobj = Anneal(my_primer_sequences, mytemplate, my_topology, my_homology_limit)

    print aobj

    print aobj.fwd_primers[0].format("gb")

    print aobj.rev_primers[0].format("gb")

    amplicons = aobj.define_amplicons(flank = 5)

    print amplicons[0]
    
    for amplicon in amplicons:
        print "size ",amplicon.product_size
        print amplicon.detailed_figure()
        print amplicon.product_sequence.format("gb")
        print amplicon.product_sequence.format("fasta")
        print amplicon.template_sequence.format("fasta")