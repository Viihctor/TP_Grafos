import unittest
from Codigo import Grafo  # Corrigido para importar a classe Grafo

class TestGrafo(unittest.TestCase):

    def setUp(self):
        self.grafo = Grafo()
        # Adicionando arestas para os testes
        self.grafo.adicionar_aresta('A', 'B')
        self.grafo.adicionar_aresta('B', 'C')
        self.grafo.adicionar_aresta('C', 'A')  # Criando um ciclo

    def test_adicionar_aresta(self):
        self.grafo.adicionar_aresta('D', 'E')
        self.assertIn(('D', 'E'), self.grafo.arestas, "Aresta (D, E) não foi adicionada corretamente.")
        self.assertIn('D', self.grafo.vertices, "Vértice D não foi adicionado corretamente.")
        self.assertIn('E', self.grafo.vertices, "Vértice E não foi adicionado corretamente.")

    def test_tem_ciclo(self):
        self.assertTrue(self.grafo.encontrar_ciclo(), "O grafo deveria ter um ciclo.")

        # Criando um grafo acíclico
        grafo_aciclico = Grafo()
        grafo_aciclico.adicionar_aresta('X', 'Y')
        grafo_aciclico.adicionar_aresta('Y', 'Z')
        self.assertFalse(grafo_aciclico.encontrar_ciclo(), "O grafo acíclico não deveria ter ciclos.")

    def test_ordem_topologica(self):
        # Testando a ordem topológica em um grafo acíclico
        grafo_aciclico = Grafo()
        grafo_aciclico.adicionar_aresta('X', 'Y')
        grafo_aciclico.adicionar_aresta('Y', 'Z')
        ordem = grafo_aciclico.ordem_topologica()
        self.assertEqual(ordem, ['X', 'Y', 'Z'], "A ordem topológica não está correta.")

    def test_carregar_de_xml(self):
        # Teste para verificar se as arestas são carregadas corretamente do XML
        self.grafo.carregar_de_xml('./SERVICES DEPENDENCY GRAPHS FOR WEB SERVICES COMPOSITION MODELING DATASET/2-Pablo Rodríguez Mier Dataset/Generated Repositories with Random Parameters/1000/1000_Services with RANDOM I_O parameters.xml')
        
        # Verifique se as arestas esperadas estão presentes
        self.assertIn(('S2', 'S1'), self.grafo.arestas, "Aresta (S2, S1) não foi carregada corretamente.")
        self.assertIn(('S1', 'S3'), self.grafo.arestas, "Aresta (S1, S3) não foi carregada corretamente.")

    def test_carregar_de_xml_invalido(self):
        # Teste para verificar se o método lida com um XML inválido
        with self.assertRaises(FileNotFoundError):
            self.grafo.carregar_de_xml('./caminho/invalido.xml')

    def test_grafo_vazio(self):
        grafo_vazio = Grafo()
        self.assertFalse(grafo_vazio.encontrar_ciclo(), "Um grafo vazio não deve ter ciclos.")
        self.assertEqual(grafo_vazio.ordem_topologica(), [], "A ordem topológica de um grafo vazio deve ser uma lista vazia.")

if __name__ == '__main__':
    unittest.main()