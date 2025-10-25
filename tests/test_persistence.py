import json
from pathlib import Path

from tasks import TaskManager


def test_add_and_load(tmp_path: Path):
    p = tmp_path / "mytasks.json"
    tm = TaskManager(str(p))
    assert tm.get_all() == []
    t = tm.add("comprar leite")
    assert t["id"] == 1
    assert t["title"] == "comprar leite"
    # reload from file
    tm2 = TaskManager(str(p))
    all_tasks = tm2.get_all()
    assert len(all_tasks) == 1
    assert all_tasks[0]["title"] == "comprar leite"


def test_update_and_remove(tmp_path: Path):
    p = tmp_path / "mytasks.json"
    tm = TaskManager(str(p))
    tm.add("t1")
    tm.add("t2")
    assert tm.update(1, title="t1-updated")
    assert tm.find(1)["title"] == "t1-updated"
    assert tm.toggle(2)
    assert tm.find(2)["done"] is True
    assert tm.remove(1)
    assert tm.find(1) is None
