from Bio.Seq import Seq
import random

def randomRNA(length,interval=0):
    return Seq(''.join([random.choice('GAUC') for x in range(length+int(random.triangular(-interval,interval)))]))    

def randomDNA(length,interval=0):
    return Seq(''.join([random.choice('GATC') for x in range(length+int(random.triangular(-interval,interval)))]))

def randomprot(length,interval=0):
    return Seq(''.join([random.choice('ACDEFGHIKLMNPQRSTVWY') for x in range(length+int(random.triangular(-interval,interval)))]))


if __name__ == '__main__':
    for a in range(10):
        print randomRNA(20)
    print
    for a in range(10):
        print randomDNA(20)
    print
    for a in range(10):
        print randomprot(20)
    print
    for a in range(10):
        print randomRNA(20,10)
    print
    for a in range(10):
        print randomDNA(20,10)
    print
    for a in range(10):
        print randomprot(20,10)
