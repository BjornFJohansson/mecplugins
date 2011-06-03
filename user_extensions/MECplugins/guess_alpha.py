

#>>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
#>>> fruit = set(basket)               # create a set without duplicates
#>>> fruit
#set(['orange', 'pear', 'apple', 'banana'])
#>>> 'orange' in fruit                 # fast membership testing
#True
#>>> 'crabgrass' in fruit
#False

#>>> # Demonstrate set operations on unique letters from two words
#...
#>>> a = set('abracadabra')
#>>> b = set('alacazam')
#>>> a                                  # unique letters in a
#set(['a', 'r', 'b', 'c', 'd'])
#>>> a - b                              # letters in a but not in b
#set(['r', 'd', 'b'])
#>>> a | b                              # letters in either a or b
#set(['a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'])
#>>> a & b                              # letters in both a and b
#set(['a', 'c'])
#>>> a ^ b                              # letters in a or b but not both
#set(['r', 'd', 'b', 'm', 'z', 'l'])

#ACGT

#ACGU

#ABCDGHKMNRSTVWY

#ABCDGHKMNRSUVWY

#ACDEFGHIKLMNPQRSTVWY

#ABCDEFGHIJKLMNOPQRSTUVWXYZ

#!/usr/bin/env python
# -*- coding: latin-1 -*-

def guess_alphabet(seq, thresh = 0.90, nucleic_letters = ['G', 'A', 'T', 'C', 'U', 'N']):

    if len(seq)>0:
        import string    
        from Bio.Alphabet.IUPAC import extended_protein
        from Bio.Alphabet.IUPAC import protein
        from Bio.Alphabet.IUPAC import ambiguous_dna
        from Bio.Alphabet.IUPAC import unambiguous_dna
        from Bio.Alphabet.IUPAC import extended_dna
        from Bio.Alphabet.IUPAC import ambiguous_rna
        from Bio.Alphabet.IUPAC import unambiguous_rna
        
        seq=seq.upper()
        
        for c in seq:
            if c not in string.ascii_letters:
                return "non coding (unicode)letters"    
        
        xp = set(extended_protein.letters)
        pr = set(protein.letters)
        
        ad = set(ambiguous_dna.letters)
        ud = set(unambiguous_dna.letters) 
        ed = set(extended_dna.letters)
        
        ar = set(ambiguous_rna.letters)
        ur = set(unambiguous_rna.letters) 
        
        alphabet = set(seq)
        
        all = xp|pr|ad|ud|ed|ar|ur
        
        if alphabet - all:
            return "non coding letters"
        
        nucleic_count = 0      
        
        for letter in nucleic_letters:
            nucleic_count += seq.count(letter)      
                
        if float(nucleic_count) / float(len(seq)) >= thresh:
        
            if 'T' in alphabet and 'U' in alphabet:
                return "mixed DNA/RNA"
            
            if   not alphabet-ud:
                return unambiguous_dna
                
            elif not alphabet-ad :
                return ambiguous_dna
                
            elif not alphabet-ed:
                return extended_dna
                
            elif not alphabet-ur:
                return unambiguous_rna
                
            elif not alphabet-ar:
                return extended_rna
                
            else:
                return "amb nucleic acid/protein"
            
        else:
        
        
            threecode = ['ALA', 'ASX', 'CYS', 'ASP','GLU', 'PHE', 'GLY', 'HIS',
                         'ILE', 'LYS', 'LEU', 'MET','ASN', 'PRO', 'GLN', 'ARG',
                         'SER', 'THR', 'VAL', 'TRP','TYR', 'GLX', 'XAA', 'TER',
                         'SEL', 'PYL', 'XLE']
       
            tc=set(threecode)                     
           
            three_letter_alphabet = set( [ seq[i:i+3] for i in range(0,len(seq),3)] )
            
            if not three_letter_alphabet - tc:
                return "three letter code"
            if not alphabet - pr:
                return protein
            if not alphabet - xp:
                return extended_protein
    return "not defined"


if __name__=="__main__":

    from Bio.Alphabet.IUPAC import extended_protein
    from Bio.Alphabet.IUPAC import protein
    from Bio.Alphabet.IUPAC import ambiguous_dna
    from Bio.Alphabet.IUPAC import unambiguous_dna
    from Bio.Alphabet.IUPAC import extended_dna
    from Bio.Alphabet.IUPAC import ambiguous_rna
    from Bio.Alphabet.IUPAC import unambiguous_rna
    print
    print guess_alphabet("None")
    print guess_alphabet("GATCGATCGATCGATCW")
    print guess_alphabet("GAUC")
    print guess_alphabet("MKT")
    print guess_alphabet("MKTjzX")
    print guess_alphabet("augaugaug")
    print guess_alphabet("MetAlaIleValMetGlyArgTrpLysGlyAlaArgTer")
    print guess_alphabet("metmethej")
    

