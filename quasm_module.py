import numpy as np
import qutip
from qutip import qip
from random import random
from bisect import bisect
import matplotlib.pyplot as plt
   
class qasm:
    def __init__(self,filename):  # The function used when the object is created.
        self.filename=filename
        self.qasm_file=[]
        self.qasm_instructions=[]
        self.qasm_instruction_line=[]
        self.last_qubit_line_index=int(0)
        self.number_of_qubits=1
        self.probability_vector=([0,1])
        self.state=np.array([0,1])
        self.gate_dict=self.operator_dict_default()
        self.measurement_hist
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
            if line[0]=='#' or line.split()==[]:
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
        self.qasm_instruction_line=[operator, qubits]
        
    def read_qubits_string(self,qubits):
        """
        In: list with qubit names
        ----
        Out: returns a list with qubit numbers starting at 0.
        """
        qubit_numbers=[]
        for i in range(len(qubits)):
            name=qubits[i]
            number=name[1::]
            qubit_numbers.append(int(number))
        self.qubit_numbers=qubit_numbers
        #return qubit_numbers
        
    def run_algorithm(self):
        """
        load the file, filter the instructions
        run the instructions line by line
        Out: final qubit state.
        """
        self.load_qasm_file()
        self.get_filtered_qasm()
        self.get_number_of_qubits()
        self.create_qubits()
        for line_index,line in enumerate(self.qasm_instructions[self.last_qubit_line_index::]):
            self.read_instruction_line(line_index+self.last_qubit_line_index)
            self.run_instruction_line()
        return(self.state)
            
    def run_instruction_line(self):
        instruction=self.qasm_instruction_line
        self.read_qubits_string(instruction[1])
        qubits=self.qubit_numbers
        gate_matrix=self.gate_dict.get(instruction[0])
        matrix=[]
        if gate_matrix==None:
            if instruction[0]=='cnot':
                control=qubits[0]
                target=qubits[1]
                matrix=self.create_cnot_gate(control,target)
                self.act_gate_on_state(matrix)
            elif instruction[0]=='measure':
                self.do_measurement()
            else:
                raise NameError ('Gate ' + instruction[0] + ' not defined')
        else:
            for qubit_number in range(len(qubits)):
                matrix=self.create_single_qubit_gate(instruction[0],qubit_number)
                print(matrix)
                self.act_gate_on_state(matrix)

    def get_number_of_qubits(self):
        '''
        In: filtered quasm instructions
        ---
        Out: integer with number of needed qubits
        '''
        num_qubits=0
        last_qubit_line_index=0
        for line_index, line in enumerate(self.qasm_instructions):
            if 'qubit' in line:
                num_qubits+=1
                last_qubit_line_index=line_index
        self.number_of_qubits=num_qubits
        self.last_qubit_line_index=last_qubit_line_index+1
    
    def create_qubits(self):
        self.state=np.zeros(2**self.number_of_qubits) # construct the state vector
        self.state[0]=1 #start in the ground state

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

    def create_cnot_gate(self,control,target):
        '''
        In: control qubit, starting with 0, target qubit, starting with 0, number of qubits
        ---
        Out: Matrix for the gate
        '''
        return qip.cnot(N=self.number_of_qubits, control=control, target=target).full()
    
    def do_measurement(self,number_of_measurements=10000):
        self.get_probability_vector()
        result=0
        hist=np.array(len(self.probability_vector))
        for i in range(number_of_measurements):
            result=int(self.measure())
            #add a count to the histogram
            hist(result)+=1
        hist=hist/number_of_measurements
        self.measurement_hist=hist
        self.plot_measurement_hist()
        
    def plot_measurement_hist(self):
        plt.hist(self.measurement_hist)
        plt.xlabel(self.measurent_hist_xlabel())
        plt.show()
        
    def measurement_hist_xlabel(self)
        #just take binary of the index
        label=[]
        for i in range(len(self.probability_vector)):
            label.append("{0:b}".format(i)
        return label
    
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
        # add identity
        operator_dict.update({'nop':np.array([[1,0],[0,1]])})
        # add Pauli X
        operator_dict.update({'x':np.array([[0,1],[1,0]])})
        # add Pauli Y
        operator_dict.update({'y':np.array([[0,-1j],[1j,0]])})
        # add Pauli Z
        operator_dict.update({'z':np.array([[1,0],[0,-1]])})
        return operator_dict

    def get_probability_vector(self):
        self.probability_vector=self.state**2
        
    
    def measure(self):
        weights=self.probability_vector
        values=range(self.number_of_qubits)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        x = random() * total
        i = bisect(cum_weights, x)
        return values[i]

