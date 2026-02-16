from PyQt5.QtWidgets import QApplication

try:
    # Quando importado como pacote (python -m src.todoList)
    from .style import apply_app_style
    from .ui.main_window import AplicativoTarefas
except ImportError:  # pragma: no cover
    # Quando executado como script (python src/todoList.py)
    from style import apply_app_style
    from ui.main_window import AplicativoTarefas


# === Execução principal ===
if __name__ == "__main__": # pragma: no cover
    app = QApplication([])
    apply_app_style(app)
    janela = AplicativoTarefas()
    janela.show()
    app.exec_()
