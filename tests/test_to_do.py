import json
from pathlib import Path

from to_do import SimpleStore


def teste_adicionar_e_encontrar(tmp_path: Path):
    """Adicionar uma tarefa e encontrá-la pela id."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    assert s.tasks == []
    t = s.add("comprar pão")
    assert t["title"] == "comprar pão"
    assert s.find(t["id"]) is not None


def teste_remover_move_para_lixeira(tmp_path: Path):
    """Remover uma tarefa deve movê-la para a lixeira."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    t1 = s.add("tarefa um")
    t2 = s.add("tarefa dois")
    assert s.remove(t1["id"]) is True
    assert s.find(t1["id"]) is None
    assert any(x["id"] == t1["id"] for x in s.trash)


def teste_restaurar_da_lixeira(tmp_path: Path):
    """Restaurar uma tarefa previamente removida."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    t = s.add("vai e volta")
    tid = t["id"]
    s.remove(tid)
    assert any(x["id"] == tid for x in s.trash)
    assert s.restore(tid) is True
    assert s.find(tid) is not None


def teste_toggle_e_set_all(tmp_path: Path):
    """Alternar estado de concluído e aplicar set_all."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    a = s.add("a")
    b = s.add("b")
    assert s.find(a["id"]) is not None
    assert s.find(a["id"]) ["done"] is False
    assert s.toggle(a["id"]) is True
    assert s.find(a["id"]) ["done"] is True
    s.set_all(False)
    assert all(not t.get("done") for t in s.tasks)


def teste_clear_move_tudo_para_lixeira(tmp_path: Path):
    """Clear deve mover todas as tarefas para a lixeira e limpar a lista."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    s.add("x")
    s.add("y")
    s.clear()
    assert s.tasks == []
    assert len(s.trash) >= 2
