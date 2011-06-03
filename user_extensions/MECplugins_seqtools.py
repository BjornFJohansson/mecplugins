##########################################
#   _____         _______          _
#  / ____|       |__   __|        | |
# | (___   ___  __ _| | ___   ___ | |___
#  \___ \ / _ \/ _` | |/ _ \ / _ \| / __|
#  ____) |  __/ (_| | | (_) | (_) | \__ \
# |_____/ \___|\__, |_|\___/ \___/|_|___/
#                 | |
#                 |_|
##########################################

WIKIDPAD_PLUGIN = (("MenuFunctions",1), ("ToolbarFunctions",1))
#WIKIDPAD_PLUGIN = (("MenuFunctions",1), )

import MECplugins_ini

import codecs
import os
import re
import string
import textwrap

from os                             import linesep
from cStringIO                      import StringIO
from string                         import split
from pwiki.StringOps                import mbcsEnc, strftimeUB, pathnameFromUrl
from pwiki.WikiExceptions           import WikiFileNotFoundException
from pwiki.PersonalWikiFrame        import PersonalWikiFrame

from Bio                            import SeqIO
from Bio.Seq                        import Seq
from Bio.SeqUtils                   import GC, seq3
from Bio.SeqUtils.MeltingTemp       import Tm_staluc

from Bio.Alphabet.IUPAC             import extended_protein
from Bio.Alphabet.IUPAC             import protein
from Bio.Alphabet.IUPAC             import ambiguous_dna
from Bio.Alphabet.IUPAC             import unambiguous_dna
from Bio.Alphabet.IUPAC             import extended_dna
from Bio.Alphabet.IUPAC             import ambiguous_rna
from Bio.Alphabet.IUPAC             import unambiguous_rna

from basictm                        import basictm
from pcr_mix                        import PCRmixture
from sequence_filter                import seq_filter
from guess_alpha                    import guess_alphabet
from seq31                          import seq1
from parse_string                   import parse_text_into_list_of_seqs, parse_string_into_formatted_records, parse_raw_sequence_into_fasta
from pcr                            import anneal
from analysis                       import restrictionanalyserecords

def describeMenuItems(wiki):
    return (
            (revcomp,           _(u"MECplugins|DNA Sequence Tools|Reverse complement")             + u"\t",               _(u"revcomp")),
            (comp,              _(u"MECplugins|DNA Sequence Tools|Complement")                     + u"\t",               _(u"comp")),
            (translate,         _(u"MECplugins|DNA Sequence Tools|Translate")                      + u"\t",               _(u"pcr")),
            (tm,                _(u"MECplugins|DNA Sequence Tools|Melting temperature")            + u"\tCtrl-Shift-T",   _(u"tm")),
            (toggle_format,     _(u"MECplugins|DNA Sequence Tools|Toggle sequence formats")        + u"\t",               _(u"toggle_format")),
            (fasta_tab,         _(u"MECplugins|DNA Sequence Tools|fasta->tab format")              + u"\t",               _(u"fasta_tab")),
            (pcr,               _(u"MECplugins|DNA Sequence Tools|PCR simulation")                 + u"\tCtrl-Shift-P",   _(u"pcr")),
            (pcr_mix,           _(u"MECplugins|DNA Sequence Tools|PCR-mix")                        + u"\t",               _(u"PCR-mix")),
            (reanal,            _(u"MECplugins|DNA Sequence Tools|Restriction analysis")           + u"\t",               _(u"reanal")),
            )

def empty(wiki, evt):
    pass

def describeToolbarItems(wiki):
    return (
            (revcomp, "reverse complement", "reverse complement", "reverse_com"),
            (comp, "complement", "complement", "complement"),
            (translate, "translate", "translate", "translate"),
            (tm, "tm", "tm", "tm"),
            (toggle_format,"Toggle format","Toggle format","toggle_format"),
            (pcr, "PCR simulation", "PCR simulation", "pcr"),
            (pcr_mix, "PCR-mix", "PCR-mix", "PCR-mix"),
            (reanal, "resctriction analysis", "resctriction analysis", "digest"),
           )

def revcomp(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    if not raw_sequence:
        return
    sequence = Seq(raw_sequence, ambiguous_dna)
    reverse_complement = sequence.reverse_complement()
    start, end = wiki.getActiveEditor().GetSelection()
    wiki.getActiveEditor().ReplaceSelection(str(reverse_complement))
    wiki.getActiveEditor().SetSelection(start, end)

def comp(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    if not raw_sequence:
        return
    sequence = Seq(raw_sequence, ambiguous_dna)
    complement = sequence.complement()
    start, end = wiki.getActiveEditor().GetSelection()
    wiki.getActiveEditor().ReplaceSelection(str(complement))
    wiki.getActiveEditor().SetSelection(start, end)
    return

def translate(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    if not raw_sequence:
        return
    start, end = wiki.getActiveEditor().GetSelection()
    raw_string = seq_filter(raw_sequence)
    alphabet = guess_alphabet(raw_string)
    #print alphabet
    if alphabet==ambiguous_dna or alphabet==unambiguous_dna or alphabet==extended_dna or alphabet==unambiguous_rna or alphabet==ambiguous_rna:
        sequence = Seq(raw_string, alphabet)
        protein_sequence = str(sequence.translate(to_stop=True))
        protein_sequence ="".join([i+"  " for i in protein_sequence])
    if alphabet==protein or alphabet == extended_protein:
        protein_sequence = seq3(raw_string)
    if alphabet=="three letter code":
        protein_sequence = seq1(raw_string)
    padding = len(raw_sequence)-len(protein_sequence)
    wiki.getActiveEditor().ReplaceSelection(protein_sequence+" "*padding)
    wiki.getActiveEditor().SetSelection(start, start+len(protein_sequence+" "*padding))
    return

def tm(wiki, evt):
    start, end = wiki.getActiveEditor().GetSelection()
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    primer = seq_filter(raw_sequence)

    if primer and 1<len(primer)<13:
        return

    length = len(primer)

    if not primer:

        tm_optimal=53
        length=1

        maxlength = len(wiki.getActiveEditor().GetText())

        while True:
            wiki.getActiveEditor().SetSelection(start,start+length)
            print start,length
            primer = seq_filter(wiki.getActiveEditor().GetSelectedText())
            t=Tm_staluc(primer)
            if t<tm_optimal:
                length+=1
                if length>maxlength:
                    break
            else:
                if int(round(GC(primer)))>45 or length>29:
                    start+=1
                    length=1
                else:
                    break

    wiki.getActiveEditor().SetSelection(start,end)
    #wiki.getActiveEditor().GotoPos(start)

    GCcontent = round(GC(primer),0)
    temperature_staluc  = round(Tm_staluc(primer),1)
    temperature_wallace = basictm(primer)
    if temperature_staluc < 35:
        return
    wiki.displayMessage("Primer melting temperature",
                        "Nearest Neighbour (SantaLucia 1998): %s C\n"
                        "(A+T)*2+(G+C)*4: %s C\n"
                        "GC: %s\n"
                        "length: %s-mer"
    % (str(temperature_staluc),str(temperature_wallace),str(GCcontent),str(len(primer))))

    return

def fasta_tab(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    if not raw_sequence:
        return
    start, end = wiki.getActiveEditor().GetSelection()
    new_sequences=parse_string_into_formatted_records(raw_sequence)
    if not new_sequences:
        return
    out_handle = StringIO()
    for seq in new_sequences:
        SeqIO.write( [seq.record] , out_handle, "tab")
    out_handle.seek(0)
    result_text = out_handle.read()
    wiki.getActiveEditor().ReplaceSelection(result_text)
    wiki.getActiveEditor().SetSelection(start, start+len(result_text))
    return

def toggle_format(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    if not raw_sequence:
        return
    start, end = wiki.getActiveEditor().GetSelection()
    new_sequences=parse_string_into_formatted_records(raw_sequence)
    if not new_sequences:
        new_sequences=parse_raw_sequence_into_fasta(raw_sequence)
    out_handle = StringIO()
    for seq in new_sequences:
        if seq.format == "raw":
            format = "fasta"
        elif seq.format == "embl":
            format = "genbank"
        elif seq.format == "fasta":
            format = "genbank"
        elif seq.format == "tab":
            format = "fasta"
        elif seq.format == "genbank":
            format = "fasta"
            if seq.record.id in ("","."):
                seq.record.id = seq.record.name
            if seq.record.description ==".":
                seq.record.description = ""      

        else:
            format = "fasta"
        SeqIO.write([seq.record] , out_handle, format)
        print >>out_handle,""
    out_handle.seek(0)
    result_text = out_handle.read()
    wiki.getActiveEditor().ReplaceSelection(result_text)
    wiki.getActiveEditor().SetSelection(start, start+len(result_text))
    return

def pcr(wiki, evt):
    #print "ePCR:"
    start, end = wiki.getActiveEditor().GetSelection()
    selected_text = wiki.getActiveEditor().GetSelectedText() #.decode('UTF-8')
    # if nothing was selected
    if not selected_text:
        return
    #make a list of strings of selected text
    lines=selected_text.splitlines()
    #print lines
    #print
    #look for wikiwords to expand, they have to come alone, one per row
    expanded_list=[]
    for line in lines:
        # if the wikiwords are enclosed by [], this should be done better
        strippedline = line.strip("[ ]")
        if wiki.getWikiDocument().isDefinedWikiLink(strippedline):
            pagelines=(linesep + wiki.getWikiDocument().getWikiPage(strippedline).getContent() + linesep).splitlines()
            expanded_list.extend(pagelines)
        else:
            expanded_list.append(line)
    #look for file links, they have to come alone in the begining of each row, one per row
    lines=expanded_list
    expanded_list=[]
    #return
    prog = re.compile(ur'\[*((?:(?:rel)://\S|file://?)(?:[^"\t\n<>\]])*)\]*')
    index=0
    while index<len(lines):
        line=lines[index]
        result = prog.match(line)
        if result:
            foundurl = result.group(1)
            absfoundurl = pathnameFromUrl( wiki.makeRelUrlAbsolute(foundurl) )

            if os.path.isfile(absfoundurl):
                f = open(absfoundurl, 'r')
                filelines=(linesep + f.read() + linesep).splitlines()
                f.close()
                lines=lines[:index] + filelines + lines[index+1:]
                index+=len(filelines)
                filelines=[]

            if os.path.isdir(absfoundurl):
                dirlines=[]
                for file in os.listdir(absfoundurl):
                    f = open( os.path.join(absfoundurl, file), 'r')
                    dirlines+=(linesep+f.read()+linesep).splitlines()
                    f.close()
                lines=lines[:index] + dirlines + lines[index+1:]
                index+=len(dirlines)
                dirlines=[]
        else:
            index+=1

    # get settings

    exec(wiki.getWikiDocument().getWikiPage("WikiSettings/MECplugins/ePCR").getContent().encode())

    if lines.count(template_separator)>1:
        message=wiki.stdDialog("o", "Error in data for ePCR", "too many template separators ("+template_separator+") in the data", additional=None)
        return
    elif lines.count(template_separator)==1:
        index=lines.index(template_separator)
        primertext = linesep.join(lines[:index])+linesep
        primer_sequences = parse_text_into_list_of_seqs(primertext)
        #remove sequence records with no sequence
        primer_sequences = [rec.record for rec in primer_sequences if rec.record.seq]
        templatetext=linesep.join(lines[index+1:])+linesep
        template_sequences = parse_text_into_list_of_seqs(templatetext)
        #remove sequence records with no sequence
        template_sequences = [rec.record for rec in template_sequences if rec.record.seq]

    else:
        #No separator, join all text together
        primer_and_templatetext=linesep.join(lines)+linesep
        #print primer_and_templatetext
        all_sequences = parse_text_into_list_of_seqs(primer_and_templatetext)
        #remove sequence records with no sequence
        all_sequences = [rec.record for rec in all_sequences if rec.record.seq]
        #if there is no template separator, the last sequence is considered the template
        template_sequences = [all_sequences.pop()]
        primer_sequences = all_sequences
    #test if there is at least one non-empty template sequence
    if len(template_sequences)<1:
        message=wiki.stdDialog("o", "Error in data for ePCR", "template empty!", additional=None)
        return
    #test if there is at least one non-empty primer sequence
    if len(primer_sequences)<1:
        message=wiki.stdDialog("o", "Error in data for ePCR", "No primers!", additional=None)
        return

    # prepare report
    result_text=''
    message_template = report_header

    for template in template_sequences:

        anneal_primers = anneal(primer_sequences, template)

        if str(anneal_primers):
            message_template += report_for_each_simulation

        if anneal_primers.products():

            for ampl in anneal_primers.amplicons:

                forward_primer_name           = ampl.forward_primer.primer.name
                forward_primer_sequence       = ampl.forward_primer.primer.seq
                reverse_primer_name           = ampl.reverse_primer.primer.name
                reverse_primer_sequence       = ampl.reverse_primer.primer.seq
                product_name                  = ampl.product.name
                product_sequence              = ampl.product.seq
                template_name                 = anneal_primers.template.name
                template_sequence             = anneal_primers.template.seq
                upstream_flanking_sequence    = ampl.flankup
                downstream_flanking_sequence  = ampl.flankdn
                figure                        = ampl.detailed_figure()

                message_template += report_for_each_amplicon

                result_text+=linesep+string.Template(message_template).safe_substitute(locals())
                message_template=''

    if not result_text:
        result_text=linesep+str(anneal_primers)

    #print str(anneal_primers)

    wiki.getActiveEditor().GotoPos(end)
    wiki.getActiveEditor().AddText(result_text)
    wiki.getActiveEditor().SetSelection(end+1, end+len(result_text))

    return

def pcr_mix(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    start, end = wiki.getActiveEditor().GetSelection()
    if not raw_sequence:
        result_text='''PCR volume(s) (volume x no of tubes) 50 x 1 + 20 x 1

template (v/v) 2.5 %

primer 1 fwdprimername stock 10 uM , final 1 uM
primer 2 revprimername stock 10 uM , final 1 uM

buffer 10xTaq Buffer w (NH4)2SO4 stock 10.0 x , final 1.0 x

MgSO4 homemade 2009-03-23 stock 50.0 mM , final 2.0 mM

dNTP stock 1.0 mM , final 100.0 uM

DNA pol (v/v) 2.0 %
extra volume 10.0 %

#	mm	temp	Description
r1	48.75	1.25    template
r2	19.5	0.5	    negative control
'''
    else:

        result_text = "+++ PCR "+strftimeUB("%Y-%m-%d %H:%M:%S")+"\n"
        result_text+= PCRmixture(raw_sequence).result_text
    wiki.getActiveEditor().ReplaceSelection(result_text)
    wiki.getActiveEditor().SetSelection(start, start+len(result_text))
    return

def reanal(wiki, evt):
    raw_sequence = wiki.getActiveEditor().GetSelectedText()
    start, end = wiki.getActiveEditor().GetSelection()
    if not raw_sequence:
        return
    new_sequences=parse_string_into_formatted_records(raw_sequence)
    if not new_sequences:
        return
    result_text=restrictionanalyserecords(new_sequences)
    wiki.getActiveEditor().GotoPos(end)
    wiki.getActiveEditor().AddText(result_text)
    wiki.getActiveEditor().SetSelection(end+1, end+len(result_text))
    #wiki.getActiveEditor().GotoPos(start)
    return
