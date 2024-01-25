# Line 1: A list of states, Q, separated by tabs.
# Line 2: A list of the symbols in Σ, separated by tabs. The Empty string
# will not be explicitly included. You can assume that the state names do not
# also appear in the alphabet.
# Line 3: The start state, q0 ∈ Q.
# Line 4: The set of valid accept states, F , separated by tabs.
# Line 5: The token BEGIN to denote the start of the transition function
# Line 6 to line before last: The transition function. Each line will
# be of the form s, x = sf
# . This is translated to mean that reading
# symbol x in state s causes a transition to state sf
# . The string EPS will
# be used to represent an epsilon transition.
# Last Line: The token END to denote the end of the transition
# function.

# The output should be to a text file with the extension .DFA. The
# output should have the same format as above. You may use the symbol
# EM to represent the empty state, ∅. If {1} and {2} are states in the
# NFA that are combined in the DFA, represent the state with the string
# {1, 2}.

import sys


# THIS IS DOGSHIT SPAGHETTI CODE BUT IT WORKS AND SPAGHETTI IS DELICIOUS
# global variables
STATES = []
ALPHABET = []
START_STATE = ""
ACCEPT_STATES = []

DFA_START_STATE = []
DFA_ACCEPT_STATES = []


# Define a nested dictionary to represent state transitions
NFA_TRANSITIONS = {}

DFA_TRANSITIONS = {}

VISITED = set()

def openFile(input_file):
    # open file
    file = open(input_file, "r")
    # read file
    readNFA(file)
    # close file
    file.close()

def printInfo():
    print("STATES: " + str(STATES))
    print("ALPHABET: " + str(ALPHABET))
    print("START STATE: " + START_STATE)
    print("ACCEPT STATES: " + str(ACCEPT_STATES))

def readNFA(file):
    global START_STATE  # Declare START_STATE as a global variable

    file_iterator = iter(file)

    states = next(file_iterator).split("\t")
    for state in states:
        STATES.append(state.strip())
    # add states to the nested dictionary
    for state in states:
        NFA_TRANSITIONS[state.strip()] = {}

    alphabet = next(file_iterator).split("\t")
    for symbol in alphabet:
        ALPHABET.append(symbol.strip())
    ALPHABET.append("EPS")
    # add symbols to the nested dictionary
    for state in STATES:
        for symbol in ALPHABET:
            NFA_TRANSITIONS[state][symbol] = []

    start_line = next(file_iterator)
    #print("START LINE: " + start_line)
    START_STATE = start_line.strip()  # Set START_STATE value

    accept_states = next(file_iterator).split("\t")
    for state in accept_states:
        ACCEPT_STATES.append(state.strip())

    #printInfo()

    if (next(file_iterator).strip() == "BEGIN"):
        # read transition functions
        line = next(file_iterator)
        #print(line)
        while (line.strip() != "END"):
            # transition is in the form of state, symbol = state
            transition = line.split(",")
            # split 2nd entry of transition into symbol and state
            symbol_state = transition[1].split("=")
            #symbol_state[1] = symbol_state[1].strip()
            transition[1] = symbol_state[0].strip()
            next_state = symbol_state[1].strip()
            #print("NEXT STATE: " + next_state)
            transition.append(next_state)
            
            # add transition to nested dictionary
            #print("TRANSITION: " + str(transition))
            NFA_TRANSITIONS[transition[0]][transition[1]].append(transition[2])
            line = next(file_iterator)

def printNFADictionary():
    print("NFA TRANSITIONS:")
    for state in NFA_TRANSITIONS:
        print(state + ": " + str(NFA_TRANSITIONS[state]))

def printDFADictionary():
    print("DFA TRANSITIONS:")
    for state in DFA_TRANSITIONS:
        print(state + ": " + str(DFA_TRANSITIONS[state]))

    print()

def epsilonEnclosure(state):
    start_state = state
    # create a list containing the start state
    closure = [start_state]
    # get the epsilon transition states
    epsilon_states = NFA_TRANSITIONS[start_state]["EPS"]
    # add epsilon states to closure
    for state in epsilon_states:
        closure.append(state)
    # check if epsilon states have epsilon states
    for state in epsilon_states:
        epsilon_states = NFA_TRANSITIONS[state]["EPS"]
        for state in epsilon_states:
            if state not in closure:
                closure.append(state)
    #print("EPSILON CLOSURE OF " + str(start_state) + " : " + str(closure))
    return closure

def convertToDFA():
    # get epsilon enclosure of start state as the new start state of DFA
    start_state = epsilonEnclosure(START_STATE)
    DFA_START_STATE.append(start_state)

    # create a queue of that is a queue of lists of states
    queue = [start_state]
    #counter = 0
    while (queue != []):
        # counter += 1
        # if counter == 7:
        #     break
        #print()
        #print("THE STATES THAT WE HAVE VISITED: " + str(VISITED))
        #printDFADictionary()
        #print("QUEUE: " + str(queue))
        if str(queue[0]) not in DFA_TRANSITIONS:
            current_states = queue.pop(0)
            DFA_TRANSITIONS[str(current_states)] = {}
            for letter in ALPHABET:
                #print()
                #print("WE ARE CURRENTLY ON STATES: " + str(current_states) + " WITH LETTER: " + letter)
                visited_states = set()

                if letter == "EPS":
                    #print("SKIP")
                    continue

                for nfa_state in current_states:
                    #print()
                    #print("Substep of State: " + nfa_state + " With Letter: " + letter)
                    temp_list = NFA_TRANSITIONS[nfa_state][letter]
                    if (temp_list == []):
                        #visited_states.add("{EM}")
                        continue
                    #print("TEMP LIST: " + str(temp_list))
                    for state in temp_list:
                        enclosure = epsilonEnclosure(state)
                        for e in enclosure:
                            #print("e: " + e)
                            visited_states.update([e])  # Wrapping e in a list

                    # sort visited_states
                    #visited_states = sorted(visited_states)
                visited_states = sorted(visited_states)  # This is a list
                if (visited_states == []):
                    visited_states = ["{EM}"]
                #print("VISITED STATES: " + str(visited_states))

                DFA_TRANSITIONS[str(current_states)][letter] = visited_states
                VISITED.update([str(current_states)])
                # print out format in {current_states}letter =  {visited_states}
                #print()
                #print("FINAL RESULT: ")
                #print(str(current_states) + letter + " = " + str(visited_states))
                # if DFA doesn't have visited_states as a key, add it to the queue
                if str(visited_states) not in VISITED:
                    if (visited_states != ["{EM}"]):
                        queue.append(visited_states)

                # check if queue has multiples, and if so, remove
                for i in range(len(queue)):
                    for j in range(i + 1, len(queue)):
                        if queue[i] == queue[j]:
                            queue.pop(j)
                            break

                # print out the queue
                #print("QUEUE: " + str(queue))

def findDFAAcceptStates():
    for state in DFA_TRANSITIONS:
        for accept_state in ACCEPT_STATES:
            if accept_state in state:
                DFA_ACCEPT_STATES.append(state)
                break
                        
def cleanData(string):
    clean_data = string.translate(str.maketrans('', '', "[],'{}"))
    # Split the string into elements and ensure each element is separated by a comma
    elements = clean_data.split()
    states = ', '.join(element for element in elements if element)
    # Format to the desired output
    return "{" + states + "}"

# Line 1: A list of states, Q, separated by tabs.
# Line 2: A list of the symbols in Σ, separated by tabs. The Empty string will not be explicitly included. 
# You can assume that the state names do not also appear in the alphabet.
# Line 3: The start state, q0 ∈ Q.
# Line 4: The set of valid accept states, F , separated by tabs.
# Line 5: The token BEGIN to denote the start of the transition function
# Line 6 to line before last: The transition function. Each line will be of the form s, x = sf
# This is translated to mean that reading
# symbol x in state s causes a transition to state sf
# Last Line: The token END to denote the end of the transition function.
                        
def writeToOutput(output_file):
    file = open(output_file, "w")

    # write states
    file.write("{EM}\t")
    for state in DFA_TRANSITIONS:
        #file.write(str(state).replace("{", "").replace("}", "").replace("'", "").replace("[", "{").replace("]", "}") + "\t")
        file.write(cleanData(str(state)) + "\t")
    file.write("\n")

    # write alphabet
    for symbol in ALPHABET:
        if symbol == "EPS":
            continue
        file.write(str(symbol) + "\t")
    file.write("\n")

    # write start state
    file.write(cleanData(str(DFA_START_STATE)) + "\n")

    # write accept states
    findDFAAcceptStates()
    for state in DFA_ACCEPT_STATES:
        file.write(cleanData(str(state)) + "\t")
    file.write("\n")

    file.write("BEGIN\n")
    # write transition functions by iterating through the DFA dictionary
    # Line 6 to line before last: The transition function. Each line will be of the form s, x = sf
    # This is translated to mean that reading
    # symbol x in state s causes a transition to state sf
    for state in DFA_TRANSITIONS:
        for symbol in DFA_TRANSITIONS[state]:
            file.write(cleanData(str(state)) + ", " + str(symbol) + " = " + cleanData(str(DFA_TRANSITIONS[state][symbol])) + "\n")
    # append {EM} with each symbol
    for symbol in ALPHABET:
        if symbol == "EPS":
            continue
        file.write("{EM}, " + str(symbol) + " = {EM}\n")
    file.write("END\n")
            


# command line argument 1 is the input file
# command line argument 2 is the output file
input_file = sys.argv[1]
output_file = sys.argv[2]

print("INPUT FILE: " + input_file)
print("OUTPUT FILE: " + output_file)

openFile(input_file)

#printInfo()
print()

printNFADictionary()

print()

convertToDFA()

printDFADictionary()

writeToOutput(output_file)