from pydantic import BaseModel

class PerfilCreate(BaseModel):
    perfil_nome: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    perfil: PerfilCreate 

class PerfilResponse(BaseModel):
    id: int
    perfil_nome: str
    model_config = {"from_attributes": True}

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    id_perfil: int
    perfil: PerfilResponse 
    model_config = {"from_attributes": True}