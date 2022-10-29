from calendar import TUESDAY
from tabulate import tabulate
table=[['sunday','monday','tuesday'],['wednesday','thursday','friday'],'saturday']
print(tabulate(table,tablefmt='grid'))
