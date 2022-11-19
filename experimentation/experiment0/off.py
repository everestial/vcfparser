
f = open("100mb.vcf", "r")

# You can copy any offset from offset.txt file to get to that position directly without linear probing 
f.seek(61846821)
for line in f :
    print(line)
    break