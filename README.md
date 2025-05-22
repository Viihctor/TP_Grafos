
# 📦 Gestão de Conflitos em Sistemas de Dependência
> Trabalho Prático — Grafos (2025)

Projeto acadêmico desenvolvido em **Java** para simular sistemas de tarefas interdependentes utilizando grafos dirigidos. O objetivo é detectar **ciclos de dependência**, executar uma **ordenação topológica segura** e fornecer **visualização interativa** do grafo.

---

## 🎯 Objetivo

- Representar tarefas e dependências como um **grafo dirigido**
- Detectar **ciclos** que inviabilizam a execução
- Realizar **ordenação topológica** para definir a execução segura
- Visualizar o grafo e permitir interação com o usuário

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia  | Uso                                   |
|-------------|----------------------------------------|
| Java 17+    | Linguagem de programação principal     |
| JGraphT     | Estrutura e algoritmos de grafos       |
| JavaFX      | Interface gráfica (alternativa: Swing) |
| GraphStream | Visualização gráfica de grafos (extra) |
| JUnit       | Testes unitários                       |
| Maven       | Gerenciamento de dependências          |
| Git         | Controle de versão                     |

---

## 📁 Estrutura do Projeto

```

├── 📁 src/
|
├── 📁 relatorio/
|
├── 📁 dados/
|
└── README.md
```
---

## ▶️ Como Executar o Projeto

## 📥 Formato Esperado dos Dados (JSON)

```json
{
  "tarefas": [
    { "id": "A", "dependencias": [] },
    { "id": "B", "dependencias": ["A"] },
    { "id": "C", "dependencias": ["A", "B"] },
    { "id": "D", "dependencias": ["C"] }
  ]
}
```

---

## 📋 Funcionalidades

- ✅ Leitura de dados a partir de `.json` ou `.csv`
- ✅ Construção de grafo dirigido com tarefas
- ✅ Detecção de ciclos (Tarjan ou DFS)
- ✅ Ordenação topológica segura (Kahn ou DFS)
- ✅ Interface gráfica para interação e visualização
- ✅ Exportação de relatório (opcional)

---

## 📈 Visualização (Em Planejamento)

> Se usar GraphStream ou JavaFX:
- Cores diferentes para ciclos detectados
- Ordem de execução numerada
- Feedback ao usuário com alertas ou logs

---

## ✅ Testes

```bash
mvn test
```

> Testes em JUnit para:
- Casos com e sem ciclos
- Ordenação topológica correta
- Leitura de arquivos de dados

---

## 👥 Equipe

| Nome                | Função no Projeto                         |
|Victor L. Tornelli   | Modelagem de grafos e documentação inicial|
| ------------------  | -----------------------------------       |
| ------------------  | Interface gráfica                         |
| ------------------  | Leitura de arquivos e testes              |
| ------------------  | Integração                                |

---

## 📜 Licença

Uso acadêmico sob responsabilidade da equipe.  
Desenvolvido para fins educacionais na disciplina de Grafos – 2025.

---