from __future__ import annotations

from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QBrush

try:
    # Quando importado como pacote (src.ui.main_window)
    from ..services.simple_store import ArmazenamentoSimples
except ImportError:  # pragma: no cover
    # Quando executado com a pasta src no sys.path
    from services.simple_store import ArmazenamentoSimples

try:
    # Quando importado como pacote
    from ..style import (
        style_buttons,
        style_message_box,
        style_task_input,
        style_task_list,
    )
except ImportError:  # pragma: no cover
    # Quando executado com a pasta src no sys.path
    from style import (
        style_buttons,
        style_message_box,
        style_task_input,
        style_task_list,
    )


class AplicativoTarefas(QWidget):
    """Interface principal do aplicativo de lista de tarefas."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Tarefas 📝")
        self._updating_list = False
        self._definir_tamanho_janela()
        self.armazenamento = ArmazenamentoSimples(Path("dados/tarefas.json"))
        self._configurar_interface()
        self._carregar_tarefas_salvas()

    def _definir_tamanho_janela(self) -> None:
        self.resize(400, 500)
        self.setMinimumWidth(350)

    def _configurar_interface(self) -> None:
        layout_principal = QVBoxLayout()
        layout_input = QHBoxLayout()

        self.campo_tarefa = QLineEdit()
        self.campo_tarefa.setPlaceholderText("Digite uma nova tarefa...")
        style_task_input(self.campo_tarefa)

        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_remover = QPushButton("Remover")
        style_buttons([self.botao_adicionar, self.botao_remover])

        self.lista_tarefas = QListWidget()
        self.lista_tarefas.setSelectionMode(QAbstractItemView.ExtendedSelection)
        style_task_list(self.lista_tarefas)

        layout_input.addWidget(self.campo_tarefa)
        layout_input.addWidget(self.botao_adicionar)
        layout_principal.addLayout(layout_input)
        layout_principal.addWidget(self.lista_tarefas)
        layout_principal.addWidget(self.botao_remover)
        self.setLayout(layout_principal)

        self.botao_adicionar.clicked.connect(self._adicionar_tarefa)
        self.botao_remover.clicked.connect(self._remover_tarefa)
        self.lista_tarefas.itemDoubleClicked.connect(self._alternar_status_tarefa)
        self.lista_tarefas.itemChanged.connect(self._on_item_changed)
        self.lista_tarefas.currentRowChanged.connect(self._atualizar_estado_botoes)
        self.campo_tarefa.returnPressed.connect(self._adicionar_tarefa)

        self._atualizar_estado_botoes()

    def _carregar_tarefas_salvas(self) -> None:
        self._updating_list = True
        try:
            self.lista_tarefas.blockSignals(True)
            self.lista_tarefas.clear()
            for tarefa in self.armazenamento.tarefas:
                titulo = str(tarefa.get("titulo", "")).strip()
                if not titulo:
                    continue

                item = QListWidgetItem(titulo)
                item.setFlags(
                    item.flags()
                    | Qt.ItemIsUserCheckable
                    | Qt.ItemIsSelectable
                    | Qt.ItemIsEnabled
                )
                item.setCheckState(Qt.Checked if tarefa.get("feito") else Qt.Unchecked)
                item.setForeground(QBrush(Qt.black))
                self._aplicar_estilo_conclusao(item)
                self.lista_tarefas.addItem(item)
        finally:
            self.lista_tarefas.blockSignals(False)
            self._updating_list = False
            self._atualizar_estado_botoes()

    def _adicionar_tarefa(self) -> None:
        titulo = self.campo_tarefa.text().strip()
        if not titulo:
            self._mostrar_aviso("Digite uma tarefa antes de adicionar.")
            return
        self.armazenamento.adicionar(titulo)
        self.campo_tarefa.clear()
        self._carregar_tarefas_salvas()

    def _remover_tarefa(self) -> None:
        itens = self.lista_tarefas.selectedItems()
        if not itens:
            self._mostrar_aviso("Selecione uma tarefa para remover.")
            return

        indices = sorted(
            {self.lista_tarefas.row(item) for item in itens},
            reverse=True,
        )

        tarefas = self.armazenamento.tarefas
        for indice in indices:
            if 0 <= indice < len(tarefas):
                tarefas.pop(indice)

        self.armazenamento.tarefas = tarefas
        self.armazenamento.salvar()
        self._carregar_tarefas_salvas()

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if self._updating_list:
            return

        indice = self.lista_tarefas.row(item)
        if indice < 0:
            return

        # Se o backend estiver fora de sincronia, recarrega.
        # Caso contrário, apenas alterna.
        tarefas = self.armazenamento.tarefas
        if indice >= len(tarefas):
            self._carregar_tarefas_salvas()
            return

        deseja_feito = item.checkState() == Qt.Checked
        atual_feito = bool(tarefas[indice].get("feito"))

        # Atualiza o visual (texto riscado) sem re-disparar itemChanged.
        self._updating_list = True
        try:
            self.lista_tarefas.blockSignals(True)
            self._aplicar_estilo_conclusao(item)
        finally:
            self.lista_tarefas.blockSignals(False)
            self._updating_list = False

        if deseja_feito != atual_feito:
            self.armazenamento.alternar_status(indice)

    def _alternar_status_tarefa(self, item) -> None:
        # Mantém o duplo clique como atalho: alterna o checkbox.
        estado = item.checkState()
        item.setCheckState(Qt.Unchecked if estado == Qt.Checked else Qt.Checked)

    def _atualizar_estado_botoes(self) -> None:
        self.botao_remover.setEnabled(len(self.lista_tarefas.selectedItems()) > 0)

    def _mostrar_aviso(self, mensagem: str) -> None:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("Aviso")
        box.setText(mensagem)
        box.setStandardButtons(QMessageBox.Ok)
        style_message_box(box)
        box.exec_()

    def _aplicar_estilo_conclusao(self, item: QListWidgetItem) -> None:
        fonte = item.font()
        fonte.setStrikeOut(item.checkState() == Qt.Checked)
        item.setFont(fonte)
