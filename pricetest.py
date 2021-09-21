import pickle
import os
from Price import PriceHandler

# Price program

class_names = pickle.loads(open('classnames.txt', "rb").read()) 
path = os.path.join(os.getcwd(), 'pricelist.csv')
header = ['name', 'price_kg']

# Make new instance of PriceHandler
p1 = PriceHandler(path, header, class_names)
# Run menu from which you can access the PriceHandler methods quite easily
p1.menu()    





