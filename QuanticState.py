class QuanticState:
    def __init__(self, unique_id = str, vector = list, basis = list):
        self.unique_id = unique_id
        self.vector = vector
        self.basis = basis

    def __str__(self):
        return f"Estado cuántico: (id={self.unique_id}, vector={self.vector}, base={self.basis})"
   
    def validate_vector(self):
        
        if not isinstance(self.vector, list):
            raise ValueError("El vector debe ser una lista.")
        if not all(isinstance(x, complex) for x in self.vector):
            raise ValueError("El vector debe contener números complejos.")
        if len(self.vector) == 0 or (len(self.vector) & (len(self.vector) - 1)) != 0:
            raise ValueError("La longitud del vector debe ser una potencia de 2.")

    def measure(self):
        probabilities = {basis: abs(amplitude)**2 for basis, amplitude in zip(self.basis, self.vector)}
        total_probability = sum(probabilities.values())
        
        # Normalize probabilities if the total is not exactly 1
        if not (0.999 <= total_probability <= 1.001):  # Allowing for small rounding errors
            probabilities = {basis: prob / total_probability for basis, prob in probabilities.items()}
        
        return probabilities