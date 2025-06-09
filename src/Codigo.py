import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict, deque
import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# --- Classe Grafo ---
class Grafo:
    # --------------------------------------------------------------
    # 1. __init__()
    #    Inicializa as estruturas de dados do grafo: lista de adjacência,
    #    conjunto de arestas e conjunto de vértices.
    # --------------------------------------------------------------
    def __init__(self):
        self.grafo = defaultdict(list)
        self.arestas = set()
        self.vertices = set()

    # --------------------------------------------------------------
    # 2. adicionar_aresta(u, v)
    #    Adiciona uma aresta do vértice u para o vértice v.
    #    Atualiza as listas de adjacência, arestas e vértices.
    # --------------------------------------------------------------
    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)
        self.arestas.add((u, v))
        self.vertices.update([u, v])

    # --------------------------------------------------------------
    # 3. carregar_de_arquivo(caminho_arquivo)
    #    Lê um arquivo texto com pares de vértices por linha e adiciona as arestas.
    # --------------------------------------------------------------
    def carregar_de_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                u, v = map(int, linha.strip().split())
                self.adicionar_aresta(u, v)

    # ------------------------------------------------------------------
    # 4. encontrar_ciclo()
    #    Função de alto nível: percorre todos os vértices e inicia a DFS.
    #    Retorna o ciclo se QUALQUER ciclo for encontrado, senão None.
    # ------------------------------------------------------------------
    def encontrar_ciclo(self):
        visitado = {v: False for v in self.vertices}
        pilha = []
        em_pilha = {v: False for v in self.vertices}

        # --------------------------------------------------------------
        # 4.1 dfs(v)
        #     Busca em profundidade recursiva para detectar ciclos.
        #     Retorna o ciclo encontrado ou None.
        # --------------------------------------------------------------
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
                    idx = pilha.index(vizinho)
                    return pilha[idx:]

            pilha.pop()
            em_pilha[v] = False
            return None

        for vertice in self.vertices:
            if not visitado[vertice]:
                ciclo = dfs(vertice)
                if ciclo:
                    return ciclo
        return None

    # --------------------------------------------------------------
    # 5. ordem_topologica()
    #    Retorna uma lista com a ordem topológica dos vértices se o grafo
    #    for acíclico. Caso contrário, retorna None.
    # --------------------------------------------------------------
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

    # --------------------------------------------------------------
    # 6. carregar_de_csv(caminho_csv)
    #    Lê um arquivo CSV com colunas 'source' e 'target' e adiciona as arestas.
    # --------------------------------------------------------------
    def carregar_de_csv(self, caminho_csv):
        df = pd.read_csv(caminho_csv)
        for _, linha in df.iterrows():
            self.adicionar_aresta(str(linha['source']), str(linha['target']))

    # --------------------------------------------------------------
    # 7. carregar_de_xml(caminho_xml)
    #    Lê um arquivo XML no formato esperado e adiciona as arestas
    #    conforme as dependências entre inputs e outputs dos serviços.
    # --------------------------------------------------------------
    def carregar_de_xml(self, caminho_xml):
        tree = ET.parse(caminho_xml)
        root = tree.getroot()

        for service in root.findall('service'):
            inputs = [instance.get('name') for instance in service.find('inputs').findall('instance')]
            outputs = [instance.get('name') for instance in service.find('outputs').findall('instance')]
            
            for input_name in inputs:
                for output_name in outputs:
                    self.adicionar_aresta(input_name, output_name)

# ------------------------------------------------------------------
# Classe Principal da Aplicação (App)
# Responsável pela interface gráfica, carregamento de arquivos,
# análise do grafo e atualização dos resultados na interface.
# ------------------------------------------------------------------
class App(tk.Tk):
    # --------------------------------------------------------------
    # 1. __init__()
    #    Inicializa a janela principal, widgets, frames e configurações
    #    de estilo da interface gráfica.
    # --------------------------------------------------------------
    def __init__(self):
        super().__init__()

        self.title("Ferramenta de Análise de Grafos de Dependência")
        self.geometry("1000x800")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TLabel", padding=6, font=("Helvetica", 10))
        style.configure("TButton", padding=6, font=("Helvetica", 10, "bold"))
        style.configure("Result.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Cycle.TLabel", font=("Helvetica", 12, "bold"))

        self.caminho_arquivo = tk.StringVar(value="Nenhum arquivo carregado.")
        self.grafo_obj = None

        top_frame = ttk.Frame(self, padding="10")
        top_frame.pack(fill=tk.X, side=tk.TOP)

        ttk.Button(top_frame, text="Carregar Arquivo", command=self.carregar_arquivo).pack(side=tk.LEFT, padx=5)
        ttk.Label(top_frame, textvariable=self.caminho_arquivo, relief="sunken", padding=5).pack(fill=tk.X, expand=True, side=tk.LEFT)

        results_frame = ttk.Frame(self, padding="10")
        results_frame.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)

        ttk.Label(results_frame, text="Resultados da Análise", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=5)
        
        self.lbl_vertices = ttk.Label(results_frame, text="Vértices: -")
        self.lbl_vertices.pack(anchor="w")
        
        self.lbl_arestas = ttk.Label(results_frame, text="Arestas: -")
        self.lbl_arestas.pack(anchor="w")

        self.lbl_ciclo = ttk.Label(results_frame, text="Tem ciclo?: -", style="Cycle.TLabel")
        self.lbl_ciclo.pack(anchor="w", pady=10)

        ttk.Label(results_frame, text="Ordem Topológica:", style="Result.TLabel").pack(anchor="w", pady=(20, 5))
        
        self.txt_ordem_topo = tk.Text(results_frame, height=15, width=40, state="disabled", wrap="word", font=("Courier New", 10))
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.txt_ordem_topo.yview)
        self.txt_ordem_topo.configure(yscrollcommand=scrollbar.set)
        self.txt_ordem_topo.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        graph_frame = ttk.Frame(self, padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        self.figura = plt.Figure(figsize=(7, 7), dpi=100)
        self.ax = self.figura.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.ax.set_title("Visualização do Grafo")
        self.ax.axis('off')
        self.canvas.draw()

    # --------------------------------------------------------------
    # 2. carregar_arquivo()
    #    Abre o diálogo para seleção de arquivo, carrega o grafo a partir
    #    do arquivo selecionado e inicia a análise em uma thread separada.
    # --------------------------------------------------------------
    def carregar_arquivo(self):
        path = filedialog.askopenfilename(
            title="Selecione o arquivo de dependências",
            filetypes=(("Arquivos XML", "*.xml"), ("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if not path:
            return

        self.caminho_arquivo.set(path)
        self.grafo_obj = Grafo()
        
        try:
            if path.lower().endswith('.xml'):
                self.grafo_obj.carregar_de_xml(path)
            elif path.lower().endswith('.txt'):
                self.grafo_obj.carregar_de_arquivo(path)
            else:
                raise ValueError("Formato de arquivo não suportado.")
            
            # Executa a análise em uma thread separada
            threading.Thread(target=self.analisar_e_atualizar).start()

        except Exception as e:
            messagebox.showerror("Erro ao Carregar Arquivo", f"Ocorreu um erro: {e}")
            self.limpar_resultados()

    # --------------------------------------------------------------
    # 3. analisar_e_atualizar()
    #    Executa a análise do grafo (detecção de ciclo e ordem topológica)
    #    e agenda a atualização da interface na thread principal.
    # --------------------------------------------------------------
    def analisar_e_atualizar(self):
        if not self.grafo_obj:
            return
            
        tem_ciclo = self.grafo_obj.encontrar_ciclo() is not None
        ordem_topo = None
        if not tem_ciclo:
            ordem_topo = self.grafo_obj.ordem_topologica()

        # Atualiza a interface na thread principal
        self.after(0, self.atualizar_interface, tem_ciclo, ordem_topo)

    # --------------------------------------------------------------
    # 4. atualizar_interface(tem_ciclo, ordem_topo)
    #    Atualiza os rótulos, textos e cores da interface de acordo com
    #    os resultados da análise do grafo.
    # --------------------------------------------------------------
    def atualizar_interface(self, tem_ciclo, ordem_topo):
        self.lbl_vertices.config(text=f"Vértices: {len(self.grafo_obj.vertices)}")
        self.lbl_arestas.config(text=f"Arestas: {len(self.grafo_obj.arestas)}")

        if tem_ciclo:
            self.lbl_ciclo.config(text="Tem ciclo?: Sim", foreground="red")
            self.atualizar_texto_ordem("Não é possível gerar uma ordem topológica, pois o grafo contém um ciclo.")
        else:
            self.lbl_ciclo.config(text="Tem ciclo?: Não", foreground="green")
            if ordem_topo:
                ordem_formatada = " ->\n".join(map(str, ordem_topo))
                self.atualizar_texto_ordem(ordem_formatada)
            else:
                self.atualizar_texto_ordem("Ocorreu um erro ao gerar a ordem topológica.")
        
        self.desenhar_grafo(tem_ciclo)

    # --------------------------------------------------------------
    # 5. desenhar_grafo(tem_ciclo)
    #    Desenha o grafo na interface usando o matplotlib, destacando
    #    os nós do ciclo (se houver).
    # --------------------------------------------------------------
    def desenhar_grafo(self, tem_ciclo):
        self.ax.clear()

        if not self.grafo_obj or not self.grafo_obj.vertices:
            self.ax.set_title("Nenhum grafo para exibir")
            self.ax.axis('off')
            self.canvas.draw()
            return

        G = nx.DiGraph()
        G.add_edges_from(self.grafo_obj.arestas)

        # Usar um layout mais simples para melhorar a performance
        pos = nx.spring_layout(G, k=0.5, iterations=20)

        # Define a cor dos nós
        cor_nos = []
        if tem_ciclo:
            ciclo = self.grafo_obj.encontrar_ciclo()  # Obtém o ciclo
            for node in G.nodes():
                cor_nos.append('red' if node in ciclo else 'skyblue')
        else:
            cor_nos = ['skyblue'] * len(G.nodes())

        # Desenha o grafo
        nx.draw(G, pos, ax=self.ax, with_labels=True, 
                node_color=cor_nos,
                node_size=1500,
                font_size=8,
                font_weight='bold',
                arrows=True,
                arrowstyle='->',
                arrowsize=15,
                edge_color='gray')

        self.ax.set_title("Visualização do Grafo")
        self.ax.axis('off')
        self.canvas.draw()

    # --------------------------------------------------------------
    # 6. atualizar_texto_ordem(texto)
    #    Atualiza o conteúdo do widget de texto com a ordem topológica
    #    ou mensagem de erro.
    # --------------------------------------------------------------
    def atualizar_texto_ordem(self, texto):
        self.txt_ordem_topo.config(state="normal")
        self.txt_ordem_topo.delete("1.0", tk.END)
        self.txt_ordem_topo.insert(tk.END, texto)
        self.txt_ordem_topo.config(state="disabled")
        
    # --------------------------------------------------------------
    # 7. limpar_resultados()
    #    Limpa todos os resultados e reseta a interface para o estado inicial.
    # --------------------------------------------------------------
    def limpar_resultados(self):
        self.lbl_vertices.config(text="Vértices: -")
        self.lbl_arestas.config(text="Arestas: -")
        self.lbl_ciclo.config(text="Tem ciclo?: -", foreground="black")
        self.atualizar_texto_ordem("")
        self.ax.clear()
        self.ax.set_title("Visualização do Grafo")
        self.ax.axis('off')
        self.canvas.draw()

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    app = App()
    app.mainloop()