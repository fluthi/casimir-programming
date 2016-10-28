import numpy as np
import qutip
from qutip import qip

   
class qasm:
    def __init__(self,filename):  # The function used when the object is created.
        self.filename=filename
        
        self.number_of_qubits=1
        self.state=np.array([0,1])
        self.gate_dict=operator_dict_default()
        pass
    
    def load_qasm_file(self):
    '''
    Reads in a .qasm file. filename a string with the filename, eg. 'test1.qasm'
    ---
    Return: List of strings with all characters in the file
    '''
    quasm_file=[]
    f=open(self.filename,'r')
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

    def number_of_qubits(self):
        '''
        In: filtered quasm instructions
        ---
        Out: integer with number of needed qubits
        '''
        num_qubits=0
        for line in self.qasm_instructions:
            if 'qubit' in line:
                num_qubits+=1
        self.number_of_qubits=num_qubits
    
    def create_qubits(self):
        self.state=np.zeros(2**self.number_of_qubits) # construct the state vector
        self.state[0]=1 #start in the ground state
        
        
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

    def read_qubits_string(qubits):
        """
        In: list with qubit names
        ----
        Out: returns a list with qubit numbers
        """
        qubit_numbers=[]
        for i in range(len(qubits)-1):
            name=qubits[i]
            number=name[1:len(name)-1]
            qubit_numbers[i]=number
        return qubit_numbers

    def create_single_qubit_gate(self,gate,qubit_number):
        '''
        In: which gate is to be applied, qubit_number: which qubit is acted on (first qubit is 0), number_of_qubits: total number of qubits
        ---
        Out: Process matrix with dimension 2**number_of_qubits x 2**number_of_qubits
        '''
        single_qubit_gate=self.gate_dict[gate]
        if qubit_number==0:
            matrix=single_qubit_gate
        else:
            matrix=self.gate_dict['i']
        for tt in range(1,self.number_of_qubits):
            if tt==qubit_number:
                matrix=np.kron(matrix,single_qubit_gate)
            else:
                matrix=np.kron(matrix,self.gate_dict['i'])
        return matrix

    def cnot_gate(self,control,target):
        '''
        In: control qubit, starting with 0, target qubit, starting with 0, number of qubits
        ---
        Out: Matrix for the gate
        '''
        return qip.cnot(N=self.number_of_qubits, control=control, target=target)
    
    def act_gate_on_state(self,matrix):
        '''
        In: Matrix that should be acted on the qubits
        ---
        Out: -    updates the state of the qubit
        '''
        old_state=self.state
        new_state=np.dot(matrix,old_state)
        self.state=new_state

    def operator_dict_default(self):
        """
        In: none
        Creates a dictionary with default operations
        Out: none
        """
        operator_dict={}
        # add hadamard
        operator_dict.update({'h':1/np.sqrt(2)*np.array([[1,1],[1,-1]])})
        # add identity
        operator_dict.update({'i':np.array([[1,0],[0,1]])})
        # add Pauli X
        operator_dict.update({'x':np.array([[0,1],[1,0]])})
        # add Pauli Y
        operator_dict.update({'y':np.array([[0,-1j],[1j,0]])})
        # add Pauli Z
        operator_dict.update({'z':np.array([[1,0],[0,-1]])})
        return operator_dict

