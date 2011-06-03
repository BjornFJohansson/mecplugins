import                              string
from os                             import linesep as ls
from math                           import log10,log
from Bio                            import SeqIO
from Bio.Seq                        import Seq, reverse_complement
from Bio.Alphabet.IUPAC             import unambiguous_dna
from Bio.SeqRecord                  import SeqRecord
from cStringIO                      import StringIO
from parse_string                   import parse_string_into_formatted_records
from Bio.SeqUtils                   import GC
from Bio.SeqUtils.MeltingTemp       import Tm_staluc

def define_right_overlap(first_sequence,second_sequence):

    length = len(first_sequence)

    if length>len(second_sequence):
        length=len(second_sequence)

    first_sequence  =  str(  first_sequence[ -( length) : ]).upper()
    second_sequence =  str( second_sequence[ -( length) : ]).upper()

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

    assert type(direction)              ==str
    assert type(limit)                  ==int

    positions   = []
    position    = 0
    start       = 0

    three_end_part_of_first_sequence = str(first_sequence[-limit:]).upper()
    second_sequence=Seq(str(second_sequence).upper())

    if direction =="forward":

        while position!=-1:

            position = second_sequence.find(three_end_part_of_first_sequence, start)

            if position!=-1:
                start = position + limit
                positions.append(start)

    if direction =="reverse":

        three_end_part_of_first_sequence = str(first_sequence[-limit:].reverse_complement()).upper()

        while position!=-1:

            position = second_sequence.find(three_end_part_of_first_sequence, start)

            if position!=-1:
                positions.insert(0,position)
                start = position + limit

    return positions

class anneal:

    def __init__(self, primers, template, topology="linear", homology_limit=13, flankuplength=200, flankdnlength=200, max_product_size=15000):

        assert type(primers)                            == list
        assert type(template)                           == SeqRecord

        self.template                                   =template
        if topology=="circular":
            self.circular_template=True
        else:
            self.circular_template=False
        self.homology_limit                             =homology_limit

        class forward_primer:
            def __init__(self,primer, annealing_position):
                self.primer = primer
                self.annealing_position=annealing_position

        class reverse_primer:
            def __init__(self,primer, annealing_position):
                self.primer = primer
                self.annealing_position=annealing_position

        self.fwd_primers = []
        self.rev_primers = []
        self.amplicons   = []
        assert(template.seq) # empty template record
        for primer in primers:
            assert(primer.seq) # empty sequence records in primers

        # primer = primers[0]
        # if annealing_positions(primer.seq, template.seq,"reverse",homology_limit):
        #    template.seq=template.seq.reverse_complement()

        for primer in primers:
            annealing_on_watson_strand = annealing_positions(primer.seq, template.seq,"forward",homology_limit)
            for pos in annealing_on_watson_strand:
                self.fwd_primers.append(forward_primer(primer,pos))

        for primer in primers:
            annealing_on_crick_strand = annealing_positions(primer.seq, template.seq,"reverse",homology_limit)
            for pos in annealing_on_crick_strand:
                self.rev_primers.append(reverse_primer(primer,pos))

        class amplicon:

            def __init__(self,forward_primer,forward_annealing_zone,reverse_primer, reverse_annealing_zone, product, flankup, flankdn, max_product_size):
                self.forward_primer             = forward_primer
                self.forward_annealing_zone     = forward_annealing_zone
                self.reverse_primer             = reverse_primer
                self.reverse_annealing_zone     = reverse_annealing_zone
                self.product                    = product
                self.flankup                    = flankup
                self.flankdn                    = flankdn
                self.max_product_size           = max_product_size

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

        for fp in self.fwd_primers:
            for rp  in self.rev_primers:
                middle_part=""
                if (0 < rp.annealing_position - fp.annealing_position < max_product_size) and not self.circular_template:
                    middle_part = self.template.seq[fp.annealing_position:rp.annealing_position]
                elif (0 < fp.annealing_position - rp.annealing_position < max_product_size) and self.circular_template:
                    middle_part = self.template.seq[fp.annealing_position:]+self.template.seq[:rp.annealing_position]
                else:
                    continue
                prod_seq = fp.primer.seq + middle_part + rp.primer.seq.reverse_complement()
                prod_name = 'PCR product (%s bp) primers %s and %s' % (len(prod_seq), fp.primer.name, rp.primer.name)
                prod_id = fp.primer.name + "-" + rp.primer.name + "_" + str(len(prod_seq))
                prod_description = "("+prod_name + ")"
                product = SeqRecord(prod_seq,prod_id,prod_name,prod_description)
                if fp.annealing_position-len(fp.primer)<= 0:
                    covered_template = self.template.seq[0:fp.annealing_position]
                else:
                    covered_template = self.template.seq[fp.annealing_position-len(fp.primer):fp.annealing_position]
                fz = covered_template[-define_right_overlap(fp.primer.seq,covered_template):]
                covered_template = self.template.seq[rp.annealing_position:rp.annealing_position+len(rp.primer)]
                rz = covered_template[:define_right_overlap(rp.primer.seq,covered_template.reverse_complement())]

                flankup=self.template.seq[fp.annealing_position-flankuplength-len(fz):fp.annealing_position-len(fz)]
                flankdn=self.template.seq[rp.annealing_position+len(rz):rp.annealing_position+flankdnlength+len(rz)]

                self.amplicons.append(amplicon(fp,fz,rp,rz,product,flankup,flankdn,max_product_size))

    def __str__(self):

        string = "Template " + self.template.name + ":" + ls

        if self.fwd_primers:

            for primer in self.fwd_primers:
                string += "Primer "+primer.primer.name
                string += " anneals at position "
                string += str(primer.annealing_position)
                string += ls
        else:
            string += "No forward primers anneal...\n"

        if self.rev_primers:

            for primer in self.rev_primers:
                string += "Primer "+primer.primer.name
                string += " anneals reverse at position "
                string += str(primer.annealing_position)
                string += ls

        else:

             string += "No reverse primers anneal...\n"
             #string = ''

        return string

    def products(self):
        string=""
        product_list = []

        for ampl in self.amplicons:
            product_list.append(ampl.product)

        if product_list:
            #print "sant"
            pass

        if not product_list:
            #print "falskT"
            return False

        handle=StringIO()

        SeqIO.write(product_list, handle, "fasta")

        string=handle.getvalue()

        handle.close()

        #print string

        return string




if __name__=="__main__":

    raw='''
>99_CRE_cds_r_BsiWI
NNNGTCAAGCTTCGTACGATCGCCATCTTCCAG
>98_CRE_cds_f_Acc65I
GATCGGTACCATGTCCAATTTACTG
>CRE
AAAAatcgccatcttccagcaggcgcaccattgcccctttggtgtacggtcagtaaattggacatCCCC
'''

    new_sequences = parse_string_into_formatted_records(raw)
    template = new_sequences.pop().record
    primer_sequences  = [sequence.record for sequence in new_sequences]
    topology="linear"
    homology_limit=13
    flankuplength=100
    flankdnlength=100
    max_product_size=5000

    anneal_primers = anneal(primer_sequences, template, topology, homology_limit, flankuplength, flankdnlength, max_product_size)

    print anneal_primers

    if anneal_primers.products():
        for hej in anneal_primers.amplicons:
            print hej.detailed_figure()
            print hej.flankup
            print hej.flankdn
