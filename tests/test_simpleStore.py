import json
from src.todoList import ArmazenamentoSimples


# ----------------------------
# Testes da classe ArmazenamentoSimples
# ----------------------------

def test_inicia_vazio_quando_arquivo_nao_existe(tmp_path):
    """Verifica se o armazenamento inicia vazio quando o arquivo não existe."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    assert store.tarefas == []


def test_adiciona_tarefa_e_salva(tmp_path):
    """Testa se adicionar() cria uma nova tarefa e salva corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Comprar pão")
    
    assert len(store.tarefas) == 1
    tarefa = store.tarefas[0]
    assert tarefa["titulo"] == "Comprar pão"
    assert not tarefa["feito"]

    # Verifica se salvou no arquivo
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados[0]["titulo"] == "Comprar pão"


def test_remove_tarefa_da_lista(tmp_path):
    """Testa se remover() realmente exclui uma tarefa existente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Estudar Python")
    
    assert len(store.tarefas) == 1
    store.remover(0)
    assert store.tarefas == []


def test_alternar_status_marca_e_desmarca(tmp_path):
    """Verifica se alternar_status() muda o estado 'feito' corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Fazer exercícios")
    
    assert not store.tarefas[0]["feito"]
    store.alternar_status(0)
    assert store.tarefas[0]["feito"]
    store.alternar_status(0)
    assert not store.tarefas[0]["feito"]


def test_salvar_e_carregar(tmp_path):
    """Verifica se salvar() e carregar() funcionam corretamente."""
    caminho = tmp_path / "tarefas.json"
    store = ArmazenamentoSimples(caminho)
    store.adicionar("Ler um livro")

    # Verifica que o arquivo foi criado
    assert caminho.exists()

    # Cria nova instância e carrega do arquivo
    novo_store = ArmazenamentoSimples(caminho)
    assert len(novo_store.tarefas) == 1
    assert novo_store.tarefas[0]["titulo"] == "Ler um livro"
    assert not novo_store.tarefas[0]["feito"]

