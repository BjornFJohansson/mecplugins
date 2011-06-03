table='''123 456 eee  
789   abc rrr          
cde fgh nnn          
'''

# http://code.activestate.com/recipes/410687-transposing-a-list-of-lists-with-different-lengths/
# http://docs.python.org/tutorial/controlflow.html#tut-unpacking-arguments
#print table
import string, array

rows=[row.strip() for row in table.splitlines()]

no_rows  = len(rows)

no_cols = max([len(row) for row in rows]) 

rows = [row.ljust(no_cols) for row in rows]

trows = zip(*rows)

rows = ["".join(a) for a in trows]


(rows.index((" "*no_rows,last)


#print zip(*rows)

