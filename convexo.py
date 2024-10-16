
import numpy as np

def is_convex_polygon(vertices):
    """
    Verifica se um polígono definido pelos vértices é convexo.

    :param vertices: Array 2D com os vértices do polígono (Nx2)
    :return: True se o polígono é convexo, False caso contrário
    """
    num_vertices = len(vertices)
    if num_vertices < 3:
        return False  # Um polígono precisa ter pelo menos 3 vértices

    # Variável para armazenar o sinal do primeiro produto vetorial
    first_sign = 0

    for i in range(num_vertices):
        # Vértices atuais e os próximos (usando módulo para fechar o polígono)
        p1 = vertices[i]
        p2 = vertices[(i + 1) % num_vertices]
        p3 = vertices[(i + 2) % num_vertices]

        # Cálculo do produto vetorial
        vector1 = p2 - p1
        vector2 = p3 - p2
        cross_product = np.cross(vector1, vector2)

        # Determinar o sinal do produto vetorial
        if cross_product != 0:  # Ignorar casos em que os vetores são colineares
            current_sign = np.sign(cross_product)
            if first_sign == 0:
                first_sign = current_sign
            elif first_sign != current_sign:
                return False  # Sinal mudou, polígono é côncavo

    return True  # Se todos os sinais foram consistentes, o polígono é convexo