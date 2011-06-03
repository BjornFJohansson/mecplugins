def argsparse(argument):

    import argparse

    parser = argparse.ArgumentParser(description='PCR simulation options')
    parser.add_argument('-c'    ,'--circ'       ,'--circular', action='store_true')
    parser.add_argument('-gb'   ,'--genbank'    ,              action='store_true')
    parser.add_argument('-v'    ,'--verbosity'  ,              type=int )
    parser.add_argument('-f'    ,'--files'      ,              nargs='+')
    parser.add_argument('-p'    ,'--primers'    ,              nargs='+')    
    parser.add_argument('-t'    ,'--templates'  ,              nargs='+')   

    args = parser.parse_args(argument.split())

    print args



    # PCR --primers primers.txt --templates templates.txt --output prod.txt -verbose 3

    # -o, --output                  use as output file
    # -v, --verbose                 verbose
    # -a, --anneal-only             report primer annealing only


if __name__=="__main__":
    
    argsparse("-gb --genbank")