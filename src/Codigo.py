from collections import defaultdict, deque
import xml.etree.ElementTree as ET
import pandas as pd

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
    #    Retorna os ciclo se QUALQUER ciclo for encontrado.
    # ------------------------------------------------------------------
    def encontrar_ciclo(self):
        visitado = {v: False for v in self.vertices}
        pilha = []  # caminho atual da DFS
        em_pilha = {v: False for v in self.vertices}

        def dfs(v):
            visitado[v] = True
            em_pilha[v] = True
            pilha.append(v)

            for vizinho in self.grafo[v]:
                if not visitado[vizinho]:
                    resultado = dfs(vizinho)
                    if resultado:
                        return resultado
                elif em_pilha[vizinho]:
                    # Encontramos ciclo: recorta caminho do ciclo
                    idx = pilha.index(vizinho)
                    return pilha[idx:]  # ciclo completo

            pilha.pop()
            em_pilha[v] = False
            return None

        for vertice in self.vertices:
            if not visitado[vertice]:
                ciclo = dfs(vertice)
                if ciclo:
                    return ciclo
        return None  # Nenhum ciclo encontrado

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
        grau_entrada = {v: 0 for v in self.vertices}
        for u in self.grafo:
            for v in self.grafo[u]:
                grau_entrada[v] += 1

        fila = deque([v for v in self.vertices if grau_entrada[v] == 0])
        ordem = []

        while fila:
            u = fila.popleft()
            ordem.append(u)
            for vizinho in self.grafo[u]:
                grau_entrada[vizinho] -= 1
                if grau_entrada[vizinho] == 0:
                    fila.append(vizinho)

        if len(ordem) != len(self.vertices):
            return None
        return ordem

    
    # ------------------------------------------------------------------
    # 6. carregar_de_arquivo(caminho_arquivo)
    #    Lê um arquivo csv onde cada linha tem "source,target" – dois strings
    #    separados por vírgula – e adiciona a aresta (source -> target).
    # ------------------------------------------------------------------
    def carregar_de_csv(self, caminho_csv):
        df = pd.read_csv(caminho_csv)
        for _, linha in df.iterrows():
            self.adicionar_aresta(str(linha['source']), str(linha['target']))

    # ----
    # 7. carregar_de_xml(caminho_xml)
    #    Lê um arquivo XML e adiciona as arestas ao grafo.
    # ----
    def carregar_de_xml(self, caminho_xml):
        tree = ET.parse(caminho_xml)
        root = tree.getroot()

        for service in root.findall('service'):
            service_name = service.get('name')
            inputs = [instance.get('name') for instance in service.find('inputs').findall('instance')]
            outputs = [instance.get('name') for instance in service.find('outputs').findall('instance')]
            
            # Adiciona arestas entre entradas e saídas
            for input_name in inputs:
                for output_name in outputs:
                    self.adicionar_aresta(input_name, output_name)

# ----------------------------------------------------------------------
# --------------------------- BLOCO PRINCIPAL --------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    g = Grafo()
    
    # Carregar de arquivos
    g.carregar_de_xml('./SERVICES DEPENDENCY GRAPHS FOR WEB SERVICES COMPOSITION MODELING DATASET/2-Pablo Rodríguez Mier Dataset/Original Web Rervice Repositories by Pablo Rodriguez Mier/3000/3000_Services with I_O parameters.xml')  # Carregando do XML
    # Adicione outros métodos de carregamento conforme necessário

    # Converte conjuntos para listas ordenadas, útil para frontend.
    vertices = sorted(list(g.vertices))
    arestas  = sorted(list(g.arestas))

    # Detecta ciclo
    ciclo = g.encontrar_ciclo()

     # Transforma ciclo (nós) em lista de arestas (u, v)
    ciclo_arestas = []
    if ciclo:
        for i in range(len(ciclo)):
            u = ciclo[i]
            v = ciclo[(i + 1) % len(ciclo)]  # liga último com o primeiro
            ciclo_arestas.append((u, v))

    # Calcula ordem topológica se for um DAG (grafo acíclico)
    ordem_topo = g.ordem_topologica() 

    # ---- Saídas para o frontend ----
    print("Vertices:", vertices)
    print("Arestas:",  arestas)
    print("Tem ciclo?", ciclo is not None)
    print("Ciclo (nós):", ciclo)
    print("Ciclo (arestas):", ciclo_arestas)
    print("Ordem topologica:", ordem_topo)