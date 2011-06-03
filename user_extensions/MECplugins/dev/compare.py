from Bio import pairwise2

print
#print pairwise2.align.localms.__doc__

#                             localms(sequenceA, sequenceB, match, mismatch, open, extend) 
# alignments = pairwise2.align.globalms("AGGATCCACGTAGCAGAATTC", "TAACGGGATCCAATTGGAATTCCC", 1, -1, -10000000, -1000000)

alignments = pairwise2.align.globalxs("ggatccatcatgcacactattatctatcatatg", "atcatgcacactattatctatcatat",-0.1, 0)


for aln in alignments:

    #print aln

    print pairwise2.format_alignment(aln[0],aln[1],aln[2],aln[3],aln[4])
    
    
    

