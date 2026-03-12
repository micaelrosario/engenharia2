from __future__ import annotations

from pathlib import Path
from typing import Any

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QShortcut,
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QBrush, QKeySequence

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
    from style import (
        style_buttons,
        style_message_box,
        style_task_input,
        style_task_list,
    )


class AplicativoTarefas(QWidget):
    """Interface principal do aplicativo de lista de tarefas."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Lista de Tarefas 📝")
        self._updating_list: bool = False
        self._ultima_remocao: list[tuple[int, dict[str, Any]]] = []
        self._definir_tamanho_janela()
        self.armazenamento: ArmazenamentoSimples = ArmazenamentoSimples(
            Path("dados/tarefas.json")
        )
        self._configurar_interface()
        self._carregar_tarefas_salvas()

    def _definir_tamanho_janela(self) -> None:
        self.resize(400, 500)
        self.setMinimumWidth(350)

    def _configurar_interface(self) -> None:
        layout_principal = QVBoxLayout()
        layout_input = QHBoxLayout()
        layout_acoes = QHBoxLayout()

        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(12)
        layout_input.setSpacing(10)
        layout_acoes.setSpacing(10)

        self.campo_tarefa = QLineEdit()
        self.campo_tarefa.setPlaceholderText("Digite uma nova tarefa...")
        self.campo_tarefa.setClearButtonEnabled(True)
        self.campo_tarefa.setToolTip(
            "Digite a tarefa e pressione Enter para adicionar."
        )
        style_task_input(self.campo_tarefa)

        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_desfazer = QPushButton("Desfazer")
        self.botao_remover = QPushButton("Remover")

        # Destaca a ação principal com o tema azul.
        self.botao_adicionar.setProperty("variant", "primary")

        self.botao_adicionar.setToolTip("Adicionar tarefa (Enter)")
        self.botao_desfazer.setToolTip("Desfazer última remoção (Ctrl+Z)")
        self.botao_remover.setToolTip("Remover tarefas selecionadas")
        style_buttons([self.botao_adicionar, self.botao_desfazer, self.botao_remover])

        self.lista_tarefas = QListWidget()
        self.lista_tarefas.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lista_tarefas.setToolTip("Duplo clique: marcar/desmarcar como concluída.")
        style_task_list(self.lista_tarefas)

        layout_input.addWidget(self.campo_tarefa)
        layout_input.addWidget(self.botao_adicionar)
        layout_principal.addLayout(layout_input)
        layout_principal.addWidget(self.lista_tarefas)

        layout_acoes.addWidget(self.botao_desfazer)
        layout_acoes.addWidget(self.botao_remover)
        layout_principal.addLayout(layout_acoes)
        self.setLayout(layout_principal)

        self.botao_adicionar.clicked.connect(self._adicionar_tarefa)
        self.botao_desfazer.clicked.connect(self._desfazer_ultima_remocao)
        self.botao_remover.clicked.connect(self._remover_tarefa)
        self.lista_tarefas.itemDoubleClicked.connect(self._alternar_status_tarefa)
        self.lista_tarefas.itemChanged.connect(self._on_item_changed)
        self.lista_tarefas.currentRowChanged.connect(self._atualizar_estado_botoes)
        self.campo_tarefa.returnPressed.connect(self._adicionar_tarefa)

        self._atalho_desfazer = QShortcut(QKeySequence.Undo, self)
        self._atalho_desfazer.activated.connect(self._desfazer_ultima_remocao)

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

        adicionado = self.armazenamento.adicionar(titulo)
        if not adicionado:
            self._mostrar_aviso("Essa tarefa já existe.")
            return

        self.campo_tarefa.clear()
        self._carregar_tarefas_salvas()

    def _remover_tarefa(self) -> None:
        itens = self.lista_tarefas.selectedItems()
        if not itens:
            self._mostrar_aviso("Selecione uma tarefa para remover.")
            return

        if not self._confirmar_remocao(len(itens)):
            return

        indices = sorted(
            {self.lista_tarefas.row(item) for item in itens},
            reverse=True,
        )

        tarefas: list[dict[str, Any]] = self.armazenamento.tarefas
        removidas: list[tuple[int, dict[str, Any]]] = []
        for indice in indices:
            if 0 <= indice < len(tarefas):
                removidas.append((indice, tarefas[indice]))
                tarefas.pop(indice)

        self.armazenamento.tarefas = tarefas
        self.armazenamento.salvar()
        self._ultima_remocao = sorted(removidas, key=lambda x: x[0])
        self._carregar_tarefas_salvas()
        self.lista_tarefas.setFocus()

    def _desfazer_ultima_remocao(self) -> None:
        if not self._ultima_remocao:
            return

        tarefas: list[dict[str, Any]] = self.armazenamento.tarefas
        titulos_atuais: set[str] = {str(t.get("titulo", "")).strip() for t in tarefas}

        restauradas = 0
        puladas = 0
        for indice, tarefa in self._ultima_remocao:
            titulo = str(tarefa.get("titulo", "")).strip()
            if not titulo:
                continue

            if titulo in titulos_atuais:
                puladas += 1
                continue

            pos = indice if 0 <= indice <= len(tarefas) else len(tarefas)
            tarefas.insert(pos, tarefa)
            titulos_atuais.add(titulo)
            restauradas += 1

        self._ultima_remocao = []
        self.armazenamento.tarefas = tarefas
        self.armazenamento.salvar()
        self._carregar_tarefas_salvas()

        if restauradas and puladas:
            self._mostrar_info(
                (
                    f"Desfez {restauradas} remoção(ões). {puladas} tarefa(s) não foram "
                    "restauradas por já existirem."
                )
            )
        elif restauradas:
            self._mostrar_info(f"Desfez {restauradas} remoção(ões).")

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

    def _alternar_status_tarefa(self, item: QListWidgetItem) -> None:
        # Mantém o duplo clique como atalho: alterna o checkbox.
        estado = item.checkState()
        item.setCheckState(Qt.Unchecked if estado == Qt.Checked else Qt.Checked)

    def _atualizar_estado_botoes(self) -> None:
        self.botao_remover.setEnabled(len(self.lista_tarefas.selectedItems()) > 0)
        self.botao_desfazer.setEnabled(bool(self._ultima_remocao))

    def _mostrar_aviso(self, mensagem: str) -> None:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle("Aviso")
        box.setText(mensagem)
        box.setStandardButtons(QMessageBox.Ok)
        style_message_box(box)
        box.exec_()

    def _mostrar_info(self, mensagem: str) -> None:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle("Informação")
        box.setText(mensagem)
        box.setStandardButtons(QMessageBox.Ok)
        style_message_box(box)
        box.exec_()

    def _confirmar_remocao(self, quantidade: int) -> bool:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle("Confirmar remoção")
        box.setText(
            "Tem certeza que deseja remover esta tarefa?"
            if quantidade == 1
            else f"Tem certeza que deseja remover {quantidade} tarefas?"
        )
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        box.setDefaultButton(QMessageBox.No)
        style_message_box(box)
        return box.exec_() == QMessageBox.Yes

    def _aplicar_estilo_conclusao(self, item: QListWidgetItem) -> None:
        fonte = item.font()
        fonte.setStrikeOut(item.checkState() == Qt.Checked)
        item.setFont(fonte)
