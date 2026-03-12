from __future__ import annotations

from typing import Sequence

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QStyleFactory,
    QWidget,
)


# === Tokens de tema (escuro + acento azul) ===
# Mantém Window=#1e1e1e (coberto por testes).
COLOR_BG = "#1e1e1e"
COLOR_SURFACE = "#2b2f3a"
COLOR_SURFACE_HOVER = "#343b4a"
COLOR_BORDER = "#3b4252"

COLOR_TEXT = "#f8fafc"
COLOR_TEXT_DISABLED = "#94a3b8"

COLOR_ACCENT = "#3b82f6"
COLOR_ACCENT_HOVER = "#2563eb"
COLOR_ACCENT_PRESSED = "#1d4ed8"
COLOR_ACCENT_SOFT_HOVER = "#eff6ff"
COLOR_ACCENT_SOFT_SELECTED = "#dbeafe"
COLOR_ACCENT_SOFT_ACTIVE = "#bfdbfe"

COLOR_INPUT_BG = "#111827"
COLOR_INPUT_BORDER = "#334155"
COLOR_LIST_BORDER = "#d1d5db"


# === Estilo dos botões com efeito hover ===
def estilo_botoes() -> str:
    """Retorna o stylesheet padrão de botões do app."""
    return f"""
        QPushButton {{
            background-color: {COLOR_SURFACE};
            color: {COLOR_TEXT};
            border: 1px solid {COLOR_BORDER};
            border-radius: 10px;
            padding: 10px 14px;
            min-height: 40px;
            font-size: 13pt;
        }}
        QPushButton:hover {{
            background-color: {COLOR_SURFACE_HOVER};
            border: 1px solid {COLOR_ACCENT};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_BORDER};
        }}
        QPushButton:focus {{
            border: 1px solid {COLOR_ACCENT};
        }}
        QPushButton:disabled {{
            background-color: {COLOR_BG};
            color: {COLOR_TEXT_DISABLED};
            border: 1px solid {COLOR_BORDER};
        }}

        QPushButton[variant="primary"] {{
            background-color: {COLOR_ACCENT};
            border: 1px solid {COLOR_ACCENT};
            color: white;
        }}
        QPushButton[variant="primary"]:hover {{
            background-color: {COLOR_ACCENT_HOVER};
            border: 1px solid {COLOR_ACCENT_HOVER};
        }}
        QPushButton[variant="primary"]:pressed {{
            background-color: {COLOR_ACCENT_PRESSED};
            border: 1px solid {COLOR_ACCENT_PRESSED};
        }}
    """


# === Paleta de cores para tema escuro ===
def paleta_escura() -> QPalette:
    paleta = QPalette()
    paleta.setColor(QPalette.Window, QColor(30, 30, 30))  # Cor do fundo da janela
    paleta.setColor(QPalette.WindowText, Qt.white)  # Cor do texto geral
    paleta.setColor(
        QPalette.Base,
        QColor(COLOR_INPUT_BG),
    )  # Fundo dos campos de texto
    paleta.setColor(
        QPalette.Text,
        Qt.white,
    )  # Texto digitado nos campos
    paleta.setColor(QPalette.Button, QColor(COLOR_SURFACE))  # Cor dos botões
    paleta.setColor(QPalette.ButtonText, Qt.white)  # Texto dos botões
    paleta.setColor(
        QPalette.Highlight,
        QColor(COLOR_ACCENT),
    )  # Cor de destaque (seleção)
    paleta.setColor(QPalette.HighlightedText, Qt.white)  # Texto em destaque
    return paleta


# === Aplica tema global e fonte base ===
def apply_app_style(app: QApplication | None, base_font_pt: int = 11) -> None:
    """Aplica paleta e fonte global à aplicação Qt."""
    if not app:
        raise ValueError("Objeto 'app' inválido: aplicação Qt não fornecida.")

    # Garante widgets consistentes e que respeitam a paleta (evita diálogos nativos
    # com contraste ruim em alguns ambientes).
    fusion = QStyleFactory.create("Fusion")
    app.setStyle(fusion)

    f = QFont()
    f.setPointSize(base_font_pt)
    app.setFont(f)

    paleta = paleta_escura()
    app.setPalette(paleta)


def style_message_box(box: QMessageBox | None) -> None:
    """Aplica um estilo legível para QMessageBox baseado na paleta do app."""
    if box is None:
        return

    box.setStyleSheet(
        "".join(
            [
                "QMessageBox { background: palette(window); }",
                "QLabel { color: palette(window-text); }",
                estilo_botoes(),
            ]
        )
    )


# === Aplica estilo consistente aos botões ===
def style_buttons(
    buttons: Sequence[QWidget | None] | None,
    min_height: int = 44,
    font_pt: int = 13,
) -> None:
    """Aplica estilo consistente a uma lista de botões."""
    if not buttons:
        return

    for b in buttons:
        if b is None:
            continue
        bf = b.font() or QFont()
        bf.setPointSize(font_pt)
        b.setFont(bf)
        b.setMinimumHeight(min_height)
        b.setStyleSheet(estilo_botoes())


# === Estilo do campo de entrada de tarefas ===
def style_task_input(
    inp: QLineEdit | None,
    height: int = 44,
    font_pt: int = 14,
) -> None:
    """Aplica altura e fonte ao campo de entrada."""
    if inp is None:
        return

    inp.setFixedHeight(height)
    f = inp.font() or QFont()
    f.setPointSize(font_pt)
    inp.setFont(f)

    inp.setStyleSheet(
        f"""
        QLineEdit {{
            background-color: {COLOR_INPUT_BG};
            color: {COLOR_TEXT};
            border: 1px solid {COLOR_INPUT_BORDER};
            border-radius: 10px;
            padding: 10px 12px;
        }}
        QLineEdit:focus {{
            border: 1px solid {COLOR_ACCENT};
        }}
        QLineEdit::placeholder {{
            color: {COLOR_TEXT_DISABLED};
        }}
        """
    )


# === Estilo da lista de tarefas ===
def style_task_list(
    lst: QListWidget | None,
    font_pt: int = 13,
    item_height: int = 36,
    bg_color: str = "#f8fafc",
):
    """Aplica estilo visual à lista de tarefas."""
    if lst is None:
        return

    f = lst.font() or QFont()
    f.setPointSize(font_pt)
    lst.setFont(f)

    # Mantém a lista legível mesmo em tema escuro: fundo claro + texto escuro.
    # (A paleta global pode definir Text como branco.)
    p = lst.palette()
    p.setColor(QPalette.Base, QColor(bg_color))
    p.setColor(QPalette.Text, Qt.black)
    p.setColor(QPalette.HighlightedText, Qt.black)
    lst.setPalette(p)

    # padding e cor de fundo (personalizável)
    lst.setStyleSheet(
        f"""
        QListWidget {{
            padding: 8px;
            background: {bg_color};
            border: 1px solid {COLOR_LIST_BORDER};
            border-radius: 12px;
            outline: none;
        }}
        QListWidget::item {{
            padding: 10px 10px;
            height: {item_height}px;
            color: black;
            border-radius: 10px;
            margin: 4px 0px;
        }}
        QListWidget::item:hover {{
            background: {COLOR_ACCENT_SOFT_HOVER};
        }}
        QListWidget::item:selected {{
            background: {COLOR_ACCENT_SOFT_SELECTED};
            color: black;
        }}
        QListWidget::item:selected:active {{
            background: {COLOR_ACCENT_SOFT_ACTIVE};
        }}
        QListWidget::item:focus {{
            outline: none;
        }}
        """
    )
