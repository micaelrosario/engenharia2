import json

from pathlib import Path

from src.services.simple_store import ArmazenamentoSimples


def test_inicia_vazio_quando_arquivo_nao_existe(tmp_path: Path) -> None:
    """Garante que inicia vazio se o arquivo não existir."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.tarefas == []


def test_adiciona_tarefa_e_salva(tmp_path: Path) -> None:
    """Verifica se adicionar() cria e salva a tarefa corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.adicionar("Comprar pão") is True

    tarefa = store.tarefas[0]
    assert tarefa == {"titulo": "Comprar pão", "feito": False}

    # Confirma que salvou no arquivo
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados == store.tarefas


def test_nao_adiciona_tarefa_vazia_ou_so_espacos(tmp_path: Path) -> None:
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)

    assert store.adicionar("   ") is False
    assert store.tarefas == []
    assert not caminho.exists()


def test_bloqueia_tarefas_duplicadas(tmp_path: Path) -> None:
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)

    assert store.adicionar("dormir") is True
    assert store.adicionar("dormir") is False
    assert store.tarefas == [{"titulo": "dormir", "feito": False}]


def test_limpa_registros_fantasmas_ao_carregar(tmp_path: Path) -> None:
    caminho = tmp_path / "tarefas.json"
    caminho.write_text(
        json.dumps(
            [
                {"titulo": "   ", "feito": False},
                {"titulo": "Ok", "feito": False},
                {"titulo": "\n\t", "feito": True},
            ],
            ensure_ascii=False,
            indent=4,
        ),
        encoding="utf-8",
    )

    store = ArmazenamentoSimples(caminho)
    assert store.tarefas == [{"titulo": "Ok", "feito": False}]

    # O arquivo também deve ser limpo para não manter "fantasmas".
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados == [{"titulo": "Ok", "feito": False}]


def test_remove_tarefa_da_lista(tmp_path: Path) -> None:
    """Verifica se remover() exclui a tarefa corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.adicionar("Estudar Python") is True

    store.remover(0)
    assert store.tarefas == []


def test_alternar_status_marca_e_desmarca(tmp_path: Path) -> None:
    """Verifica se alternar_status() muda o estado da tarefa."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.adicionar("Fazer exercícios") is True

    store.alternar_status(0)
    assert store.tarefas[0]["feito"]
    store.alternar_status(0)
    assert not store.tarefas[0]["feito"]


def test_salvar_e_carregar(tmp_path: Path) -> None:
    """Garante que salvar() e carregar() funcionam corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.adicionar("Ler um livro") is True

    assert caminho.exists()

    novo_store = ArmazenamentoSimples(caminho)
    assert novo_store.tarefas == [{"titulo": "Ler um livro", "feito": False}]


def test_carrega_arquivo_json_invalido(tmp_path: Path) -> None:
    caminho = tmp_path / "tarefas.json"
    caminho.write_text("{invalido_json}", encoding="utf-8")
    store = ArmazenamentoSimples(caminho)
    assert store.tarefas == []  # deve recomeçar vazio


def test_salvar_em_diretorio_invalido(tmp_path: Path) -> None:
    arquivo = tmp_path / "arquivo_invalido" / "tarefas.json"
    pasta_pai = arquivo.parent
    pasta_pai.mkdir()
    (pasta_pai / "arquivo_invalido").write_text(
        "conteudo",
        encoding="utf-8",
    )  # cria um arquivo no lugar do diretório

    store = ArmazenamentoSimples(arquivo)
    assert store.adicionar("Tarefa de teste") is True