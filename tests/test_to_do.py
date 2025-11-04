import json
from pathlib import Path

from to_do import SimpleStore


def teste_adicionar_e_persistir(tmp_path: Path):
    """Adicionar uma tarefa e verificar que foi persistida no arquivo JSON."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    assert s.tasks == []
    t = s.add("comprar leite")
    assert t["title"] == "comprar leite"
    # arquivo foi criado e contém a tarefa
    assert arquivo.exists()
    data = json.loads(arquivo.read_text(encoding="utf-8"))
    assert "tasks" in data and len(data["tasks"]) == 1


def teste_buscar_por_id(tmp_path: Path):
    """Buscar uma tarefa existente por id."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    a = s.add("t1")
    _ = s.add("t2")
    assert s.find(a["id"]) is not None


def teste_remover_move_para_lixeira(tmp_path: Path):
    """Remover uma tarefa deve movê-la para a lixeira."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    a = s.add("t1")
    _ = s.add("t2")
    assert s.remove(a["id"]) is True
    assert s.find(a["id"]) is None
    assert any(x["id"] == a["id"] for x in s.trash)


def teste_restaurar_da_lixeira(tmp_path: Path):
    """Restaurar uma tarefa previamente removida."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    a = s.add("t1")
    s.remove(a["id"])
    assert any(x["id"] == a["id"] for x in s.trash)
    assert s.restore(a["id"]) is True
    assert s.find(a["id"]) is not None


def teste_toggle_e_set_all(tmp_path: Path):
    """Alternar estado done e aplicar set_all."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    x = s.add("x")
    y = s.add("y")
    assert s.toggle(x["id"]) is True
    assert s.find(x["id"])["done"] is True
    s.set_all(False)
    assert all(not t.get("done") for t in s.tasks)


def teste_clear_mover_para_lixeira(tmp_path: Path):
    """Clear deve mover todas as tarefas para a lixeira."""
    arquivo = tmp_path / "tasks.json"
    s = SimpleStore(str(arquivo))
    s.add("um")
    s.add("dois")
    s.clear()
    assert s.tasks == []
    assert len(s.trash) >= 2
