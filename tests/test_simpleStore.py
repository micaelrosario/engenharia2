import json
import tempfile
from pathlib import Path
from src.todoList import SimpleStore


def test_criacao_de_tarefa():
    """Testa se uma tarefa é criada corretamente e salva no arquivo JSON."""
    with tempfile.TemporaryDirectory() as tmp:
        data_path = Path(tmp) / "tasks.json"
        store = SimpleStore(data_path)
        
        tarefa = store.add("Estudar PyQt5")
        
        # Verifica se o ID e título foram gerados corretamente
        assert tarefa["id"] == 1
        assert tarefa["title"] == "Estudar PyQt5"
        assert tarefa["done"] is False
        
        # Verifica se foi salva no arquivo
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Estudar PyQt5"


def test_criacao_varias_tarefas_ids_incrementais():
    """Verifica se múltiplas tarefas recebem IDs únicos e incrementais."""
    with tempfile.TemporaryDirectory() as tmp:
        store = SimpleStore(Path(tmp) / "tasks.json")
        
        t1 = store.add("Tarefa 1")
        t2 = store.add("Tarefa 2")
        t3 = store.add("Tarefa 3")

        assert t1["id"] == 1
        assert t2["id"] == 2
        assert t3["id"] == 3
        assert len(store.tasks) == 3


def test_salvamento_e_recuperacao_do_arquivo():
    """Garante que os dados persistem entre execuções."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "tasks.json"
        
        store1 = SimpleStore(path)
        store1.add("Tarefa Persistente")
        store1.save()
        
        # Nova instância deve carregar o mesmo dado
        store2 = SimpleStore(path)
        assert len(store2.tasks) == 1
        assert store2.tasks[0]["title"] == "Tarefa Persistente"
