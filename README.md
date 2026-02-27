## README: Python + FastAPI + SQLAlchemy

# API de Usuários - FastAPI & SQLAlchemy

Implementação de API de alta performance utilizando **Python** e **FastAPI**, focando no gerenciamento manual de sessões e transações de banco de dados com **SQLAlchemy**.

## Tecnologias
* Python 3.x
* FastAPI
* SQLAlchemy (ORM)
* Pydantic (Validação de dados)

##  Lógica de Transação
Diferente de outros ORMs, aqui a transação é gerenciada explicitamente. O `Perfil` é criado primeiro para gerar o ID necessário para a chave estrangeira do `Usuario`, ambos dentro do mesmo contexto de sessão:

```python
novo_perfil = models.Perfil(perfil_nome=usuario.perfil.perfil_nome)
db.add(novo_perfil)
db.flush() # Gera o ID do perfil antes do commit final

novo_usuario = models.Usuario(..., id_perfil=novo_perfil.id)
db.add(novo_usuario)
db.commit()
```
Como Executar:
1. Crie o ambiente virtual: `python -m venv venv`

2. Ative o venv e instale: `pip install fastapi uvicorn sqlalchemy`

3. Inicie o servidor: `uvicorn main:app --reload`
