from QuanticState import QuanticState
from QuanticOperator import QuanticOperator
import csv


class StatesRepository:
    def __init__(self):
        self.states = {}

    def list_states(self):
        return list(self.states.values())
    
    def add_state(self):
        unique_id = input("Ingrese el ID único del estado cuántico: ")
        vector = input("Ingrese el vector del estado cuántico (separado por comas): ")
        bases = input("Ingrese la base del estado cuántico (separado por comas): ")

        # Convertir el vector y las bases a listas
        vector = [complex(x.strip()) for x in vector.split(",")]
        bases = [x.strip() for x in bases.split(",")]

        # Crear una instancia de QuanticState
        state = QuanticState(unique_id=unique_id, vector=vector, bases=bases)
        
        # Validar el estado cuántico
        state.validate_vector()
        
        # Agregar el estado al repositorio
        self.states[unique_id] = state
        return state

    def get_state(self, unique_id):
        if unique_id in self.states:
            return self.states[unique_id]
        else:
            raise ValueError(f"El estado cuántico con ID {unique_id} no existe.")
        
    def remove_state(self, unique_id):
        if unique_id in self.states:
            del self.states[unique_id]
        else:
            raise ValueError(f"El estado cuántico con ID {unique_id} no existe.")
        
    def applyOperator(self, unique_id: str, operator: QuanticOperator, new_id: str = None):
        # Crear un nuevo estado cuántico llamando a add_state
        new_state = self.add_state()
        
        # Verificar si el estado cuántico original existe
        if not self.get_state(unique_id):
            raise Exception(f"El estado cuántico con ID {unique_id} no existe.")
        
        # Aplicar el operador cuántico al estado original
        result_state = operator.apply_operator(self.get_state(unique_id))
        
        # Actualizar el vector del nuevo estado con el resultado
        new_state.vector = result_state.vector
        
        # Asignar un nuevo ID si se proporciona, o generar uno basado en el operador
        if new_id is not None:
            new_state.unique_id = new_id
        else:
            new_state.unique_id = "{}_{}".format(unique_id, operator.name)
        
        # Agregar o actualizar el estado en el repositorio
        self.states[new_state.unique_id] = new_state

        return new_state
    
    def measure_state(self, unique_id: str):
        # Verificar si el estado cuántico existe
        try:
            state = self.get_state(unique_id)
        except ValueError as e:
            raise ValueError(f"El estado cuántico con ID {unique_id} no existe.") from e
        
        # Medir el estado cuántico y obtener la distribución de probabilidades
        measurement_results = state.measure()
        
        # Formatear el resultado de la medición
        formatted_results = f"Medición del estado {unique_id} en base {state.bases}:\n"
        for outcome, probability in measurement_results.items():
            formatted_results += f"- Resultado {outcome}: {probability * 100:.2f}%\n"
        
        return formatted_results
    
    def save_states(self, file):
        with open('States.csv', mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
        for state in self.states.values():
            writer.writerow([state.unique_id, state.vector, state.bases])

    def load_states(self, file):
        with open(file, newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for unique_id, basis, vector in reader:
                vector = eval(vector)
                self.add_state(unique_id, basis, vector)