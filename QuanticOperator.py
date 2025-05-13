from QuanticState import QuanticState

class QuanticOperator:

    def __init__(self, name = str, matrix = list):
        self.name = name
        self.matrix = matrix
    
    def __str__(self):
        return f"Operador cuántico: (nombre={self.name}, matriz={self.matrix})"
    
    def validate_matrix(self):
        if not all(len(row) == len(self.matrix) for row in self.matrix):
            raise ValueError("La matriz debe tener el mismo número de filas que de columnas.")
        if not all(isinstance(x, (complex, float)) for row in self.matrix for x in row):
            raise ValueError("La matriz debe contener números complejos o decimales.")
        
    def apply_operator(self, state: QuanticState):
        if len(self.matrix) != len(state.vector):
            raise ValueError("La matriz del operador no coincide con la longitud del vector del estado.")
        
        new_vector = []
        for i in range(len(self.matrix)):
            new_value = sum(self.matrix[i][j] * state.vector[j] for j in range(len(state.vector)))
            new_vector.append(new_value)
        
        return QuanticState(unique_id=state.unique_id, vector=new_vector, bases=state.bases)