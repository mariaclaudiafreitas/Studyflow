# 📚 StudyFlow — Sistema Inteligente de Organização de Estudos

> Plataforma web para gerenciamento de matérias, tarefas e progresso acadêmico, com IA heurística para divisão de carga de estudo.

---

## 🎯 Descrição

O **StudyFlow** é uma aplicação web full-stack que centraliza o planejamento de estudos do estudante. Com ele, o usuário gerencia matérias, cria tarefas, acompanha o progresso semanal e conta com uma IA heurística que divide automaticamente tarefas longas em blocos otimizados de estudo.

---

## 🛠 Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Frontend | React 18 + Vite |
| Estilização | Vanilla CSS (Glassmorphism) |
| HTTP Client | Axios |
| Roteamento | React Router DOM 6 |
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Banco de Dados | SQLite 3 |
| Autenticação | JWT (python-jose) + bcrypt (passlib) |
| Validação | Pydantic |

---

## 🏗 Arquitetura

```
┌─────────────────────┐     REST + JWT      ┌──────────────────────┐
│  Frontend (React)   │ ──────────────────► │  Backend (FastAPI)   │
│  porta :5173        │ ◄────────────────── │  porta :8000         │
└─────────────────────┘                     └──────────┬───────────┘
                                                       │ SQLAlchemy ORM
                                            ┌──────────▼───────────┐
                                            │  SQLite (studyflow.db)│
                                            └──────────────────────┘
```

**Padrão:** SPA desacoplada comunicando-se com API REST. Frontend nunca acessa o banco diretamente.

---

## 📁 Estrutura de Pastas

```
StudyFlow/
├── backend/
│   ├── main.py           # Inicialização FastAPI + CORS
│   ├── database.py       # Configuração SQLAlchemy + SQLite
│   ├── models.py         # Modelos ORM: User, Subject, Task
│   ├── schemas.py        # Schemas Pydantic (request/response)
│   ├── auth.py           # JWT + bcrypt
│   ├── studyflow.db      # Banco de dados SQLite
│   └── routers/
│       ├── users.py      # /users/register, /users/login
│       ├── subjects.py   # CRUD /subjects
│       └── tasks.py      # CRUD /tasks + IA heurística
│
└── frontend/
    ├── src/
    │   ├── App.jsx           # Roteamento SPA
    │   ├── main.jsx          # Entry point React
    │   ├── index.css         # Design system Glassmorphism
    │   ├── services/api.js   # Axios + interceptor JWT
    │   └── pages/
    │       ├── Login.jsx
    │       ├── Register.jsx
    │       └── Dashboard.jsx
    └── package.json
```

---

## ▶️ Instruções de Execução

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- npm

### 1. Backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] pydantic[email]
uvicorn main:app --reload
```

- API disponível em: `http://localhost:8000`
- Swagger UI (documentação interativa): `http://localhost:8000/docs`

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev
```

- Interface disponível em: `http://localhost:5173`

### 3. Atalho Windows

Execute `run.bat` na raiz do projeto para iniciar ambos automaticamente.

---

## 🔐 Variáveis de Ambiente (Produção)

> Em desenvolvimento, as variáveis estão no código. Em produção, use um arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta-forte-aqui
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///./studyflow.db
```

---

## 🤖 Funcionalidade de IA

Ao criar uma tarefa com **mais de 120 minutos estimados**, o backend divide automaticamente em blocos de 60 minutos. As subtarefas geradas pela IA aparecem com o ícone ✨ no dashboard.

**Exemplo:** Tarefa de 150 min → 3 subtarefas (60 + 60 + 30 min)

---

## 📋 Endpoints Principais

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/users/register` | Criar conta | ❌ |
| POST | `/users/login` | Login (retorna JWT) | ❌ |
| GET | `/subjects/` | Listar matérias | ✅ |
| POST | `/subjects/` | Criar matéria | ✅ |
| PUT | `/subjects/{id}` | Editar matéria | ✅ |
| DELETE | `/subjects/{id}` | Deletar matéria | ✅ |
| GET | `/tasks/` | Listar tarefas | ✅ |
| POST | `/tasks/` | Criar tarefa (+ IA) | ✅ |
| PUT | `/tasks/{id}` | Atualizar tarefa | ✅ |
| DELETE | `/tasks/{id}` | Deletar tarefa | ✅ |

---
PS C:\Users\supor\Study_Flow> .\run.bat                                                                
=========================================
   INICIANDO AMBIENTE STUDYFLOW
=========================================

[1] Iniciando Backend FastAPI na porta 8000...
[2] Iniciando Frontend React (Vite) na porta 5173...

Os servidores foram abertos em novas janelas!

Para testar, abra no seu navegador:
Frontend (Telas): http://localhost:5173
Backend (Documentacao API): http://localhost:8000/docs

## 👥 Equipe
Maria Claudia Freitas

Projeto desenvolvido para a disciplina **Métodos e Aplicações de IA** — 2026.
