#!/usr/bin/env python
# -*- coding: utf-8 -*-

def expandtolist(content):
    __version__=001
    import re,string,sys,itertools,math,pprint
    resultlist=[]
    for line in re.finditer("([^\(\)]*?)(\[.*?\])", content):
        text2rep = line.group(1)
        bracket =  line.group(2)
        inbracket = [item.strip("[ ]") for item in bracket.split(",")]
        expanded = []
        for item in inbracket:
            if re.match("(\d+\.\.\d+)|([a-z]+\.\.[a-z]+)|([A-Z]+\.\.[A-Z]+)",item):
                low, high = item.split("..",)
                if low.isdigit() and high.isdigit():
                    r = [str(x) for x in range (int(low), 1+int(high))]
                if (low.islower() and high.islower()) or (low.isupper() and high.isupper()):
                    r = [chr(a) for a in range(ord(low),1+ord(high))]
                expanded.extend(r)
            else:
                expanded.append(item.strip())

        resultlist.append([text2rep+" "+x for x in expanded])

    ml = max([len(x) for x in resultlist])
    norm = []
    for r in resultlist:
        mp = int(math.ceil(float(ml)/float(len(r))))
        norm.append(list(itertools.chain.from_iterable(zip(*(r,)*mp))))

    #pprint.pprint(norm)
    rt=""
    for a in range(ml):
        rt +="".join([b[a] for b in norm])+"\n"
    return rt


if __name__=="__main__":
    content = "lane [1..4] clone [1,2]"
    print content
    print expandtolist(content)
