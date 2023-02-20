import requests
import re

res = requests.get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
anyth = res.text.split()


def solve(s):
   regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
   if re.fullmatch(regex,s):
      slevel = s.split('@')[1]
      print(slevel)
      toplvl = slevel.split('.')[1]
      print(toplvl)
      if toplvl.upper() in anyth:
         return s
      else:
         return (s + " not in the list")
   else:
      return "not valid email"
         
         

s = "good@food.bh"
print(solve(s))
