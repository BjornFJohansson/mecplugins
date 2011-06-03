table='''123 456         
789   abc           
cde fgh           
'''

# http://code.activestate.com/recipes/410687-transposing-a-list-of-lists-with-different-lengths/
# http://docs.python.org/tutorial/controlflow.html#tut-unpacking-arguments
print table
import string, array

rows=[row.strip() for row in table.splitlines()]

no_rows  = len(rows)

no_cols = max([len(row) for row in rows]) 

rows = [row.ljust(no_cols) for row in rows]

trows = zip(*rows)

rows = ["".join(a) for a in trows]

print rows.index(" "*no_rows)

print zip(*rows)



d=[]

for column in range(maxrowlength):
    c=[]
    for row in rows:
        c.append(row[column])
    d.append("".join(c))

max = d.index("   ")

rows = d[:max]
gg= []

for column in range(3):
    c=[]
    for row in rows:
        c.append(row[column])
    gg.append("".join(c))
    
print gg