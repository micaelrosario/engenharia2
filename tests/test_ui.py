import pytest
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QListWidget
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import Qt

# importa o módulo que estamos testando
import src.style as style


@pytest.fixture(scope="session")
def app():
    """Cria uma instância única de QApplication para os testes."""
    import sys
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    return app


# === Testes para estilo_botoes ===
def test_estilo_botoes_retorna_css():
    css = style.estilo_botoes()
    assert isinstance(css, str)
    assert "QPushButton" in css
    assert "background-color" in css


# === Testes para paleta_escura ===
def test_paleta_escura_retorna_qpalette():
    paleta = style.paleta_escura()
    assert isinstance(paleta, QPalette)
    assert paleta.color(QPalette.Window).name() in ("#1e1e1e", "#1e1e1e")


# === Testes para apply_app_style ===
def test_apply_app_style_aplica_paleta_e_fonte(app):
    style.apply_app_style(app, base_font_pt=12)
    font = app.font()
    assert isinstance(font, QFont)
    assert font.pointSize() == 12


# === Testes para style_buttons ===
def test_style_buttons_aplica_estilos(app):
    btn1 = QPushButton("Botão 1")
    btn2 = QPushButton("Botão 2")
    style.style_buttons([btn1, btn2])

    for btn in (btn1, btn2):
        assert btn.minimumHeight() == 44
        assert isinstance(btn.font(), QFont)
        assert "QPushButton" in btn.styleSheet()


# === Testes para style_task_input ===
def test_style_task_input_aplica_altura_e_fonte(app):
    inp = QLineEdit()
    style.style_task_input(inp)
    assert inp.height() == 44
    assert isinstance(inp.font(), QFont)
    assert inp.font().pointSize() == 14


# === Testes para style_task_list ===
def test_style_task_list_aplica_estilo_e_fonte(app):
    lst = QListWidget()
    style.style_task_list(lst, font_pt=15, item_height=38, bg_color="#fafafa")

    f = lst.font()
    assert f.pointSize() == 15
    css = lst.styleSheet()
    assert "QListWidget" in css
    assert "background: #fafafa" in css
    assert "height: 38px" in css
