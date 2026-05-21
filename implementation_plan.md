# Plano de Implementação: MVP do StudyFlow

Este documento detalha o plano de desenvolvimento para construir o sistema web StudyFlow (MVP) do zero, implementando as tecnologias e requisitos solicitados.

## User Review Required

> [!IMPORTANT]
> **Estilização (CSS):** Conforme as melhores práticas recomendadas para flexibilidade, planejamos utilizar **Vanilla CSS** (CSS puro / CSS Modules) para garantir um design exclusivo, moderno (glassmorphism, cores vibrantes) e responsivo. Se você preferir o uso de algum framework como TailwindCSS, por favor me avise antes de aprovarmos este plano.
> 
> **Diretório do Projeto:** O projeto será criado em `C:\Users\supor\.gemini\antigravity\scratch\StudyFlow`.

## Open Questions

> [!TIP]
> **Inteligência Artificial:** Para a funcionalidade de IA de "divisão de tarefas", como este é um MVP, podemos iniciar com um algoritmo heurístico (simulando a IA) que divide a tarefa baseado na "carga horária estimada" (ex: tarefas de > 2 horas são divididas em blocos de 1h), ou você prefere que já estruturemos uma chamada real para uma API de LLM (como OpenAI ou Google Gemini)?

## Proposed Changes

O projeto será dividido em dois diretórios principais: `backend` e `frontend`.

### Backend (FastAPI + SQLite)
Será construída uma API RESTful estruturada e escalável.

#### [NEW] `backend/main.py`
Ponto de entrada da aplicação, inicialização do FastAPI, configuração de CORS (para permitir o frontend) e inclusão das rotas.

#### [NEW] `backend/database.py`
Configuração de conexão com o SQLite usando SQLAlchemy, criando a `SessionLocal` e a base declarativa.

#### [NEW] `backend/models.py`
Definição das tabelas do banco de dados (ORM):
- `User`: id, email, password_hash
- `Subject`: id, name, color, user_id
- `Task`: id, title, status (pendente/concluída), estimated_minutes, user_id, subject_id

#### [NEW] `backend/schemas.py`
Modelos Pydantic para validação de entrada e saída de dados da API (ex: `UserCreate`, `TaskResponse`).

#### [NEW] `backend/auth.py`
Lógica de segurança: funções para criar o token JWT, validar o token em cada requisição e fazer o hash das senhas utilizando `passlib` (bcrypt).

#### [NEW] `backend/routers/`
Diretório contendo os endpoints organizados:
- `users.py`: `POST /register`, `POST /login`
- `subjects.py`: CRUD completo protegido por JWT.
- `tasks.py`: CRUD completo protegido por JWT, incluindo o endpoint que avalia a necessidade de divisão da tarefa (IA).

---

### Frontend (React + Vite)
Interface de usuário moderna, rápida e componentizada, comunicando-se com a API.

#### [NEW] `frontend/package.json`
Configuração do projeto gerado via Vite, com dependências como `axios` (para chamadas HTTP), `react-router-dom` (para navegação) e `lucide-react` (para ícones modernos).

#### [NEW] `frontend/src/services/api.js`
Configuração centralizada do Axios para interceptar requisições e injetar automaticamente o Token JWT no header `Authorization`.

#### [NEW] `frontend/src/index.css`
Arquivo de estilos globais contendo as variáveis do Design System (cores vibrantes, tipografia moderna) e utilitários para criar uma interface rica, responsiva e com micro-animações.

#### [NEW] `frontend/src/pages/`
- `Login.jsx`: Tela de autenticação.
- `Register.jsx`: Tela de criação de conta.
- `Dashboard.jsx`: Visão central com a barra de progresso, listas de matérias e gerenciamento de tarefas.

#### [NEW] `frontend/src/components/`
Componentes isolados e reutilizáveis:
- `ProgressBar.jsx`: Componente visual dinâmico do progresso diário/semanal.
- `TaskCard.jsx`: Card interativo para visualizar, editar e concluir tarefas.
- `SubjectModal.jsx`: Formulário para criar/editar matérias.

## Verification Plan

### Automated/Local Tests
1. **Ambiente Backend:** Iniciar o servidor uvicorn e validar todos os endpoints via Swagger UI (`http://localhost:8000/docs`).
2. **Ambiente Frontend:** Iniciar o servidor Vite (`npm run dev`) e testar a responsividade e renderização nos modos mobile e desktop simulados no navegador.

### Manual Verification
- **Fluxo Completo (E2E Manual):**
  1. Registrar um usuário e realizar login.
  2. Criar duas matérias.
  3. Criar tarefas com alta carga horária e verificar se o sistema (IA simulada ou real) propõe a divisão das tarefas em blocos.
  4. Marcar tarefas como concluídas e verificar se a Barra de Progresso no Dashboard é atualizada com transições suaves (design moderno).
- **Segurança:** Tentar acessar rotas de matérias/tarefas sem um Token JWT e verificar se o backend retorna status `401 Unauthorized`.
