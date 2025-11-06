import json
from pathlib import Path
import re
import pytest


def _carrega_classe_simplestore():
    """Carrega a classe SimpleStore do arquivo `to_do.py` sem importar PyQt5.
       Isso permite testar persistência sem requerer PyQt5 no ambiente de execução.
    """
    base = Path(__file__).resolve().parents[2]
    src = (base / "to_do.py").read_text(encoding="utf-8")
    m = re.search(r"class SimpleStore\b.*?(?=\nclass |\Z)", src, flags=re.S)
    assert m, "Não foi possível localizar `class SimpleStore` em to_do.py"
    class_src = m.group(0)
    ns: dict = {"Path": Path, "json": json}
    exec(class_src, ns)
    return ns["SimpleStore"]


def test_salva_escreve_arquivo_e_conteudo(tmp_path):
    SimpleStore = _carrega_classe_simplestore()
    caminho = tmp_path / "data" / "tasks.json"
    store = SimpleStore(caminho)
    store.tasks = [{"id": 1, "title": "tarefa unicode — café", "done": False}]
    store.trash = [{"id": 2, "title": "antigo", "done": True}]
    store.save()

    assert caminho.exists()
    with caminho.open("r", encoding="utf-8") as f:
        dados = json.load(f)
    assert dados["tasks"] == store.tasks
    assert dados["trash"] == store.trash


def test_salva_cria_pastas_pais(tmp_path):
    SimpleStore = _carrega_classe_simplestore()
    nested = tmp_path / "a" / "b" / "c" / "tasks.json"
    store = SimpleStore(nested)
    store.tasks = [{"id": 1, "title": "x", "done": False}]
    # garante que o diretório pai não existe antes
    assert not nested.parent.exists()
    store.save()
    assert nested.exists()


def test_salva_sobrescreve_arquivo_existente(tmp_path):
    SimpleStore = _carrega_classe_simplestore()
    p = tmp_path / "tasks.json"
    # criar arquivo inicial com conteúdo diferente
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"tasks": [], "trash": []}', encoding="utf-8")
    store = SimpleStore(p)
    store.tasks = [{"id": 5, "title": "novo", "done": True}]
    store.trash = []
    store.save()
    with p.open("r", encoding="utf-8") as f:
        dados = json.load(f)
    assert dados["tasks"] == store.tasks


def test_salva_lanca_se_pai_e_arquivo(tmp_path):
    """Quando o pai (parent) do arquivo é um arquivo comum, mkdir deve lançar FileExistsError."""
    SimpleStore = _carrega_classe_simplestore()
    blocked = tmp_path / "blocked"
    blocked.write_text("Sou um arquivo, não um diretório", encoding="utf-8")
    target = blocked / "tasks.json"
    store = SimpleStore(target)
    store.tasks = [{"id": 1, "title": "t", "done": False}]
    with pytest.raises(FileExistsError):
        store.save()
