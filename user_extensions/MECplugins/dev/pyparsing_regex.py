

from pyparsing import Regex
from pyparsing import Word, Literal, printables, LineStart, LineEnd, SkipTo, Combine, nums


raw_string = '''
ORDER CONFIRMATION
==================




Eurofins MWG Operon
Anzinger Str. 7
85560 Ebersberg
Germany



-------------------------------------
Order ID : 2432375
Your Order ID: Wednesday, May 11 20
Customer ID  : 00052826
Orderer ID   : 00052827
-------------------------------------

Fisher Scientific, Lda.

Edificio EURO
Rua Pedro Alvares Cabral 24,3.°D
PT-  Infantado


CUSTOMER ADDRESS:
-----------------
University of Minho

Department of Biology
Campus de Gualtar
PT-4710-057 Braga

SHIPPING ADDRESS:
-----------------
Dr. Björn Johansson
University of Minho

Department of Biology
Campus de Gualtar
PT-4710-057 Braga

Phone: +351-253604310  Fax: +351-253678980
Email: bjorn_johansson@bio.uminho.pt
VAT (customer): PT506429210
VAT (orderer): PT502571357

Order Date:      11.05.11 12:48
Order Submitted: 11.05.11 12:48
Shipment:  - EXPRESS SHIPPING -
Payment Method:  purchase order

Order Comment:
Bill Comment: Factura Nº 731
Fisher Scientific, Lda.
Edificio EURO
Rua Pedro Alvares Cabral 24,3.°D
PT-  Infantado



oligo name.......... oligo details
......................................... price
=====================================================================================
pCAPsZraI5Pf         Modified Oligos à la Carte
  36.26 EUR
                    5'PHO-GTCAGCGGCCGCATTGCACAGACT-3'  HPLC
                    0.01

pCAPsZraI5Pr         Modified Oligos à la Carte
  40.22 EUR
                    5'PHO-GTCGAGGAACGCCAGGTTGCCCACTTTC-3'  HPLC
                    0.01

pCAPsEcoRV5Pf        Modified Oligos à la Carte
  42.20 EUR
                    5'PHO-ATCCTGATGCGTTTGTCTGCACAGATGGCG-3'  HPLC
                    0.01

pCAPsEcoRV5Pr        Modified Oligos à la Carte
  53.09 EUR
                    5'PHO-ATCCGGATTTACCTGAATCAATTGGCGAAATTTTTTGTACG-3
                    '  HPLC 0.01

MX4blf               Unmodified Oligos à la Carte
  16.66 EUR
                    5'-CCAAtcacatcacatccgaacataaacaaccatg-3'  HPSF
                    0.01

MX4bl-I-SceIr        Unmodified Oligos à la Carte
  30.68 EUR
                    5'-TCCGATTACCCTGTTATCCCTAcaagaatctttttattgtcagtac
                    tgatta-3'  HPSF 0.05

MX4bl-PI-SceIr       Unmodified Oligos à la Carte
  37.76 EUR
                    5'-TCCGATCTATGTCGGGTGCGGAGAAAGAGGTAATcaagaatctttt
                    tattgtcagtactgatta-3'  HPSF 0.05

YlACC1f_SgsI         Unmodified Oligos à la Carte
  13.23 EUR
                    5'-CCAAatgcgactgcaattgaggacact-3'  HPSF
                    0.01

YlACC1r_CpoI         Unmodified Oligos à la Carte
  12.74 EUR
                    5'-TCCGtcacaaccccttgagcagctca-3'  HPSF
                    0.01

A-pdc5               Unmodified Oligos à la Carte
  12.25 EUR
                    5'-AAAAATTGATTCTCATCGTAAATGC-3'  HPSF
                    0.01

D-pdc5               Unmodified Oligos à la Carte
  12.25 EUR
                    5'-CTAAAGGTACAAAACCGAATACGAA-3'  HPSF
                    0.01

TDHpromFWD           Unmodified Oligos à la Carte
  14.21 EUR
                    5'-ACAAGGCAATTGACCCACGCATGTATCTA-3'  HPSF
                    0.01

                    Printed Synth. Report
   0.00 EUR*
=====================================================================================

  321.55 EUR*

All prices are net prices and do not include delivery costs and taxes.
Country specific shipping charges can be found on our international
shipping price list in the "Service Corner" menu.
The stated prices are subject to change. Prices marked with * do not
consider customer specific conditions and may vary for export
countries.
Orders can be cancelled by yourself within 30 minutes after order
submission in the tracking section of "my orders".

'''

name        =  Word(printables).setResultsName("name")
seq_start   =  Literal("-").suppress()
seq_stop    =  Literal("-").suppress()
sequence    =  Regex("[atcgyrnATCGYRN]+").setResultsName("seq") 
mwg_primer  =  sequence #LineStart() + name + 

result = mwg_primer.scanString(raw_string)

seqlist = [data for data,dataStart,dataEnd in result]

print seqlist