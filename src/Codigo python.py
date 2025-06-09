from collections import defaultdict, deque

class Grafo:
    def __init__(self):
        # defaultdict(list) cria, automaticamente, uma lista vazia para cada
        # nova chave usada. Isso simplifica a inserção de arestas.
        self.grafo = defaultdict(list)

        # Conjuntos são úteis para evitar duplicidades.
        self.arestas = set()     # Conjunto de tuplas (u, v) com TODAS as arestas
        self.vertices = set()    # Conjunto com TODOS os vértices presentes

    # ------------------------------------------------------------------
    # 1. adicionar_aresta(u, v)
    #    Adiciona uma aresta DIRECIONADA do vértice u para o vértice v ;
    #    também registra u e v nos conjuntos auxiliares.
    # ------------------------------------------------------------------
    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)        # registra vizinho
        self.arestas.add((u, v))       # guarda tupla da aresta
        self.vertices.update([u, v])   # garante que ambos vértices existam

    # ------------------------------------------------------------------
    # 2. carregar_de_arquivo(caminho_arquivo)
    #    Lê um arquivo txt onde cada linha tem "u v" – dois inteiros
    #    separados por espaço – e adiciona a aresta (u -> v).
    # ------------------------------------------------------------------
    def carregar_de_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                # strip remove \n; split separa por espaço; map(int) converte
                u, v = map(int, linha.strip().split())
                self.adicionar_aresta(u, v)

    # ------------------------------------------------------------------
    # 3. tem_ciclo_util(v, visitado, pilha_rec)
    #    DFS recursiva para grafo DIRECIONADO.
    #    visitado  -> marca vértices já visitados em QUALQUER DFS
    #    pilha_rec -> marca vértices no caminho atual da recursão
    # ------------------------------------------------------------------
    def tem_ciclo_util(self, v, visitado, pilha_rec):
        visitado[v] = True      # marca como visitado globalmente
        pilha_rec[v] = True     # entra na pilha de chamada

        for vizinho in self.grafo[v]:
            if not visitado[vizinho]:
                # segue recursivamente
                if self.tem_ciclo_util(vizinho, visitado, pilha_rec):
                    return True
            elif pilha_rec[vizinho]:
                # Encontrou um vértice na pilha -> retro-aresta -> ciclo
                return True

        pilha_rec[v] = False    # sai da pilha antes de retornar
        return False

    # ------------------------------------------------------------------
    # 4. tem_ciclo()
    #    Função de alto nível: percorre todos os vértices e inicia a DFS.
    #    Retorna True se QUALQUER ciclo for encontrado.
    # ------------------------------------------------------------------
    def tem_ciclo(self):
        visitado  = {v: False for v in self.vertices}
        pilha_rec = {v: False for v in self.vertices}

        for vertice in self.vertices:
            if not visitado[vertice]:
                if self.tem_ciclo_util(vertice, visitado, pilha_rec):
                    return True
        return False

    # ------------------------------------------------------------------
    # 5. ordem_topologica()
    #    Implementa o algoritmo de Kahn (BFS) para obter uma ordenação
    #    topológica. Só existe se o grafo NÃO tiver ciclos.
    #
    #    Passos:
    #      1. Calcula o grau de entrada (in-degree) de cada vértice.
    #      2. Enfileira vértices com grau 0.
    #      3. Remove vértices da fila, “eliminando” suas arestas,
    #         e enfileira vizinhos que chegam a grau 0.
    #      4. Se ao final não processamos todos os vértices,
    #         significa que há ciclo → retorna None.
    # ------------------------------------------------------------------
    def ordem_topologica(self):
        # 1. Grau de entrada
        grau_entrada = {v: 0 for v in self.vertices}
        for u in self.grafo:
            for v in self.grafo[u]:
                grau_entrada[v] += 1

        # 2. Fila com vértices que já têm grau 0
        fila = deque([v for v in self.vertices if grau_entrada[v] == 0])

        ordem = []  # resultado final

        # 3. Processa a fila
        while fila:
            u = fila.popleft()
            ordem.append(u)

            for vizinho in self.grafo[u]:
                grau_entrada[vizinho] -= 1
                if grau_entrada[vizinho] == 0:
                    fila.append(vizinho)

        # 4. Verifica se processou todos os vértices
        if len(ordem) != len(self.vertices):
            return None  # Ainda restam vértices → ciclo presente
        return ordem


# ----------------------------------------------------------------------
# --------------------------- BLOCO PRINCIPAL --------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    caminho_arquivo = 'grafo.txt'  # Altere se necessário

    g = Grafo()
    g.carregar_de_arquivo(caminho_arquivo)

    # Converte conjuntos para listas ordenadas, útil para frontend.
    vertices = sorted(list(g.vertices))
    arestas  = sorted(list(g.arestas))

    # Detecta ciclo
    tem_ciclo = g.tem_ciclo()

    # Calcula ordem topológica se for um DAG (grafo acíclico)
    ordem_topo = g.ordem_topologica() if not tem_ciclo else None

    # ---------------- Saídas para o frontend -----------------
    print("Vertices:", vertices)
    print("Arestas:",  arestas)
    print("Tem ciclo?", tem_ciclo)
    print("Ordem topológica:", ordem_topo)
