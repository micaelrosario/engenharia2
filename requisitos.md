# 🧾 Documento de Requisitos — Sistema de Lista de Tarefas

## 📘 Descrição Geral
Este documento descreve os **requisitos funcionais** e **não funcionais** do sistema de lista de tarefas (To-Do List).  
O objetivo é definir as principais funcionalidades e características técnicas que o sistema deve apresentar para garantir boa usabilidade, desempenho e manutenção.

---

## ✅ Requisitos Funcionais

| Código | Descrição |
|:------:|------------|
| **RF01** | O sistema deve permitir ao usuário adicionar novas tarefas através de um campo de texto e um botão “Adicionar”. |
| **RF02** | O sistema deve exibir todas as tarefas adicionadas em uma lista. |
| **RF03** | Cada tarefa deve possuir um checkbox para marcar como concluída ou pendente. |
| **RF04** | O sistema deve permitir selecionar todas as tarefas de uma só vez através do botão “Selecionar tudo”. |
| **RF05** | O sistema deve permitir excluir tarefas selecionadas através do botão “Excluir”. |
| **RF06** | O sistema deve permitir limpar todas as tarefas da lista através do botão “Limpar tudo”. |
| **RF07** | O sistema deve permitir mover tarefas excluídas para uma lixeira (sem apagá-las definitivamente). |
| **RF08** | O sistema deve possuir uma área ou botão para acessar a lixeira, onde é possível visualizar ou restaurar tarefas. |
| **RF09** | O sistema deve armazenar as tarefas localmente (em arquivo, banco de dados ou cache local) para que não se percam ao fechar o aplicativo. |
| **RF10** | O sistema deve exibir uma interface gráfica com campo de texto, lista e botões de ação. |

---

## ⚙️ Requisitos Não Funcionais

| Código | Descrição |
|:------:|------------|
| **RNF01** | A interface deve seguir o tema escuro (dark mode) com contraste adequado entre texto e fundo. |
| **RNF02** | O sistema deve ser intuitivo e fácil de usar, permitindo adicionar ou remover tarefas com poucos cliques. |
| **RNF03** | O sistema deve ser leve e rápido, com tempo de resposta inferior a 2 segundos para qualquer ação. |
| **RNF04** | O sistema deve ser compatível com Windows e Linux. |
| **RNF05** | O sistema deve armazenar as tarefas de forma persistente, garantindo que dados não sejam perdidos ao reiniciar. |
| **RNF06** | O código deve seguir boas práticas de organização, com funções separadas para interface, lógica e armazenamento. |
| **RNF07** | O sistema deve permitir fácil expansão futura, como integração com banco de dados, login de usuário ou sincronização em nuvem. |

---

## 📂 Observações
- O sistema será desenvolvido em **Python**, com interface feita em **PyQt5**.  
- O armazenamento inicial será feito em **arquivo JSON local**.  
- O design seguirá o padrão **Dark Mode** para maior conforto visual.  

---

📅 **Versão:** 1.0  
✍️ **Autores:** [Micael Rosário - João Mesquita - Cauã Blanco]  
🗓️ **Data:** [06/11/2025]
