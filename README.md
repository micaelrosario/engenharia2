# To‑Do List

Este repositório contém uma aplicação To‑Do em Python com interface gráfica (PyQt5),
persistência simples em JSON e uma suíte de testes mínimas com pytest. O objetivo foi
deixar a aplicação mais visível e prática (tema escuro, checkboxes, lixeira, persistência).

Funcionalidades principais
- GUI com PyQt5 (entrypoint em `src/todoList.py`)
	- Adicionar tarefas
	- Marcar/desmarcar tarefas via checkbox
	- Botão "Selecionar tudo" (marca/desmarca todas)
	- Excluir tarefas (movem para a lixeira)
	- Lixeira com restaurar / excluir permanentemente
	- Tema escuro com área central da lixeira em fundo branco para legibilidade
- Persistência em JSON (classe `ArmazenamentoSimples` em `src/services/simple_store.py`)
- Estilos centralizados em `style.py` (helpers para botões, lista, paleta)
- Testes com pytest em `tests/`

Qualidade de código
- Lint com Ruff (config em `pyproject.toml`)

Requisitos
- Python 3.8+ (testado com 3.13+)
- PyQt5
- pytest (para executar os testes)

Instalação rápida (Windows PowerShell)
1. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale dependências:

```powershell
pip install -r requirements.txt
# ou, se preferir instalar manualmente:
pip install pyqt5 pytest
```

Como executar
- Abrir a interface gráfica (recomendado):

```powershell
python -m src
```

- Alternativa (modo script):

```powershell
python src/todoList.py
```

- Executar os testes:

```powershell
pytest
```

- Rodar lint (Ruff):

```powershell
python -m ruff check .
```

Nota sobre a suíte completa de testes
Alguns arquivos de teste antigos (por exemplo `tests/test_persistence.py`) podem esperar
uma implementação diferente (`tasks.py`). Se quiser rodar todos os testes do repositório,
confirme se existe um `tasks.py` compatível ou atualize/remova os testes antigos.

Estrutura de arquivos (resumo)
- `src/todoList.py` — entrypoint da aplicação
- `src/ui/` — interface gráfica
- `src/services/` — backend/regras (sem UI)
- `src/persistence/` — persistência (JSON, etc.)
- `src/style.py` — helpers de estilo e paleta
- `tests/` — testes automatizados
- `requirements.txt` — dependências do projeto

Contribuindo
- Abra uma issue explicando a sugestão.
- Envie um pull request com mudanças pequenas e testes quando apropriado.

Licença
- Sem licença explícita (adicione um arquivo LICENSE se quiser abrir para contribuição pública).
