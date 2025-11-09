import json
from pathlib import Path
import re
import pytest


def _carrega_classe_armazenamento():
    """Carrega a classe ArmazenamentoSimples do arquivo `src/todoList.py`
       sem importar PyQt5, permitindo testar persistência isoladamente.
    """
    base = Path(__file__).resolve().parents[2]
    arquivo = base / "src" / "todoList.py"

    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo.resolve()}")

    src = arquivo.read_text(encoding="utf-8")

    m = re.search(r"class ArmazenamentoSimples\b.*?(?=\nclass |\Z)", src, flags=re.S)
    assert m, "Não foi possível localizar `class ArmazenamentoSimples` em todoList.py"
    class_src = m.group(0)

    ns: dict = {
        "Path": Path,
        "json": json,
        "DADOS_PADRAO": []
    }
    exec(class_src, ns)
    return ns["ArmazenamentoSimples"]


def test_salvar_cria_arquivo_e_conteudo(tmp_path):
    """Verifica se salvar() cria o arquivo e grava corretamente as tarefas."""
    ArmazenamentoSimples = _carrega_classe_armazenamento()
    caminho = tmp_path / "data" / "tasks.json"
    store = ArmazenamentoSimples(caminho)
    store.tarefas = [
        {"id": 1, "titulo": "Tarefa teste — café", "feito": False},
        {"id": 2, "titulo": "Outra tarefa", "feito": True},
    ]
    store.salvar()

    assert caminho.exists()
    with caminho.open("r", encoding="utf-8") as f:
        dados = json.load(f)

    assert dados == store.tarefas


def test_salvar_cria_pastas_necessarias(tmp_path):
    """Verifica se salvar() cria as pastas pai automaticamente."""
    ArmazenamentoSimples = _carrega_classe_armazenamento()
    caminho_aninhado = tmp_path / "a" / "b" / "c" / "tasks.json"
    store = ArmazenamentoSimples(caminho_aninhado)
    store.tarefas = [{"id": 1, "titulo": "Teste", "feito": False}]
    
    # Garante que o diretório pai não existe antes
    assert not caminho_aninhado.parent.exists()
    store.salvar()
    assert caminho_aninhado.exists()


def test_salvar_sobrescreve_arquivo_existente(tmp_path):
    """Verifica se salvar() sobrescreve corretamente um arquivo existente."""
    ArmazenamentoSimples = _carrega_classe_armazenamento()
    caminho = tmp_path / "tasks.json"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps([{"id": 99, "titulo": "Antigo", "feito": True}]), encoding="utf-8")

    store = ArmazenamentoSimples(caminho)
    store.tarefas = [{"id": 5, "titulo": "Novo", "feito": False}]
    store.salvar()

    with caminho.open("r", encoding="utf-8") as f:
        dados = json.load(f)

    assert dados == store.tarefas


def test_salvar_erro_quando_pai_e_arquivo(tmp_path):
    """Garante que salvar() lança FileExistsError se o diretório pai for um arquivo."""
    ArmazenamentoSimples = _carrega_classe_armazenamento()
    bloqueado = tmp_path / "src"
    bloqueado.write_text("Sou um arquivo, não um diretório", encoding="utf-8")
    destino = bloqueado / "tasks.json"

    store = ArmazenamentoSimples(destino)
    store.tarefas = [{"id": 1, "titulo": "Erro", "feito": False}]

    with pytest.raises(FileExistsError):
        store.salvar()
