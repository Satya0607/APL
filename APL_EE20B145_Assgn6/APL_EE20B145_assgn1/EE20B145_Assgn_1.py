
# importing sys library
import sys

CIRCUIT = ".circuit"
END = ".end"


# Extracting the tokens from a Line
def line2tokens(spiceLine):
    reqWords = spiceLine.split()

    # for R, L, C, Independent Sources
    if len(reqWords) == 4:
        elementName = reqWords[0]
        node1 = reqWords[1]
        node2 = reqWords[2]
        value = reqWords[3]
        return [elementName, node1, node2, value]

    # for CCxS
    elif len(reqWords) == 5:
        elementName = reqWords[0]
        node1 = reqWords[1]
        node2 = reqWords[2]
        voltageSource = reqWords[3]
        value = reqWords[4]
        return [elementName, node1, node2, voltageSource, value]

    # for VCxS
    elif len(reqWords) == 6:
        elementName = reqWords[0]
        node1 = reqWords[1]
        node2 = reqWords[2]
        voltageSourceNode1 = reqWords[3]
        voltageSourceNode2 = reqWords[4]
        value = reqWords[5]
        return [elementName, node1, node2, voltageSourceNode1, voltageSourceNode2, value]

    else:
        return []


def printCktDefn(SPICELinesTokens):
    for x in SPICELinesTokens[::-1]:
        for y in x[::-1]:
            print(y, end=' ')
        print('')
    print('')
    return

    # checking number of command line arguments
if len(sys.argv) != 2:
    sys.exit("Invalid number of arguments! Pass the netlist file as the second argument.")
else:
    try:
        circuitFile = sys.argv[1]

            # checking if given netlist file is of correct type
        if not circuitFile.endswith(".netlist"):
            print("Wrong file")
        else:
            with open(circuitFile, "r") as f:
                SPICELines = []
                for line in f.readlines():
                    SPICELines.append(line.split('#')[0].split('\n')[0])
                try:
                     # finding the location of the identifiers
                    identifier1 = SPICELines.index(CIRCUIT)
                    identifier2 = SPICELines.index(END)

                    SPICELinesActual = SPICELines[identifier1 + 1:identifier2]
                    SPICELinesTokens = [line2tokens(line) for line in SPICELinesActual]

                    # Printing Circuit Definition in Reverse Order
                    printCktDefn(SPICELinesTokens)
                except ValueError:
                    print("Given format is incorrect! Make sure to have .circuit and .end lines in the file.")
    except FileNotFoundError:
        print("Given file does not exist!")
