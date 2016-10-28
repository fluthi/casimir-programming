import numpy as np
import qutip
from qutip import qip

   
class qasm:
    def __init__(self,filename):  # The function used when the object is created.
        self.filename=filename
        self.qasm_file=[]
        self.qasm_instructions=[]
        self.qasm_instruction_line=[]
        pass
    
    def load_qasm_file(self):
        '''
        Reads in a .qasm file. filename a string with the filename, eg. 'test1.qasm'
        ---
        Return: List of strings with all characters in the file
        '''
        qasm_file=[]
        f=open(self.filename,'r')
        for line in f:
            qasm_file.append(line)
        self.qasm_file=qasm_file

    def get_filtered_qasm(self):
        '''
        In: List of strings with comments
        ---
        Return: list of strings without comments
        '''
        qasm_instructions=[]
        m=0
        for tt, line in enumerate(self.qasm_file):
            if line[0]=='#':
                m+=1
                pass
            else:
                qasm_instructions.append('')
                for char in line:
                    if not char=='#':
                        qasm_instructions[tt-m]+=char
                    else:
                        break
        self.qasm_instructions=qasm_instructions
        
    def read_instruction_line(self,line_index):
        """
        In: instructions 
        read the first line
        recognize the operation and qubit
        ---
        Out: list with operation as first entry and list of qubit(s) as second entry
        """
        instructions=self.qasm_instructions
        if instructions!=[]:
            instruction_line=str(instructions[line_index])
            instruction = instruction_line.split()
            operator = instruction[0]
            qubits = instruction[1].split(",")   
        self.qasm_instruction_line=[operator, [qubits]]
        
    def run_algorithm(self):
        """
        load the file, filter the instructions
        run the instructions line by line
        Out: final qubit state.
        """
        load_qasm_file()
        get_filtered_qasm()
        for line_index in self.qasm_instructions:
            read_instruction_line(line_index)
            run_instruction_line(self.qasm_instruction_line)
        return(self.state)
            
    def run_instruction_line(self,instruction)
                #redirect to single qubit or multi qubit
                #call act_gate_on_state()

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
    
    def create_qubits(number_qubits):
        self.number_of_qubits=number_of_qubits
        self.state=np.zeros(2**number_of_qubits) # construct the state vector
        self.state[0]=1 #start in the ground state
        
        

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

    def single_qubit_gate(gate,qubit_number,number_of_qubits):
        '''
        In: which gate is to be applied, qubit_number: which qubit is acted on (first qubit is 0), number_of_qubits: total number of qubits
        ---
        Out: Process matrix with dimension 2**number_of_qubits x 2**number_of_qubits
        '''
        gate_dict=operator_dict_default()
        single_qubit_gate=gate_dict[gate]
        if qubit_number==0:
            matrix=single_qubit_gate
        else:
            matrix=gate_dict['i']
        for tt in range(1,number_of_qubits):
            if tt==qubit_number:
                matrix=np.kron(matrix,single_qubit_gate)
            else:
                matrix=np.kron(matrix,gate_dict['i'])
        return matrix

    def cnot_gate(control,target,number_of_qubits):
        '''
        In: control qubit, starting with 0, target qubit, starting with 0, number of qubits
        ---
        Out: Matrix for the gate
        '''
        return qip.cnot(N=number_of_qubits, control=control, target=target)


    def operator_dict_default():
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

