import pytest
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

from src.todoList import ToDoApp, SimpleStore


def _make_app(qtbot, tmp_path=None):
    app = QApplication.instance() or QApplication([])
    janela = ToDoApp()
    if tmp_path is not None:
        janela.store = SimpleStore(str(tmp_path / "tasks.json"))
    qtbot.addWidget(janela)
    return janela


def test_handle_delete_sem_selecao_mostra_dialog(qtbot, monkeypatch):
    """Quando não há seleção, handle_delete deve abrir um QMessageBox (monkeypatchado)."""
    janela = _make_app(qtbot)

    called = {"exec": False}

    def fake_exec(self):
        called["exec"] = True
        return QMessageBox.Ok

    monkeypatch.setattr(QMessageBox, "exec_", fake_exec)

    # Garante que nada esteja selecionado
    janela.task_list.clearSelection()
    janela.handle_delete()
    assert called["exec"] is True


def test_handle_delete_com_selecao_remove_item(qtbot, tmp_path):
    """Quando um item está selecionado, handle_delete deve remover do store e atualizar a lista."""
    janela = _make_app(qtbot, tmp_path)

    # adicionar tarefas
    janela.store.add("t1")
    janela.store.add("t2")
    janela.refresh()

    # seleciona primeiro item
    item = janela.task_list.item(0)
    janela.task_list.setCurrentItem(item)

    janela.handle_delete()

    assert len(janela.store.tasks) == 1


def test_handle_item_changed_aplica_toggle(qtbot, tmp_path):
    """Simular mudança do checkbox e garantir que a store seja atualizada."""
    janela = _make_app(qtbot, tmp_path)

    t = janela.store.add("x")
    janela.refresh()

    item = janela.task_list.item(0)
    # simula usuário marcar
    item.setCheckState(Qt.Checked)
    janela.handle_item_changed(item)
    assert janela.store.find(t["id"]) ["done"] is True

    # simula usuário desmarcar
    item.setCheckState(Qt.Unchecked)
    janela.handle_item_changed(item)
    assert janela.store.find(t["id"]) ["done"] is False
