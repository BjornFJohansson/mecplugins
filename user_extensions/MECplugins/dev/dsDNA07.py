#!/usr/bin/python
       
class dsDNA: 
    
    def __init__(self,watson,crick="", shape="linear"):
        self.watson = watson
        if crick:
            self.crick=crick
        else:
            self.crick=watson.reverse_complement()
        self.shape  = shape
    
    def __str__(self):
        return str(self.watson+"\n"+self.crick[::-1])

    def rev_comp(self):
        slask=self.watson
        self.watson=self.crick
        self.crick=slask
        
class dscatalyse():
   
    def __init__(self, dsfrag, enzyme):
        
        watson_sites = enzyme.search(dsfrag.watson)
        
        space = len(dsfrag.watson)-len(dsfrag.watson.lstrip())
        
        if space:
            watson_sites =[site+space for site in watson_sites]
        
        
        
        crick_sites  = enzyme.search(dsfrag.crick)
        
        space = len(dsfrag.crick)-len(dsfrag.crick.lstrip())
        
        if space:
            crick_sites =[site+space for site in watson_sites]
        

        
        
        
        watson_sequences =[]
        crick_sequences  =[]

        f = dsfrag.watson
        
        for site in watson_sites:
        
            watson_sequences.append(f[:site-1] + " "*-enzyme.ovhg)
            f=" "*enzyme.ovhg+f[site-1:]
        
        watson_sequences.append(f)
        
        f = dsfrag.crick
        
        for site in crick_sites:

            crick_sequences.append(f[:site-1] + " "*-enzyme.ovhg)
            f=" "*enzyme.ovhg+f[site-1:]
            
        crick_sequences.append(f)
                

        self.dslist =[]
        
        for sw,sc in zip(watson_sequences,crick_sequences[::-1]):       
            self.dslist.append(dsDNA(sw,sc,"linear"))        
        return
             
        
    def __str__(self):
        string =""
        for seq in self.dslist:
            string = string + str(seq)+"\n"            
        return string
        
#        dsfrags=        
#        for site in self.watsonsites:
#            positionlist=[]
#            for pos in self.watsonsites[site]:
#                positionlist.append(pos + site.ovhg )
#                self.correctedwatsonsites[site]=positionlist      
            
        return

class dsanalyse():

    def __init__(self, dsfrag, rb):
        return
    def __str__(self):
        return #str(self.watsonsites)+str(self.correctedwatsonsites)        


# BamHI -g|g-a-t-c-c-
#       -c-c-t-a-g|g-
# PstI  -c-t-g-c-a|g-
#       -g|a-c-g-t-c-
#>>> from Bio.Restriction import *
#>>> BamHI.ovhg
#-4
#>>> PstI.ovhg
#4
#>>>


if __name__=="__main__":
    import string
    from Bio.Restriction import *
    from Bio.Seq import Seq, reverse_complement
    from Bio.Alphabet.IUPAC import IUPACAmbiguousDNA
    
    
    w = Seq('cctGGATCCata' , IUPACAmbiguousDNA())
    c = Seq('ataGGATCCagg',IUPACAmbiguousDNA())
    ds1 = dsDNA(w,c)
    print
    print ds1
    print dscatalyse(ds1,BamHI)
    print
    w = Seq(' ctCTGCAGata', IUPACAmbiguousDNA())
    c = Seq('ataCTGCAGagg', IUPACAmbiguousDNA())
    ds1 = dsDNA(w,c)
    print ds1
    print dscatalyse(ds1,PstI)

    w = Seq(' ctCCCGGGata', IUPACAmbiguousDNA())
    c = Seq('ataCCCGGGagg', IUPACAmbiguousDNA())
    ds1 = dsDNA(w,c)
    print ds1
    print dscatalyse(ds1,SmaI)
    print

