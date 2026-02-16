import json
from src.services.simple_store import ArmazenamentoSimples



def test_inicia_vazio_quando_arquivo_nao_existe(tmp_path):
    """Garante que inicia vazio se o arquivo não existir."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.tarefas == []


def test_adiciona_tarefa_e_salva(tmp_path):
    """Verifica se adicionar() cria e salva a tarefa corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Comprar pão")

    tarefa = store.tarefas[0]
    assert tarefa == {"titulo": "Comprar pão", "feito": False}

    # Confirma que salvou no arquivo
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados == store.tarefas


def test_remove_tarefa_da_lista(tmp_path):
    """Verifica se remover() exclui a tarefa corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Estudar Python")

    store.remover(0)
    assert store.tarefas == []


def test_alternar_status_marca_e_desmarca(tmp_path):
    """Verifica se alternar_status() muda o estado da tarefa."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Fazer exercícios")

    store.alternar_status(0)
    assert store.tarefas[0]["feito"]
    store.alternar_status(0)
    assert not store.tarefas[0]["feito"]


def test_salvar_e_carregar(tmp_path):
    """Garante que salvar() e carregar() funcionam corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Ler um livro")

    assert caminho.exists()

    novo_store = ArmazenamentoSimples(caminho)
    assert novo_store.tarefas == [{"titulo": "Ler um livro", "feito": False}]

def test_carrega_arquivo_json_invalido(tmp_path):
    caminho = tmp_path / "tarefas.json"
    caminho.write_text("{invalido_json}", encoding="utf-8")
    store = ArmazenamentoSimples(caminho)
    assert store.tarefas == []  # deve recomeçar vazio

def test_salvar_em_diretorio_invalido(tmp_path):
    arquivo = tmp_path / "arquivo_invalido" / "tarefas.json"
    pasta_pai = arquivo.parent
    pasta_pai.mkdir()
    (pasta_pai / "arquivo_invalido").write_text(
        "conteudo",
        encoding="utf-8",
    )  # cria um arquivo no lugar do diretório

    store = ArmazenamentoSimples(arquivo)
    store.adicionar("Tarefa de teste")