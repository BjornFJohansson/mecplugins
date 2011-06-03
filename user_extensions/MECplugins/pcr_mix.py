#!/usr/bin/env python
# -*- coding: latin-1 -*-
from SIprefix import SIprefix
import sys

class PCRmixture:

    #from SIprefix import SIprefix
    #import sys

    def __init__(self,selected_text):

        class buffer:
            def __init__(self,name,number,stock_value,stock_prefix,stock_unit,final_value,final_prefix,final_unit):

                self.name           = name
                self.stock_value    = stock_value
                self.stock_prefix   = stock_prefix
                self.stock_unit     = stock_unit

                self.final_value    = final_value
                self.final_prefix   = final_prefix
                self.final_unit     = final_unit

        class primer:

            def __init__(self,data):

                self.name           = data[2]
                self.number         = data[1]
                self.stock_value    = data[4]
                self.stock_unit     = data[5]
                self.final_value    = data[8]
                self.final_unit     = data[9]

                assert self.stock_unit[1] == self.final_unit[1]

                self.volume_percentage = 100*float(self.final_value) * SIprefix(self.final_unit[0]) / (float(self.stock_value) * SIprefix(self.stock_unit[0]))

                self.desc = " ".join(data)

        class reaction:

            def __init__(self,number,total_volume,volume_mastermix, volume_template, description):

                self.number             = number
                self.total_volume       = total_volume
                self.volume_mastermix   = volume_mastermix
                self.volume_template    = volume_template
                self.description        = description

        from pyparsing import Word, Literal, alphas, printables, LineStart, White, SkipTo, Combine, nums, And, \
        ZeroOrMore, Optional, LineEnd, delimitedList, alphanums, srange

        dot = Literal(".")

        Real = Combine(Optional("-") + Word(nums) + Optional(dot) + Optional(Word(nums)))

        percentage = Real.setResultsName("percentage")+ Literal("%")

        stock = Literal("stock")+Real.setResultsName("stock_value")+Word(alphas).setResultsName("stock_prefix_unit")+Literal(",")+Literal("final")+Real.setResultsName("final_value")+Word(alphas).setResultsName("final_prefix_unit")

        range_pat = delimitedList(Word(alphanums)+Optional(Literal("-")))

        template_pat = Literal("template (v/v)") + percentage
        result = template_pat.scanString(selected_text)
        for data,dataStart,dataEnd in result:
            self.template_desc        = " ".join(data)
            self.template_percentage  = float(data[1])

        # reactions
        self.expl_reactions=[]
        reaction_pat = (LineStart()+Literal("r")+Real+Optional(Real)+Optional(Real)+SkipTo(LineEnd()))
        result = reaction_pat.scanString(selected_text)
        no = 1
        for data,dataStart,dataEnd in result:
            self.expl_reactions.append(reaction(no,0.0,0.0,0.0,data[-1]))
            no+=1

        # PCR volumes
        volume_pat       = Real.setResultsName("volume",listAllMatches=True)
        tubes_pat        = Real.setResultsName("tubes",listAllMatches=True)
        volumextubes_pat = volume_pat + Literal("x") + tubes_pat + Optional(Literal("+"))
        PCR_volumes_pat  = Literal("PCR volume(s) (volume x no of tubes)")+ ZeroOrMore(volumextubes_pat)

        result = PCR_volumes_pat.scanString(selected_text)

        self.impl_reactions =[]

        for data,dataStart,dataEnd in result:

            self.pcr_volumes_desc = " ".join(data)

            no = 1
            for vol,tbs in zip(data.volume, data.tubes):

                for n in range(int(tbs)):
                    vol_mm = float(vol)*(100-self.template_percentage)/100
                    vol_temp =float(vol)-vol_mm
                    self.impl_reactions.append(reaction(no,vol,vol_mm,vol_temp,"n/a"))
                    no+=1

        self.reactions =[]

        for i,e in zip(self.impl_reactions,self.expl_reactions):
            rxn = reaction(i.number,i.total_volume,i.volume_mastermix,i.volume_template,e.description)
            self.reactions.append(rxn)

        if len(self.expl_reactions)>len(self.reactions):
            self.reactions = self.reactions+self.expl_reactions[len(self.reactions):]

        if len(self.impl_reactions)>len(self.reactions):
            self.reactions = self.reactions+self.impl_reactions[len(self.reactions):]

        # primers
        primer_pattern= Literal("primer")+Word(nums)+Word(printables)+stock
        result = primer_pattern.scanString(selected_text)
        self.primers=[]
        for data,dataStart,dataEnd in result:
            self.primers.append(primer(data))

        # buffer
        buffer= Literal("buffer")+SkipTo(" stock")+stock
        result = buffer.scanString(selected_text)
        for data,dataStart,dataEnd in result:
            self.buffer_desc = " ".join(data)
            self.buffer_name,self.buffer_stock_value,self.buffer_stock_unit,self.buffer_final_value,self.buffer_final_unit= data[1],data[3],data[4],data[7],data[8]

        # magnesium
        mg_pat= Combine(Literal("Mg")+(Literal("Cl2")|Literal("SO4")))+SkipTo(Literal(" stock")) + stock
        result = mg_pat.scanString(selected_text)
        for data,dataStart,dataEnd in result:
            self.mg_desc = " ".join(data)
            self.mg_compund,self.mg_info,self.mg_stock_value,self.mg_stock_unit, self.mg_final_value,self.mg_final_unit = data[0],data[1],data[3],data[4],data[7],data[8]

        #dNTPs
        dNTP= Literal("dNTP")+stock
        result = dNTP.scanString(selected_text)
        for data,dataStart,dataEnd in result:
            self.dNTP_desc = " ".join(data)
            self.dNTP_stock_value,self.dNTP_stock_unit,self.dNTP_final_value,self.dNTP_final_unit= data[2],data[3],data[6],data[7],

        # DNA pol
        pol = Literal("DNA pol (v/v)")+percentage
        result = pol.scanString(selected_text)
        for data,dataStart,dataEnd in result:
            self.pol_desc = " ".join(data)
            self.pol_percentage = float(data[1])

        # extra volume
        extravol = Literal("extra volume")+percentage
        result = extravol.scanString(selected_text)
        self.extra_volume = 0
        for data,dataStart,dataEnd in result:
            self.extravol_desc = " ".join(data)
            self.extra_volume = float(data[1])



        # Calculations

        tv=0
        no=len(self.reactions)

        for rxn in self.reactions:
            tv+=float(rxn.total_volume)

        self.total_volume=tv*(100+self.extra_volume)/100

        assert self.buffer_stock_unit   == "x"
        assert self.buffer_stock_unit   == self.buffer_final_unit
        self.buffer_volume 		        =  self.total_volume*float(self.buffer_final_value)/float(self.buffer_stock_value)

        self.mg_volume     		= self.total_volume*float(self.mg_final_value)*SIprefix(self.mg_final_unit[0])/(float(self.mg_stock_value)*SIprefix(self.mg_stock_unit[0]))
        self.dNTP_volume   		= self.total_volume*float(self.dNTP_final_value)*SIprefix(self.dNTP_final_unit[0])/(float(self.dNTP_stock_value)*SIprefix(self.dNTP_stock_unit[0]))

        self.DNA_pol_volume 	= self.total_volume*self.pol_percentage/100

        primvols=0

        for P in self.primers:
            primvols+= self.total_volume*P.volume_percentage/100

        self.template_volume = self.template_percentage*self.total_volume/100
        mastermix_volume = self.buffer_volume + self.mg_volume + self.dNTP_volume + primvols + self.DNA_pol_volume
        self.water_volume = self.total_volume - mastermix_volume - self.template_volume
        self.mastermix_volume = mastermix_volume + self.water_volume



        result_text = "\n".join([self.pcr_volumes_desc,self.template_desc,"\n".join([p.desc for p in self.primers]),self.buffer_desc,self.mg_desc,self.dNTP_desc,self.pol_desc, self.extravol_desc])

        result_text +="\n++++reactions: \n"
        result_text +="#    mm     temp  Description\n"

        for rxn in self.reactions:
            result_text +="r%i\t%5.1f\t%3.1f   %s\n" %(rxn.number,round(rxn.volume_mastermix,1),round(rxn.volume_template,1),rxn.description)

        result_text +="++++mastermix (mm):\n"

        result_text +="%4.1f\twater\n"            % (round(self.water_volume,1))
        result_text +="%4.1f\tbuffer %s\n"        % (round(self.buffer_volume,1),self.buffer_name)
        result_text +="%4.1f\t%s %s %s\n"         % (round(self.mg_volume,1),self.mg_compund,self.mg_stock_value,self.mg_stock_unit)
        result_text +="%4.1f\tdNTP %s %s\n"       % (round(self.dNTP_volume,1),self.dNTP_stock_value,self.dNTP_stock_unit)

        for P in self.primers:
            result_text += "%4.1f\t%s %s %s\n"    % (round(self.total_volume*P.volume_percentage/100,1),P.name, P.stock_value,P.stock_unit)
        result_text +="%4.1f\tDNA polymerase\n"   % (round(self.DNA_pol_volume,1))
        result_text +="%4.1f\t(template)\n"   % (round(self.template_volume,1))
        result_text +="++++mastermix (mm) using PCRMastermix-2X:\n"

        result_text +="%4.1f\tPCRMastermix-2X\n" % (round(self.total_volume/2,1))
        for P in self.primers:
            result_text += "%4.1f\t%s %s %s\n"     % (round(self.total_volume*P.volume_percentage/100,1),P.name, P.stock_value,P.stock_unit)
        result_text +="%4.1f\twater\n" % (round(self.mastermix_volume-(self.total_volume/2)-primvols,1))
        result_text +="%4.1f\t(template)\n"   % (round(self.template_volume,1))

        self.result_text = result_text
        return


if __name__=="__main__":

    selected_text='''PCR volume(s) (volume x no of tubes) 50 x 1 + 20 x 3
template (v/v) 2.5 %
primer 1 fwdprimername stock 10 uM , final 1 uM
primer 2 revprimername stock 10 uM , final 1 uM
buffer 10xTaq Buffer w (NH4)2SO4 stock 10.0 x , final 1.0 x
MgSO4 homemade 2009-03-23 stock 50.0 mM , final 1.0 mM
dNTP stock 1.0 mM , final 100.0 uM
DNA pol (v/v) 2.0 %
extra volume 10.0 %
#	mm	temp	Description
r1	48.75	1.25    cassette plasmid 1,
r2	19.5	0.5	    negative control
r3 gnurgla DNA  1,2,3-5,7
'''

    selected_text='''
bajs
svamp
fluga
'''
    a = PCRmixture(selected_text)
    print a.result_text



