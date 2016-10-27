import numpy as np

def load_qasm_file(filename):
    '''
    Reads in a .qasm file. filename a string with the filename, eg. 'test1.qasm'
    ---
    Return: List of strings with all characters in the file
    '''
    quasm_file=[]
    f=open(filename,'r')
    for line in f:
        quasm_file.append(line)
    return quasm_file

def get_filtered_qasm(list_of_qasm_strings):
    '''
    In: List of strings with comments
    ---
    Return: list of strings without comments
    '''
    quasm_instrunctions=[]
    m=0
    for tt, line in enumerate(list_of_qasm_strings):
        if line[0]=='#':
            m+=1
            pass
        else:
            quasm_instrunctions.append('')
            for char in line:
                if not char=='#':
                    quasm_instrunctions[tt-m]+=char
                else:
                    break
    return quasm_instrunctions

def number_of_qubits(quasm_instrunctions):
    '''
    In: filtered quasm instructions
    ---
    Out: integer with number of needed qubits
    '''
    num_qubits=0
    for line in quasm_instrunctions:
        if 'qubit' in line:
            num_qubits+=1
    return num_qubits

def delete_instruction(instructions,number_to_be_deleted=1):
    """
    In: list of instructions and number of instructions to remove
    ---
    Out: list with removed instructions (from top)
    """
    return instructions[number_to_be_deleted:len(instructions)-1]

def read_instruction_line(instructions):
    """
    In: instructions 
    read the first line
    recognize the operation and qubit
    ---
    Out: list with operation as first entry and list of qubit(s) as second entry
    """
    if instructions!=[]:
        instruction_line=str(instructions[0])
        instruction = instruction_line.split()
        operator = instruction[0]
        qubits = instruction[1].split(",")   
    return [operator, [qubits]]
        
def single_qubit_gate(gate,qubit_number,number_of_qubits):
    '''
    In: which gate is to be applied, qubit_number: which qubit is acted on (first qubit is 0), number_of_qubits: total number of qubits
    ---
    Out: Process matrix with dimension 2**number_of_qubits x 2**number_of_qubits
    '''
    gate_dict=operator_dict_default()
    single_qubit_gate=gate_dict['gate']
    if qubit_number==0:
        matrix=single_qubit_gate
    else:
        matrix=gate_dict['i']
    for tt in range(1,len(number_of_qubits)):
        if tt==qubit_number:
            matrix=np.outer(matrix,single_qubit_gate)
        else:
            matrix=np.outer(matrix,gate_dict['i'])
    return matrix


def operator_dict_default():
    """
    In: none
    Creates a dictionary with default operations
    Out: none
    """
    operator_dict={}
    # add hadamard
    operator_dict.update({'h',1/np.sqrt(2)*np.array([[1,1],[1,-1]])})
    # add identity
    operator_dict.update({'i',np.array([[1,0],[0,1]]})
    # add Pauli X
    operator_dict.update({'x',np.array([[0,1],[1,0]]})
    # add Pauli Y
    operator_dict.update({'y',np.array([[0,-1j],[1j,0]]})
    # add Pauli Z
    operator_dict.update({'z',np.array([[1,0],[0,-1]]})
    return operator_dict{}
    
