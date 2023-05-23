
def read_vars(input_file):

    f = open(input_file,'r')
    headers = f.readline()
    headers = headers[:len(headers)-1]
    headers = headers.split('\t') 
    vars = [[] for i in range(len(headers))]

    for line in f.readlines():
        line=line[:len(line)-1]
        strings = line.split('\t')
        for l in range(len(vars)):
            vars[l].append(float(strings[l]))

    #Find the variable to plot based on the input
    outVars = {}
    for i,varName in enumerate(headers):
        outVars[varName]=vars[i]
    return outVars