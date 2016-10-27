
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
    alphabet='abcdefghijklmnopqrstuvwxyz'
    m=0
    for tt, line in enumerate(list_of_qasm_strings):
        if not line[0] in alphabet:
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