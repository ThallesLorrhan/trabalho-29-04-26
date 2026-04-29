from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE - Criar tarefa
@app.post("/tarefas", response_model=schemas.TarefaResponse)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = models.Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa


# READ - Listar todas
@app.get("/tarefas", response_model=list[schemas.TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.Tarefa).all()


# READ - Buscar por ID
@app.get("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return tarefa


# UPDATE - Atualizar tarefa
@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: schemas.TarefaCreate, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa.titulo = dados.titulo
    tarefa.descricao = dados.descricao

    db.commit()
    db.refresh(tarefa)

    return tarefa


# DELETE - Deletar tarefa
@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()

    return {"mensagem": "Tarefa deletada com sucesso"}