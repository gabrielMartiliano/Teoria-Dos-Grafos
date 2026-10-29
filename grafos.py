import sys
import time
import random
import tracemalloc

class GrafoMatriz:
    def __init__(self, vertices):
        self.V = vertices
        self.matriz = [[0] * vertices for _ in range(vertices)]

    def adicionar_aresta(self, u, v):
        self.matriz[u][v] = 1
        self.matriz[v][u] = 1 # Para grafo não direcionado

    def grau_vertice(self, v):
        return sum(self.matriz[v])


class GrafoLista:
    def __init__(self, vertices):
        self.V = vertices
        self.lista = {i: [] for i in range(vertices)}

    def adicionar_aresta(self, u, v):
        if v not in self.lista[u]:
            self.lista[u].append(v)
        if u not in self.lista[v]:
            self.lista[v].append(u)

    def grau_vertice(self, v):
        return len(self.lista[v])


def gerar_arestas(v, densidade):
    max_arestas = (v * (v - 1)) // 2
    num_arestas = int(densidade * max_arestas)
    arestas = set()
    while len(arestas) < num_arestas:
        u = random.randint(0, v - 1)
        w = random.randint(0, v - 1)
        if u != w:
            arestas.add(tuple(sorted((u, w))))
    return list(arestas)


def benchmark():
    tamanhos = [100, 500, 1000]
    densidades = [0.1, 0.5, 0.9]  # Esparso vs Denso

    print(f"{'V':<6} | {'Densidade':<10} | {'Repr.':<15} | {'Memória (KB)':<15} | {'Tempo Arestas (s)':<18} | {'Tempo Grau (s)'}")
    print("-" * 85)

    for v in tamanhos:
        for d in densidades:
            arestas = gerar_arestas(v, d)

            # Teste Matriz de Adjacência
            tracemalloc.start()
            t0 = time.perf_counter()
            gm = GrafoMatriz(v)
            for u, w in arestas:
                gm.adicionar_aresta(u, w)
            t1 = time.perf_counter()
            
            for i in range(v):
                gm.grau_vertice(i)
            t2 = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print(f"{v:<6} | {d:<10} | {'Matriz':<15} | {peak / 1024:<15.2f} | {t1 - t0:<18.6f} | {t2 - t1:.6f}")

            # Teste Lista de Adjacência
            tracemalloc.start()
            t0 = time.perf_counter()
            gl = GrafoLista(v)
            for u, w in arestas:
                gl.adicionar_aresta(u, w)
            t1 = time.perf_counter()
            
            for i in range(v):
                gl.grau_vertice(i)
            t2 = time.perf_counter()
            current_l, peak_l = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print(f"{v:<6} | {d:<10} | {'Lista':<15} | {peak_l / 1024:<15.2f} | {t1 - t0:<18.6f} | {t2 - t1:.6f}")
            print("-" * 85)

if __name__ == "__main__":
    benchmark()