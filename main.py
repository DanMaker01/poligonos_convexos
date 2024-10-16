import numpy as np
import pygame
import formas

class Poligono:
    def __init__(self, vertices, cor):
        self.vertices = np.array(vertices, dtype=np.float64)
        self.cor = cor

    def transladar(self, dx, dy):
        """Move o polígono pela tela."""
        self.vertices[:, 0] += dx
        self.vertices[:, 1] += dy

    def escalar(self, sx, sy):
        """Escala o polígono."""
        self.vertices[:, 0] *= sx
        self.vertices[:, 1] *= sy
    
    def rotacionar(self, theta):
        """Rotaciona o polígono."""
        theta = np.radians(theta)
        cos = np.cos(theta)
        sin = np.sin(theta)
        R = np.array([[cos, -sin], [sin, cos]])
        self.vertices = np.dot(self.vertices, R)

    def centroide(self):
        """Retorna o centroide do polígono."""
        return np.mean(self.vertices, axis=0)

    def desenhar(self, screen):
        """Desenha o polígono na tela, convertendo os vértices para inteiros e desenha pontos nos vértices."""
        vertices_int = np.round(self.vertices).astype(int)  # Arredondar apenas para o Pygame
        pygame.draw.polygon(screen, self.cor, vertices_int, 0)

        # Desenhar um ponto preto em cada vértice
        for vertice in vertices_int:
            pygame.draw.circle(screen, (64, 64, 64), vertice, 5)  # Desenha um círculo preto com raio 5 em cada vértice

    def ponto_esta_contido(self, ponto):
        """Verifica se um ponto está contido no polígono usando o método do raio cruzado."""
        inside = False
        num_vertices = len(self.vertices)

        for i in range(num_vertices):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % num_vertices]

            if ((p1[1] > ponto[1]) != (p2[1] > ponto[1])):
                slope = (p2[0] - p1[0]) / (p2[1] - p1[1])
                x_intersection = p1[0] + (ponto[1] - p1[1]) * slope

                if ponto[0] < x_intersection:
                    inside = not inside

        return inside

    def aresta(self, i):
        """Retorna a i-ésima aresta do polígono."""
        return (self.vertices[i], self.vertices[(i + 1) % len(self.vertices)])

class InterseccaoPoligonos:
    @staticmethod
    def intersecao_de_arestas(aresta1, aresta2, tolerancia=1e-9):
        """Retorna o ponto de interseção entre duas arestas se houver, com tolerância."""
        p1, p2 = aresta1
        q1, q2 = aresta2

        A1 = p2[1] - p1[1]
        B1 = p1[0] - p2[0]
        C1 = A1 * p1[0] + B1 * p1[1]

        A2 = q2[1] - q1[1]
        B2 = q1[0] - q2[0]
        C2 = A2 * q1[0] + B2 * q1[1]

        det = A1 * B2 - A2 * B1

        if abs(det) < tolerancia:  # As arestas são paralelas
            return None

        x = (B2 * C1 - B1 * C2) / det
        y = (A1 * C2 - A2 * C1) / det
        intersection_point = np.array([x, y])

        # Verifica se o ponto de interseção está dentro dos segmentos
        if (min(p1[0], p2[0]) - tolerancia <= x <= max(p1[0], p2[0]) + tolerancia and
            min(p1[1], p2[1]) - tolerancia <= y <= max(p1[1], p2[1]) + tolerancia and
            min(q1[0], q2[0]) - tolerancia <= x <= max(q1[0], q2[0]) + tolerancia and
            min(q1[1], q2[1]) - tolerancia <= y <= max(q1[1], q2[1]) + tolerancia):
            return intersection_point

        return None  # Não há interseção

    @staticmethod
    def intersecao_de_poligonos_convexos(poligono1, poligono2, tolerancia=1e-9, cor=(255, 0, 0)):
        """Calcula a interseção entre dois polígonos e retorna um novo polígono resultante."""
        intersecoes = []
        num_vertices_p1 = len(poligono1.vertices)
        num_vertices_p2 = len(poligono2.vertices)

        # Listar interseções de arestas dos dois polígonos
        for i in range(num_vertices_p1):
            aresta1 = poligono1.aresta(i)
            
            for j in range(num_vertices_p2):
                aresta2 = poligono2.aresta(j)
                interseccao = InterseccaoPoligonos.intersecao_de_arestas(aresta1, aresta2, tolerancia)
                if interseccao is not None:
                    intersecoes.append(interseccao)

        # Adicionar vértices de polígono 1 que estão contidos no polígono 2
        for vertice in poligono1.vertices:
            if poligono2.ponto_esta_contido(vertice):
                intersecoes.append(vertice)

        # Adicionar vértices de polígono 2 que estão contidos no polígono 1
        for vertice in poligono2.vertices:
            if poligono1.ponto_esta_contido(vertice):
                intersecoes.append(vertice)

        # Remove duplicatas e converte para um novo polígono
        intersecoes = np.unique(np.array(intersecoes), axis=0)

        if len(intersecoes) < 3:
            return None  # Sem interseção válida

        # Ordena os pontos em sentido anti-horário
        centro = np.mean(intersecoes, axis=0)
        angulos = np.arctan2(intersecoes[:, 1] - centro[1], intersecoes[:, 0] - centro[0])
        pontos_ordenados = intersecoes[np.argsort(angulos)]

        return Poligono(pontos_ordenados, cor)  # Retorna o polígono resultante da interseção

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Interseção de Polígonos')

# Definindo os polígonos
poligono1 = Poligono([[100, 100], [300, 100], [300, 300],[200,400], [100, 300]], (0, 255, 0))  # Polígono 1 (Verde)
poligono1.transladar(150,150)

poligono3 = Poligono(formas.criar_poligono_regular(6,150), (0, 128, 0))  # Polígono 1 (Verde
poligono3.transladar(150,150)

poligono4 = Poligono(formas.criar_poligono_regular(36,100), (0, 128, 128))  # Polígono 1 (Verde
poligono4.transladar(500,100)

poligono2 = Poligono([[200, 200], [400, 200], [400, 400], [200, 400]], (0, 0, 128))  # Polígono 2 (Azul)

# Variável para controle da velocidade do polígono
velocidade = 1/3

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Captura das teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        poligono2.transladar(-velocidade, 0)  # Move para a esquerda
    if keys[pygame.K_RIGHT]:
        poligono2.transladar(velocidade, 0)  # Move para a direita
    if keys[pygame.K_UP]:
        poligono2.transladar(0, -velocidade)  # Move para cima
    if keys[pygame.K_DOWN]:
        poligono2.transladar(0, velocidade)  # Move para baixo
    if keys[pygame.K_a]:
        centroide = poligono2.centroide()
        poligono2.transladar(-centroide[0], -centroide[1])
        poligono2.escalar(0.999, 0.999)  # Aumenta o tamanho
        poligono2.transladar(centroide[0], centroide[1])
    if keys[pygame.K_s]:
        centroide = poligono2.centroide()
        poligono2.transladar(-centroide[0], -centroide[1])
        poligono2.escalar(1.001, 1.001)  # Aumenta o tamanho
        poligono2.transladar(centroide[0], centroide[1])
    if keys[pygame.K_q]:
        centroide = poligono2.centroide()
        poligono2.transladar(-centroide[0], -centroide[1])
        poligono2.rotacionar(np.radians(5))  # Rotaciona 5 graus
        poligono2.transladar(centroide[0], centroide[1])
    if keys[pygame.K_w]:
        centroide = poligono2.centroide()
        poligono2.transladar(-centroide[0], -centroide[1])
        poligono2.rotacionar(-np.radians(5))  # Rotaciona -5 graus
        poligono2.transladar(centroide[0], centroide[1])
    # Limpar a tela

    screen.fill((255, 255, 255))

    # Desenhar os polígonos
    poligono1.desenhar(screen)
    poligono2.desenhar(screen)
    poligono3.desenhar(screen)
    poligono4.desenhar(screen)

    # Calcular e desenhar a interseção
    poligono_interseccao = InterseccaoPoligonos.intersecao_de_poligonos_convexos(poligono1, poligono2, cor=(255,0,0))
    if poligono_interseccao is not None:
        poligono_interseccao.desenhar(screen)
    
    poligono_interseccao2 = InterseccaoPoligonos.intersecao_de_poligonos_convexos(poligono3, poligono2, cor=(255,0,0))
    if poligono_interseccao2 is not None:
        poligono_interseccao2.desenhar(screen)
    
    poligono_interseccao3 = InterseccaoPoligonos.intersecao_de_poligonos_convexos(poligono4, poligono2, cor=(255,0,0))
    if poligono_interseccao3 is not None:
        poligono_interseccao3.desenhar(screen)
    # Atualizar a tela
    pygame.display.flip()

pygame.quit()
