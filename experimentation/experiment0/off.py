
f = open("3gb.vcf", "r")

# You can copy any offset from offset.txt file to get to that position directly without linear probing 
f.seek(105528005)
for line in f :
    print(line)
    break