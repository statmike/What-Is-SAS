myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

print(myfamily)
print(myfamily['child1'])
temp1='child1'
print(myfamily[temp1])
print(myfamily)
if temp1 in myfamily: print('yes')
temp2='name'
if temp2 in myfamily[temp1]: print('yes')
