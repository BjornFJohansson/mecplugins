def basictm(p):
    #Tm= (wA+xT) * 2 + (yG+zC) * 4
    prim = str(p).lower()
    tm = (prim.count("a")+prim.count("t"))*2 + (prim.count("g")+prim.count("c"))*4
    return tm

