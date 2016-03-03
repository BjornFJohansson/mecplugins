# mecplugins

The mecplugins are a collection of python source code files that provide extended functionality for the personal wiki [wikidpad](http://wikidpad.sourceforge.net/).

These plugins provide wikidPad with functions for molecular biology experiment design and electronic notebook keeping.

Mecplugins include:

## DNA sequence tools

Sequence utilities is a part of the mecplugins that can be installed alone from the installer. This is a collection of tools and utilities for working with DNA sequences in wikidPad.

Simple sequence manipulation is possible, such as finding complement, reverse complement and translation of nucleic acid sequences.

[![reverse complement, complement and translation](http://img.youtube.com/vi/6pNSM2sU7_8/0.jpg)](http://www.youtube.com/watch?v=6pNSM2sU7_8)

The format of sequence files stored in WikidPad can be changed between FASTA and genbank.
[![toggle sequence formats](http://img.youtube.com/vi/TrhoIwiYYDU/0.jpg)](http://www.youtube.com/watch?v=TrhoIwiYYDU)


Restriction enzyme analysis of single or multiple sequences is also possible. 
Presented results depends on whether one or more sequences are selected.

If one sequence is selected, the following enzyme collections will be presented:

* enzymes that cut once
* enzymes that do not cut the sequence (absent)
* enzymes that cut twice or more

If two or more sequences are selected, the following enzyme collections will be presented:

* enzymes that cut once in each sequence
* enzymes that do not cut the any of the sequences
*enzymes that cut once in the last sequence and are absent in the preceding sequence(s)
* enzymes that cut twice in the last sequence and are absent in the preceding sequence(s)

The last two functions are useful for quickly finding suitable enzymes to clone one or more DNA fragments in a vector if the vector sequence is the last sequence.

[![restriction analysis](http://img.youtube.com/vi/y5vkL9WgglY/0.jpg)](http://www.youtube.com/watch?v=y5vkL9WgglY)





A PCR primer melting temparature (Tm) function is available for nucleotides in selection. Two formulas are provided, the Marmur formula (A+T)*2+(G+C)*4 (Marmur, J., and Doty, P. 1962 J Mol Biol 5:109-118) and the nearest neighbour algorithm using the SantaLucia thermodynamic values (SantaLucia J. 1998 PNAS 95:1460-1465).

[![tm](http://img.youtube.com/vi/ujMb2A3PJpE/0.jpg)](http://www.youtube.com/watch?v=ujMb2A3PJpE)


A PCR simulation function is provided. This function provides the sequence of the PCR product given the sequences of primers and template and a figure showing the annealing primers. This function allow primers with 5' overhangs that does not basepair with the template, something that is often used to incorporate restriction enzyme sites at the ends of PCR products.

[![PCR](http://img.youtube.com/vi/8zqKCJgP4so/0.jpg)](http://www.youtube.com/watch?v=8zqKCJgP4so)








A PCR primer melting temparature (Tm) function is available for nucleotides in selection. 

Two formulas are provided, the Marmur formula (A+T)*2+(G+C)*4 (Marmur, J., and Doty, P. 1962 J Mol Biol 5:109-118) and the nearest neighbour algorithm using the SantaLucia thermodynamic values (SantaLucia J. 1998 PNAS 95:1460-1465).
