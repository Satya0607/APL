import numpy as np
import sys

#getting element name
def element_type(token):
    if token[0] == 'R':
        return 'Resistor'
    elif token[0] == 'L':
        return 'Inductor'
    elif token[0] == 'C':
        return 'Capacitor'
    elif token[0] == 'V':
        return 'Indep voltage source'
    elif token[0] == 'I':
        return 'Indep current source'


class req_quan():  # Defined a class for the elements
    def __init__(self, line):
        self.line = line
        self.words = self.line.split()
        self.name = element_type(self.words[0])
        self.first_node = self.words[1]
        self.to_node = self.words[2]

        if len(self.words) == 5:
            self.type = 'dc'
            self.value = float(self.words[4])  #converting into floating point

        elif len(self.words) == 6:
            self.type = 'ac'
            Vm = float(self.words[4]) / 2    #we should divide by 2 because they have given peak to peak voltage
            phase = float(self.words[5])
            re = Vm * np.cos(phase)
            img = Vm * np.sin(phase)
            self.value = complex(re, img)

        else:
            self.type = 'RLC'
            self.value = float(self.words[3])

def freq(lines):  # This function returns the frequency of the source
    freqn = 0
    for line in lines:
        if line[:3] == '.ac':
            freqn = float(line.split()[2])
    return freqn


def get_key(d, value):  # Gets the corresponding key for a value in the dictionary
    for key in d.keys():
        if d[key] == value:
            return key


def node_map_dict(circuit):  # Returns a dictionary of nodes from the circuit definition.
    dict = {"GND": 0}
    nodes = [req_quan(line).first_node for line in circuit]
    nodes.extend([req_quan(line).to_node for line in circuit])
    nodes = list(set(nodes))  # to get distinct nodes
    nodes.remove("GND")
    nodes = sorted(nodes)
    nodes.append("GND")
    print("The nodes are")
    print(nodes)
    count = 1
    for node in nodes:
        if node != 'GND':
            dict[node] = count
            count += 1
    return dict


def make_dict(circuit, e):  # Makes a dictionary for each component of the particular type of element
    d = {}
    ele_names = [req_quan(line).words[0] for line in circuit if req_quan(line).words[0][0] == e]
    for i, name in enumerate(ele_names):
        d[name] = i
    return d


def pos_of_node(circuit, node_key, node_mapped):  # Finds the lines and position ie from/to of the given node
    indices = []
    for i in range(len(circuit)):
        for j in range(len(circuit[i].split())):
            if circuit[i].split()[j] in node_mapped.keys():
                if node_mapped[circuit[i].split()[j]] == node_key:
                    indices.append((i, j))


    return indices


def update_matrix(node_key):  # This update the M and b matrix for the given node
    indices = pos_of_node(circuit, node_key, node_mapped)
    for ind in indices:
        # getting all the attributes of the element using the class definition
        element = req_quan(circuit[ind[0]])
        ele_name = circuit[ind[0]].split()[0]
        # resistors
        if ele_name[0] == 'R':
            if ind[1] == 1:  # from_node
                adj_key = node_mapped[element.to_node]
                M[node_key, node_key] += 1 / element.value
                M[node_key, adj_key] -= 1 / element.value

            if ind[1] == 2:  # to_node
                adj_key = node_mapped[element.first_node]
                M[node_key, node_key] += 1 / element.value
                M[node_key, adj_key] -= 1 / element.value
                # inductors
        if ele_name[0] == 'L':
            try:
                if ind[1] == 1:
                    adj_key = node_mapped[element.to_node]
                    M[node_key, node_key] -= complex(0, 1 / (2 * np.pi * freqn * element.value))
                    M[node_key, adj_key] += complex(0, 1 / (2 * np.pi * freqn * element.value))
                if ind[1] == 2:
                    adj_key = node_mapped[element.first_node]
                    M[node_key, node_key] -= complex(0, 1 / (2 * np.pi * freqn * element.value))
                    M[node_key, adj_key] += complex(0, 1 / (2 * np.pi * freqn * element.value))
            except ZeroDivisionError:  # in dc case as w = 0 inductor becomes short circuit in steady state
                i = ind_dict[ele_name]
                if ind[1] == 1:
                    adj_key = node_mapped[element.to_node]
                    M[node_key, n + p + i] += 1
                    M[n + p + i, node_key] -= 1
                    b[n + p + i] = 0
                if ind[1] == 2:
                    M[node_key, n + p + i] -= 1
                    M[n + p + i, node_key] += 1
                    b[n + p + i] = 0
        # capacitors
        if ele_name[0] == 'C':
            if ind[1] == 1:  # from_node
                adj_key = node_mapped[element.to_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * freqn * element.value)
                M[node_key, adj_key] -= complex(0, 2 * np.pi * freqn * element.value)
            if ind[1] == 2:  # to_node
                adj_key = node_mapped[element.first_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * freqn * element.value)
                M[node_key, adj_key] -= complex(0, 2 * np.pi * freqn * element.value)
        # independent voltage source
        if ele_name[0] == 'V':
            index = volt_dict[ele_name]
            if ind[1] == 1:
                adj_key = node_mapped[element.to_node]
                M[node_key, n + index] += 1
                M[n + index, node_key] -= 1
                b[n + index] = element.value
            if ind[1] == 2:
                adj_key = node_mapped[element.first_node]
                M[node_key, n + index] -= 1
                M[n + index, node_key] += 1
                b[n + index] = element.value
        # independent current source
        if ele_name[0] == 'I':
            if ind[1] == 1:
                b[node_key] -= element.value
            if ind[1] == 2:
                b[node_key] += element.value


# main function
if len(sys.argv) != 2:
    sys.exit("Invalid number of arguments! Pass the netlist file as the second argument.")
try:
    with open(sys.argv[1]) as f:
        CIRCUIT = ".circuit"
        END = ".end"
        AC = '.ac'
        lines = f.readlines()

        freqn = freq(lines)  # frequency of the source, currently supports only single frequency circuits
        start = 0
        end = 1
        for line in lines:  # extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[:len(END)]:
                end = lines.index(line)
                break
        if start >= end:  # validating circuit block
            print('The circuit is invalid')
            exit(0)

        circuit = []
        for line in [' '.join(line.split('#')[0].split()) for line in lines[start + 1:end]]:
            circuit.append(line)

        node_mapped = node_map_dict(circuit)
        # table of distinct nodes present in the circuit
        # numbers assigned to the nodes correspond to the rows of the incidence matirx

        volt_dict = make_dict(circuit, "V")
        ind_dict = make_dict(circuit, 'L')

        p = len([i for i in range(len(circuit)) if circuit[i].split()[0][0] == 'V'])
        n = len(node_mapped)
        # dimension of M if source acts as AC.
        dim = n + p

        # if source is DC, we need to add inductors also

        if freqn == 0:  # dc signal, l acts as closed wire in steady state.
            M = np.zeros((dim + len(ind_dict), dim + len(ind_dict)), dtype=complex)
            b = np.zeros(dim + len(ind_dict), dtype=complex)
        else:
            M = np.zeros((dim, dim), dtype=complex)
            b = np.zeros(dim, dtype=complex)

        for i in range(len(node_mapped)):  # update matrix for the ith node
            update_matrix(i)
        # as Vgnd = 0
        M[0] = 0
        M[0, 0] = 1

        # M and b arrays are constructed
        print('The dictionary of nodes is :', node_mapped)
        print('M = :\n', M)
        print('b = :\n', b)

        # solve Mx = b
        try:
            x = np.linalg.solve(M, b)
        except Exception:
            print('The incidence matrix cannot be inverted as it is a singular matrix.')
            sys.exit()

        print('convention(voltage) : Assumed first node is at a lower potential')

        for i in range(n):
            x[i] = np.round(x[i], 6)
            print("Node {} voltage = {}".format(get_key(node_mapped, i), x[i]))
        for j in range(p):
            print('Current through source {} is {}'.format(get_key(volt_dict, j), x[n + j]))
        if freqn == 0:
            for i in range(len(ind_dict)):
                print("Current through inductor {} is {}".format(get_key(ind_dict, i), x[n + p + i]))


except IOError:
    print('Invalid file')
    exit()