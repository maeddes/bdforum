# pip install flask qiskit qiskit_ibm_runtime

from flask import Flask
import random

from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import QuantumRegister, QuantumCircuit 
from qiskit.circuit import ClassicalRegister

app = Flask(__name__)

data = [] # List of binary values
int_data = [] # List of integer values       
size = 7 # Number of qubits in the quantum register
length = 100 # Number of shots

# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_API_TOKEN")
backend = service.backend("ibmq_qasm_simulator")
# backend = service.backend("ibm_brisbane")
# backend = service.backend("ibm_kyoto")
# backend = service.backend("ibm_sherbrooke")
# backend = service.backend("ibm_osaka")

def generate_quantum_array():
    qr = QuantumRegister(size) # Create a quantum register of size n
    cr = ClassicalRegister(size)
    circuit = QuantumCircuit(qr, cr)
    circuit.h(qr) # Apply Hadamard gate to qubits
    circuit.measure(qr, cr)

    job = backend.run(circuit, shots=length, memory=True)
    result = job.result()
    print(result)

    global data 
    data = job.result().get_memory()
    print(data)

    counts = result.get_counts()

    global int_data 
    int_data = []
    for bitstring in data:
        int_data.append( int(bitstring,2) )
    print(int_data)

def get_random_number():
    rand_num = random.randint(1, 128)
    return str(rand_num)

def generate_python_array():
    global int_data
    int_data = []
    for i in range(length):
        int_data.append(get_random_number())
    print(int_data)

generate_python_array()

@app.route('/binary', methods=['GET'])
def get_binary_array():
    return str(data)

@app.route('/decimal', methods=['GET'])
def get_decimal_array():
    return str(int_data)

@app.route('/pygenerate', methods=['GET'])
def trigger_python_generate():
    generate_python_array()
    return data

@app.route('/generate', methods=['GET'])
def trigger_generate():
    generate_quantum_array()
    return data

@app.route('/', methods=['GET'])
def get_quantum_random_number():
    num = int(random.choice(int_data))
    if num > 100:
        num = round(num / 2) # make it fitting for a year

    year = num + 1930 # make it a year
    print("Year: ",year)
    return str(year)

if __name__ == '__main__':
    app.run(debug=True)