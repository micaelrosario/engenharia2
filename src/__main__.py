from __future__ import annotations

from PyQt5.QtWidgets import QApplication

from .style import apply_app_style
from .ui.main_window import AplicativoTarefas


def main() -> None:
    app = QApplication([])
    apply_app_style(app)
    janela = AplicativoTarefas()
    janela.show()
    app.exec_()


if __name__ == "__main__":
    main()

