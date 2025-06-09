
# 📦 Gestão de Conflitos em Sistemas de Dependência
> Trabalho Prático — Grafos (2025)

Projeto acadêmico desenvolvido em **Python** para simular sistemas de tarefas interdependentes utilizando grafos dirigidos. O objetivo é detectar **ciclos de dependência**, executar uma **ordenação topológica segura** e fornecer **visualização interativa** do grafo.

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
| Python    | Linguagem de programação principal     |
| Python,networkx,matplotlib,scipy      | Interface gráfica |
| matplotlib networkx pandas | Visualização gráfica de grafos (extra) |
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

## 📥 Formato Esperado dos Dados (Xml)

```Xml
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

- ✅ Leitura de dados a partir de `.xml` ou `.csv`
- ✅ Construção de grafo dirigido com tarefas
- ✅ Detecção de ciclos (DFS)
- ✅ Ordenação topológica segura (Kahn)
- ✅ Interface gráfica com interação de escolha de arquivo e visualização

---

## 📈 Visualização (Em Planejamento)

> Em python:
- Cores diferentes para ciclos detectados
- Ordem de execução numerada
- Feedback ao usuário com logs

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
| Luisa,Luiz  | Interface gráfica                         |
| Davi, Pedro | Leitura de arquivos e testes              |
| Pedro, Davi | Integração                                |

---

## 📜 Licença

Uso acadêmico sob responsabilidade da equipe.  
Desenvolvido para fins educacionais na disciplina de Grafos – 2025.

---
