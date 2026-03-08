import pytest
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QListWidget
from PyQt5.QtGui import QFont, QPalette

# importa o módulo que estamos testando
from src import style

BASE_FONT_PT = 12
BUTTON_MIN_HEIGHT = 44
TASK_INPUT_HEIGHT = 44
TASK_INPUT_FONT_PT = 14
TASK_LIST_FONT_PT = 15


@pytest.fixture(scope="session")
def app() -> QApplication:
    """Cria uma instância única de QApplication para os testes."""
    import sys
    app_instance = QApplication.instance()
    if app_instance is None:
        return QApplication(sys.argv)

    if not isinstance(app_instance, QApplication):
        raise RuntimeError("Instância Qt existente não é QApplication.")

    return app_instance


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
def test_apply_app_style_aplica_paleta_e_fonte(app: QApplication) -> None:
    style.apply_app_style(app, base_font_pt=BASE_FONT_PT)
    font = app.font()
    assert isinstance(font, QFont)
    assert font.pointSize() == BASE_FONT_PT


# === Testes para style_buttons ===
def test_style_buttons_aplica_estilos(app: QApplication) -> None:
    btn1 = QPushButton("Botão 1")
    btn2 = QPushButton("Botão 2")
    style.style_buttons([btn1, btn2])

    for btn in (btn1, btn2):
        assert btn.minimumHeight() == BUTTON_MIN_HEIGHT
        assert isinstance(btn.font(), QFont)
        assert "QPushButton" in btn.styleSheet()


# === Testes para style_task_input ===
def test_style_task_input_aplica_altura_e_fonte(app: QApplication) -> None:
    inp = QLineEdit()
    style.style_task_input(inp)
    assert inp.height() == TASK_INPUT_HEIGHT
    assert isinstance(inp.font(), QFont)
    assert inp.font().pointSize() == TASK_INPUT_FONT_PT


# === Testes para style_task_list ===
def test_style_task_list_aplica_estilo_e_fonte(app: QApplication) -> None:
    lst = QListWidget()
    style.style_task_list(
        lst,
        font_pt=TASK_LIST_FONT_PT,
        item_height=38,
        bg_color="#fafafa",
    )

    f = lst.font()
    assert f.pointSize() == TASK_LIST_FONT_PT
    css = lst.styleSheet()
    assert "QListWidget" in css
    assert "background: #fafafa" in css
    assert "height: 38px" in css
