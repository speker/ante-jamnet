fin = open("/etc/dhcpcd.conf", "rt")
#output file to write the result to
fout = open("/etc/dhcpcd.conf", "wt")
#for each line in the input file
for line in fin:
    #read replace the string and write to output file
    fout.write(line.replace('# fallback to static profile on eth', '# fallback to static profile on ethrrrr'))
#close input and output files
fin.close()
fout.close()