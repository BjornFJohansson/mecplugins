def SIprefix(prefix):
    import math
    prefix_dict = {
    'Y':    24,	    #yotta
    'Z':	21,	    #zetta
    'E':	18,	    #exa
    'P':	15,	    #peta
    'T':	12,	    #tera
    'G':	9,	    #giga
    'M':	6,	    #mega
    'k':	3,	    #kilo
    'h':	2,	    #hecto
    'da':	1,	    #deka
    'd':	-1, 	#deci
    'c':	-2,	    #centi
    'm':	-3,	    #milli
    'u':	-6,	    #micro
    'n':	-9,	    #nano
    'p':	-12,	#pico
    'f':	-15,	#femto
    'a':	-18,	#atto
    'z':	-21,	#zepto
    'y':	-24,	#yocto
    }
        
    return float(10**int(prefix_dict[prefix]))
    
if __name__=="__main__":
    print SIprefix("m")
    print SIprefix("u")
    print SIprefix("n")
    print SIprefix("p")