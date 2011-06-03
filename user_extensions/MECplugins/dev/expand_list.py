#!/usr/bin/env python
# -*- coding: latin-1 -*-
import sys
import string
from pyparsing import Word, Literal, alphas, printables, LineStart, White, SkipTo, Combine, nums, And, ZeroOrMore, Optional, LineEnd, delimitedList, alphanums, srange, OneOrMore

range_pat = OneOrMore(  Word("(",max=1) + Word(nums)  +   Optional(   Word(",",max=1).suppress()  |   Word("..",max=1) ) + Word(")",max=1) )
reaction_pat = LineStart()+OneOrMore(SkipTo(range_pat)+range_pat)

result = reaction_pat.scanString("plate (1..2,6..8) slot (1..4,9) W303-1B")



#for data,dataStart,dataEnd in result:
#    print data
#    rawlist = list(data)
#    for a in range(rawlist.count("..")):
#        index = rawlist.index("..")
#        lo = rawlist.pop(index-1)
#        hi = rawlist.pop(index)
#        rawlist = rawlist[:index-1]+range(int(lo),int(hi)+1)+rawlist[index:]
#        #rawlist[index-1] = range(int(lo),int(hi)+1)

#for index,item in enumerate(rawlist):
#    if type(item)==str and item.isdigit():
#        rawlist[index] = int(item)

#newlist=[]
#index = 0

#while index<len(rawlist):

#    if type(rawlist[index])==str:
#        newlist.append([rawlist[index].strip()])
#        index=index+1
#    if type(rawlist[index])==int:
#        templist=[]
#        while index<len(rawlist) and type(rawlist[index])==int:
#            templist.append(rawlist[index])
#            index=index+1

#        newlist.append(templist)
#print
#print newlist
#print

#lenlist=[]

#for item in newlist:
#    lenlist.append(len(item))

#maxint = max(lenlist)
#newerlist=[]

#for item in newlist:
#    if len(item)<max:
#        item = item*int(round((maxint/len(item))))
#    newerlist.append(item)

#result_list=[""]*maxint

#for item in newerlist:
#    row=""
#    for y,val in enumerate(item):
#        result_list[y]+=str(val)+" "

#for row in result_list:
#    print row