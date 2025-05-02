import numpy as np

def get_nodes(all_lines):                           #This function gets all the distinct nodes and stores them in 'nodes' list by their original name. So we also have the number of nodes.
    nodes = []
    for line in all_lines:                          #This includes GND as well
        if line[1] not in nodes :
            nodes.append(line[1])
        if line[2] not in nodes :
            nodes.append(line[2])
    #print(nodes)
    no_of_nodes = len(nodes)
    return nodes

def get_vol_sources(all_lines):                     #This gets the number of voltage soures present in the circuit.
    no_of_vol_sources = 0
    for line in all_lines:
        if 'V' in line[0]:
            no_of_vol_sources += 1
    return no_of_vol_sources

def get_curr_sources(all_lines):                    #This function gets the number of current sources present in the circuit.
    no_of_curr_sources = 0
    for line in all_lines:
        if 'I' in line[0]:
            no_of_curr_sources += 1
    return no_of_curr_sources

def Convert_vol_sources(all_lines):                 #This function takes care about converting the names of the voltage sources. If there is voltage source names'Vsource',it gets converted to V1
    no = 1
    all_vol_sources = {}
    for line in all_lines:
        if 'V' in line[0]:
            line[0] = 'V' + str(no)
            all_vol_sources[line[0]] = no           #It also creates a dictionary that stores converted names of voltage sources as keys and their number as the value.
            no += 1
    return all_vol_sources                          #It returns that dictionary

def Convert_cur_sources(all_lines):                 #This function takes care about converting the names of the current sources. If there is current source names'Isource',it gets converted to I1
    no = 1
    all_curr_sources = {}
    for line in all_lines:
        if 'I' in line[0]:
            line[0] = 'I' + str(no)
            all_curr_sources[line[0]] = no          #It also creates a dictionary that stores converted names of current sources as keys and their number as the value.
            no += 1
    return all_curr_sources                         #It returns the dictionary.

def Convert_nodes(all_lines):                       #This function converts the node names to standard n1,n2...
    nodes = get_nodes(all_lines)
    converted_nodes = {}                            #It also creates a dictionary with converted node names= keys to number assigned to them = value
    for node in nodes:
        if node == 'GND':                           #If the node is GND then we set its number to default 0
            converted_nodes[node] = 0
        else:
            no = [int(c) for c in node if c.isdigit()][0]   #The number is recieved from the node name itself to get the ordered rows in the final matrix n1,n2,n3....
            converted_nodes[node] = no
    return converted_nodes

def G_matrix(all_lines):                            #This is the top left part of the matrix that contains the Kirchoff equation at the nodes.
    size = len(Convert_nodes(all_lines)) - 1
    G = [[0 for _ in range(size)] for _ in range(size)]
    nodes = Convert_nodes(all_lines)

    for line in all_lines:                          #For each node, did +- 1/Rvalue for each R in the circuit given.I initiealised a G matrix of calculated size with 0s and then added these values at the correct place. 
        if 'R' in line[0]:
            node_1 = line[1]
            node_2 = line[2]
            node_1_no = nodes[node_1]
            node_2_no = nodes[node_2]
            if node_1_no == 0:
                G[node_2_no - 1][node_2_no - 1] += float(1/float(line[3]))
            if node_2_no == 0:
                G[node_1_no - 1][node_1_no - 1] += float(1/float(line[3]))
            if node_1_no != 0 and node_2_no != 0:
                G[node_1_no - 1][node_2_no - 1] += float(-1/float(line[3]))
                G[node_2_no - 1][node_2_no - 1] += float(1/float(line[3]))
                G[node_2_no - 1][node_1_no - 1] += float(-1/float(line[3]))
                G[node_1_no - 1][node_1_no - 1] += float(1/float(line[3]))
    return G

def B_matrix(all_lines):                            #This is the matrix which is the top left part of the matrix. It involves the part where we include the currents through the voltage spurces in each of the node kirchoff equations.
    rows = len(Convert_nodes(all_lines)) - 1
    cols = get_vol_sources(all_lines)
    B = [[0 for _ in range(cols)] for _ in range(rows)]
    nodes = Convert_nodes(all_lines)

    for line in all_lines:                          #I identify each of the voltage source and according to which side it faces, the sign of the value to be added is decided.
        if 'V' in line[0]:
            node_1 = line[1]
            node_2 = line[2]
            node_1_no = nodes[node_1]
            node_2_no = nodes[node_2]
            if node_1_no == 0:
                B[node_2_no - 1][0] += -1
            if node_2_no == 0:
                B[node_1_no - 1][0] += 1
            if node_1_no != 0 and node_2_no != 0:
                B[node_1_no - 1][0] += 1
                B[node_2_no - 1][0] += -1  
    return B

def C_matrix(all_lines):                            #This form the transpose of the B matrix. This is at the bottom right of the A matrix. This contains the equations for the Voltage sources that is the V = difference between node voltages.
    B = B_matrix(all_lines)
    C = [[B[i][j] for i in range(len(B))]for j in range(len(B[0]))]
    return C

def D_matrix(all_lines):                            #This is the bottom right of the matrix.By inspection, it is always 0.
    size  = get_vol_sources(all_lines)
    D = [[0 for i in range(size)]for j in range(size)]
    return D

def z(all_lines):                                   #This function gets the z matrix in Ax=z which contains all the currents that are coming to the respective nodes due to the current sources. Ans then the voltage sources values in order. 
    vol_sources = Convert_vol_sources(all_lines)
    curr_sources = Convert_cur_sources(all_lines)
    nodes = Convert_nodes(all_lines)
    down = np.array([[0.00000] for i in range(get_vol_sources(all_lines))])
    up = np.array([[0.000000] for i in range(len(nodes) - 1)])

    for line in all_lines:
        if 'V' in line[0]:
            no = vol_sources[line[0]]
            down[no - 1] += float(line[4])
        if 'I' in line[0]:
            node_1 = line[1]
            node_2 = line[2]
            node_1_no = nodes[node_1]
            node_2_no = nodes[node_2]
            if node_1_no != 0:
                up[node_1_no-1] += -float(line[4])
            if node_2_no != 0:
                up[node_2_no-1] += float(line[4])
    z = np.vstack((up,down))                        #I have made 2 numpy arrays for both the things described above and then stacked them vertically to get the final matrix.
    return z

def get_voltages(x,all_lines):                      #This function is called after solving the equations. We assign the node voltages to the perticular nodes by a dictionary to get the answers as written in the instruction.
    voltages = {}
    nodes = Convert_nodes(all_lines)
    for node in nodes:
        if node == 'GND':
            voltages[node] = 0
        else:
            voltages[node] = x[nodes[node]-1][0]
    return voltages

def get_currents(x,all_lines,vol_source_names):                      #This function takes all the currents in the voltage sources calculated and assigns it to the respective voltage sources for getting the answers in the form asked.
    currents = {}

    vol_sources = Convert_vol_sources(all_lines)
    nodes = get_nodes(all_lines)
    current_values = x[len(nodes)-1:]  
    
    i = 0
    for source in vol_sources:
        currents[vol_source_names[i]] = current_values[vol_sources[source] - 1][0]
        i += 1
    return currents

def check_invalid_element(all_lines):               #This is the edge cae considered. If input file has any element except R,V,I then it produces a value error. 
    for line in all_lines:
        if 'R' in line[0] or 'V' in line[0]  or 'I' in line[0]:
            pass 
        else: 
            raise ValueError('Only V, I, R elements are permitted')
            


def evalSpice(filename):                            #The main function
    try:                                            #Considered the file not found error
        f = open(filename,"r")
    except:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')
    all_lines = []
    for line in f.readlines():                      #This opens the file and reads it line by line and stores each line in a different element in a list .
        all_lines.append(line.split())

    try:
        circuit_index = all_lines.index([".circuit"])   #This is to delete all the portions which not in between .circuit and .end from the list. And to remove the .circuit and .end componenets also.
        del all_lines[:circuit_index]                   #The comments inside the portion is already taken into account. As even if they are stored in a list, they are ignored as I have indexed to get anything from the list element
        end_index = all_lines.index(['.end'])
        del all_lines[end_index+1:]
        all_lines.remove(['.circuit'])
        all_lines.remove(['.end'])
    except:                                              #Considered the value not found error
        raise ValueError('Malformed circuit file')

    check_invalid_element(all_lines)

    vol_source_names = [i[0] for i in all_lines if 'V' in i[0]]

    Convert_vol_sources(all_lines)
    Convert_cur_sources(all_lines)
    b = Convert_nodes(all_lines)
    Gk = G_matrix(all_lines)                        #I form all the matrices 
    Bk = B_matrix(all_lines)
    Ck = C_matrix(all_lines)
    Dk = D_matrix(all_lines)

    G = np.array(Gk)                                #Now I convert all the list matrices to numpy arrays.
    B = np.array(Bk)
    C = np.array(Ck)
    D = np.array(Dk)
    
    top = np.hstack((G,B))                          #I stack them according to the geometry specified above
    bottom = np.hstack((C,D))
    try:                                            #Case of only i sources
        A = np.vstack((top,bottom))
    except:
        raise ValueError('Circuit error: no solution')
    Z = z(all_lines)

    try:                                            #Test case taken into account. If the determinant of A is zero then it raises the valueerror. This takes the test_v_loop case into account.
        X = np.linalg.solve(A , Z)                  #I have solved for the node voltages and sources currents using the function specified.
    except Exception :
        raise ValueError('Circuit error: no solution')

    print(X)
    ans_voltages = get_voltages(X,all_lines)
    ans_currents = get_currents(X,all_lines,vol_source_names)

    print(ans_currents)
    return (ans_voltages, ans_currents)

if __name__ == "__main__":
    filename = 'testdata/test_v_loop.ckt'
    V,I = evalSpice(filename)
    print(I)
