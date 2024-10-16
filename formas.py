# formas

import numpy as np

def criar_poligono_regular(num_vertices, radius):
    """
    Cria os vértices de um polígono regular inscrito em um círculo.

    :param num_vertices: Número de vértices do polígono
    :param radius: Raio do círculo em que o polígono está inscrito
    :return: Array de vértices do polígono
    """
    angles = np.linspace(0, 2 * np.pi, num_vertices, endpoint=False)  # Ângulos dos vértices
    vertices = np.array([
        radius * np.cos(angles),  # Coordenadas x
        radius * np.sin(angles)   # Coordenadas y
    ]).T  # Transpor para ter um array Nx2

    return vertices

def criar_estrela_vertices(radius_outer, radius_inner, num_points):
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False) + np.pi / 2
    outer_vertices = np.array([radius_outer * np.cos(angles), radius_outer * np.sin(angles)]).T
    inner_vertices = np.array([radius_inner * np.cos(angles + np.pi / num_points), 
                               radius_inner * np.sin(angles + np.pi / num_points)]).T

    # Intercalando os vértices externos e internos
    vertices = np.empty((num_points * 2, 2))
    vertices[::2] = outer_vertices
    vertices[1::2] = inner_vertices
    
    return vertices

def criar_linha(start_point, end_point, num_points=100):
    """
    Cria os pontos de uma reta entre dois pontos.

    :param start_point: Tupla ou array com as coordenadas do ponto inicial (x1, y1)
    :param end_point: Tupla ou array com as coordenadas do ponto final (x2, y2)
    :param num_points: Número de pontos a serem gerados ao longo da reta
    :return: Array de pontos da reta
    """
    start_point = np.array(start_point)
    end_point = np.array(end_point)

    # Cria um array de parâmetros t que varia de 0 a 1
    t = np.linspace(0, 1, num_points)

    # Calcula os pontos da reta usando a forma paramétrica
    line_points = (1 - t)[:, np.newaxis] * start_point + t[:, np.newaxis] * end_point

    return line_points