import argparse

parser = argparse.ArgumentParser(description='Process opts')

parser.add_argument("-o","--overlap", action='store_true')

parser.add_argument("-d","--diff","--difference", action='store_true')

parser.add_argument("-f","--files", metavar='hej')

##                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')


args = parser.parse_args()

print args
