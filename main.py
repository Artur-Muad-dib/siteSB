from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3
from pydantic import BaseModel
from urllib.parse import unquote

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitações de todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

class LoginRequest(BaseModel):
    cpf: str
    senha: str

@app.post("/login")
def login(request: LoginRequest):
    conn = sqlite3.connect("PCD.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE cpf = ? AND senha = ?", (request.cpf, request.senha)
    )
    user = c.fetchone()

    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail=" CPF ou senha incorretos")


@app.get("/dados")
def read_data(
    sexo: Optional[str] = None,
    tipo_defic: Optional[str] = None,
    idade_min: Optional[int] = None,
    idade_max: Optional[int] = None,
    n_bairro_a: Optional[str] = None,
):
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()

    params = []
    sql = "SELECT * FROM my_table"

    if sexo:
        sql += " WHERE sexo = ?"
        params.append(sexo)

    if tipo_defic:
        sql += (params and " AND" or " WHERE") + " tipo_defic = ?"
        params.append(tipo_defic)

    if idade_min is not None:
        sql += (params and " AND" or " WHERE") + " idade >= ?"
        params.append(idade_min)

    if idade_max is not None:
        sql += (params and " AND" or " WHERE") + " idade <= ?"
        params.append(idade_max)

    if n_bairro_a and n_bairro_a != "undefined":
        n_bairro_a = unquote(n_bairro_a)
        print(f"n_bairro_a: {n_bairro_a}")  # Debug print
        sql += (params and " AND" or " WHERE") + " n_bairro_a = ?"
        params.append(n_bairro_a)
        print(f"SQL query: {sql}")  # Debug print

    c.execute(sql, params)
    rows = c.fetchall()

    return {"data": rows}


@app.get("/bairros")
def get_bairros():
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()

    c.execute("SELECT DISTINCT n_bairro_a FROM my_table")
    bairros = c.fetchall()

    return {"bairros": bairros}


@app.get("/ponibus")
def get_ponibus():
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()

    c.execute("SELECT geometry FROM ponibus")
    rows = c.fetchall()

    return {"data": rows}


