from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal

# Cria as tabelas no MySQL automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API com FastAPI e SQLAlchemy")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=201)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    # 1. Cria o perfil
    novo_perfil = models.Perfil(perfil_nome=usuario.perfil.perfil_nome)
    db.add(novo_perfil)
    db.commit()
    db.refresh(novo_perfil)

    # 2. Cria o usuário com o ID do perfil
    novo_usuario = models.Usuario(
        nome=usuario.nome, email=usuario.email, 
        senha=usuario.senha, id_perfil=novo_perfil.id
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario

@app.get("/usuarios", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@app.put("/usuarios/{id}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(id: int, dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Atualiza os dados do usuário
    usuario_db.nome = dados.nome
    usuario_db.email = dados.email
    usuario_db.senha = dados.senha
    
    # Atualiza os dados do perfil aninhado
    usuario_db.perfil.perfil_nome = dados.perfil.perfil_nome
    
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@app.delete("/usuarios/{id}")
def deletar_usuario(id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Salva o ID do perfil antes de deletar o usuário
    perfil_id = usuario_db.id_perfil
    
    # Deleta o usuário primeiro (por causa da chave estrangeira)
    db.delete(usuario_db) 
    
    # Busca e deleta o perfil que ficou órfão
    perfil_db = db.query(models.Perfil).filter(models.Perfil.id == perfil_id).first()
    if perfil_db:
        db.delete(perfil_db) 
        
    db.commit()
    return {"mensagem": "Usuário e perfil deletados com sucesso"}