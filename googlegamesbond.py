
from PIL import Image

bond_before = Image.open("images/bond.png.bak")
bond_after= Image.open("images/bond.png")

first  = bond_before.getdata()
second = bond_after.getdata()
listf = list(first)
lists = list(second)

difference = []
for i in range(len(list(first))):
    if listf[i] != lists[i]:
        difference.append(i)

#print(difference)
print(len(first))
print(len(second))
