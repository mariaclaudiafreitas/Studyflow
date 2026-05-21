# PRD — StudyFlow

**Documento:** Product Requirements Document (PRD)
**Produto:** StudyFlow — Sistema Inteligente de Organização de Estudos
**Versão:** 1.0 (MVP)
**Autor:** Equipe de Produto & Engenharia
**Data:** 2026-05-20
**Status:** Aprovado para desenvolvimento

---

## 1. Visão Geral

### 1.1 Nome
**StudyFlow** — Plataforma web inteligente para organização da rotina acadêmica de estudantes.

### 1.2 Objetivo
Oferecer aos estudantes uma ferramenta centralizada para planejar matérias, gerenciar tarefas, definir metas e acompanhar o progresso semanal, com apoio de Inteligência Artificial para otimizar a distribuição da carga de estudos.

### 1.3 Problema que resolve
Estudantes frequentemente perdem produtividade por:
- Dispersão de informações em múltiplas ferramentas (papel, planilhas, apps genéricos);
- Dificuldade em estimar e distribuir carga horária de estudo;
- Falta de visibilidade sobre o progresso real ao longo da semana;
- Sobrecarga cognitiva ao lidar com muitas tarefas simultâneas, levando à procrastinação.

StudyFlow centraliza o planejamento, mede o progresso de forma visual e usa IA para **quebrar tarefas pesadas em blocos otimizados de estudo**, reduzindo o atrito cognitivo.

### 1.4 Público-alvo
- **Primário:** Estudantes universitários (graduação) entre 18 e 30 anos.
- **Secundário:** Estudantes de cursinhos pré-vestibular, concursos e pós-graduação.
- **Perfil:** Familiarizado com ferramentas digitais, busca produtividade e autodisciplina.

### 1.5 Proposta de Valor
> "Organize, execute e evolua nos estudos — com a ajuda de uma IA que entende quando você está sobrecarregado."

---

## 2. Funcionalidades

### 2.1 Escopo do MVP (Versão 1.0)

| ID | Funcionalidade | Descrição |
|----|----------------|-----------|
| F01 | Cadastro de usuário | Registro com nome, e-mail e senha (hash bcrypt). |
| F02 | Login / Logout | Autenticação via JWT, sessão segura. |
| F03 | Dashboard geral | Visão consolidada: tarefas do dia, progresso semanal, matérias ativas. |
| F04 | CRUD de Matérias | Criar, listar, editar e excluir matérias (nome, cor, carga horária semanal). |
| F05 | CRUD de Tarefas | Criar, listar, editar e excluir tarefas vinculadas a uma matéria. |
| F06 | Controle de status | Marcar tarefa como `pendente` ou `concluída`. |
| F07 | Barra de progresso | Indicador visual de % de tarefas concluídas na semana. |
| F08 | **IA — Divisão de tarefas** | Quando o usuário acumula muitas tarefas ou alta carga horária, o sistema sugere automaticamente a divisão em blocos menores de estudo (ex.: Pomodoros de 25–50min). |

### 2.2 Funcionalidades Futuras (Pós-MVP)

| Versão | Funcionalidade |
|--------|----------------|
| 1.1 | Notificações por e-mail e push (lembretes de tarefas). |
| 1.2 | Integração com Google Calendar. |
| 1.3 | Estatísticas avançadas (heatmap de produtividade, melhores horários). |
| 1.4 | Gamificação (XP, conquistas, streaks). |
| 1.5 | Modo colaborativo (grupos de estudo). |
| 2.0 | IA conversacional (chat tutor que recomenda materiais e revisões espaçadas). |
| 2.1 | Aplicativo mobile (React Native). |

---

## 3. Requisitos

### 3.1 Requisitos Funcionais (RF)

| ID | Requisito |
|----|-----------|
| RF01 | O usuário deve poder se cadastrar com e-mail e senha. |
| RF02 | O usuário deve poder autenticar-se e receber um token JWT. |
| RF03 | O sistema deve invalidar sessões expiradas (token TTL configurável). |
| RF04 | O usuário autenticado deve poder criar, listar, editar e excluir suas matérias. |
| RF05 | O usuário autenticado deve poder criar, listar, editar e excluir suas tarefas. |
| RF06 | Cada tarefa deve pertencer obrigatoriamente a uma matéria do próprio usuário. |
| RF07 | O usuário deve poder alternar o status da tarefa entre `pendente` e `concluída`. |
| RF08 | O dashboard deve exibir o percentual de tarefas concluídas na semana corrente. |
| RF09 | O sistema deve detectar sobrecarga (ex.: >10 tarefas pendentes ou >20h estimadas na semana) e sugerir divisão em blocos via IA. |
| RF10 | O usuário deve poder aceitar ou recusar a sugestão da IA. |
| RF11 | Rotas de API que manipulam dados do usuário devem ser protegidas por JWT. |

### 3.2 Requisitos Não Funcionais (RNF)

| ID | Categoria | Requisito |
|----|-----------|-----------|
| RNF01 | Desempenho | Respostas da API < 300ms (p95) em operações CRUD. |
| RNF02 | Desempenho | Time-to-interactive do frontend < 2s em conexão 4G. |
| RNF03 | Responsividade | UI 100% responsiva (mobile-first, breakpoints sm/md/lg/xl). |
| RNF04 | Segurança | Senhas armazenadas com hash bcrypt (cost ≥ 12). |
| RNF05 | Segurança | Proteção contra SQL Injection via ORM (SQLAlchemy / Prisma). |
| RNF06 | Segurança | CORS restrito ao domínio do frontend em produção. |
| RNF07 | Segurança | Tokens JWT assinados com chave secreta forte (env var), TTL ≤ 24h. |
| RNF08 | Segurança | Validação rigorosa de input (Pydantic/Zod). |
| RNF09 | Segurança | Rate limiting nas rotas de autenticação (anti brute-force). |
| RNF10 | Acessibilidade | Contraste WCAG AA, navegação por teclado, ARIA labels. |
| RNF11 | Manutenibilidade | Cobertura de testes ≥ 70% no backend. |
| RNF12 | Observabilidade | Logs estruturados (JSON) e tracking básico de erros. |
| RNF13 | Portabilidade | Banco SQLite no MVP, com camada ORM permitindo migração futura para PostgreSQL. |

---

## 4. Arquitetura Proposta

### 4.1 Visão Geral
Arquitetura **cliente-servidor desacoplada**, com clara separação entre apresentação e domínio.

```text
┌─────────────────────┐         HTTPS / JSON          ┌──────────────────────┐
│   Frontend (SPA)    │ ───────────────────────────►  │   Backend (API)      │
│   React + Vite      │   REST + JWT (Bearer Token)   │   FastAPI (Python)   │
│   TailwindCSS       │ ◄───────────────────────────  │   ou NestJS (Node)   │
└─────────────────────┘                                └──────────┬───────────┘
                                                                  │
                                                       SQLAlchemy / Prisma ORM
                                                                  │
                                                       ┌──────────▼───────────┐
                                                       │   SQLite (file DB)   │
                                                       └──────────────────────┘
                                                                  │
                                                       ┌──────────▼───────────┐
                                                       │   IA Service Module  │
                                                       │ (heurística + LLM    │
                                                       │  opcional via API)   │
                                                       └──────────────────────┘
```

### 4.2 Camadas

**Frontend (React + Vite):**
- SPA com roteamento client-side (React Router).
- Gerenciamento de estado: React Query (server state) + Zustand/Context (UI state).
- Estilo: TailwindCSS, componentes acessíveis (shadcn/ui).
- Comunicação com backend via `fetch`/`axios`, com interceptor anexando o JWT.

**Backend (FastAPI — recomendado, ou NestJS):**
- Camada **Router/Controller**: define endpoints REST.
- Camada **Service**: regras de negócio (incluindo módulo de IA).
- Camada **Repository**: acesso a dados via ORM (SQLAlchemy).
- Camada **Schema**: validação com Pydantic.
- Middleware de autenticação JWT em rotas protegidas.

**Banco (SQLite):**
- Arquivo `studyflow.db`.
- Migrations via Alembic.
- Pronto para evoluir a PostgreSQL trocando apenas a connection string.

**Módulo de IA:**
- **Fase 1 (MVP):** heurística local — detecta sobrecarga e divide tarefas com duração > X min em blocos de 25/50min (Pomodoro), respeitando intervalos.
- **Fase 2:** integração com LLM (ex.: OpenAI/Lovable AI Gateway) para sugestões contextuais.

### 4.3 Endpoints REST principais

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/register` | Cria conta | Não |
| POST | `/auth/login` | Retorna JWT | Não |
| GET  | `/me` | Dados do usuário logado | Sim |
| GET  | `/subjects` | Lista matérias | Sim |
| POST | `/subjects` | Cria matéria | Sim |
| PUT  | `/subjects/{id}` | Atualiza matéria | Sim |
| DELETE | `/subjects/{id}` | Remove matéria | Sim |
| GET  | `/tasks` | Lista tarefas (filtros: status, semana) | Sim |
| POST | `/tasks` | Cria tarefa | Sim |
| PUT  | `/tasks/{id}` | Atualiza tarefa | Sim |
| PATCH | `/tasks/{id}/status` | Alterna status | Sim |
| DELETE | `/tasks/{id}` | Remove tarefa | Sim |
| GET  | `/dashboard/progress` | Progresso semanal | Sim |
| POST | `/ai/suggest-split` | Sugere divisão em blocos | Sim |

---

## 5. Modelo de Dados

### 5.1 Diagrama de Entidades

```text
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│   users       │ 1     N │   subjects    │ 1     N │    tasks      │
├───────────────┤────────►├───────────────┤────────►├───────────────┤
│ id (PK)       │         │ id (PK)       │         │ id (PK)       │
│ name          │         │ user_id (FK)  │         │ subject_id(FK)│
│ email (uniq)  │         │ name          │         │ user_id (FK)  │
│ password_hash │         │ color         │         │ title         │
│ created_at    │         │ weekly_hours  │         │ description   │
└───────────────┘         │ created_at    │         │ status        │
                          └───────────────┘         │ estimated_min │
                                                    │ due_date      │
                                                    │ created_at    │
                                                    │ updated_at    │
                                                    └───────────────┘
                                                            │
                                                            │ 1
                                                            ▼ N
                                                  ┌───────────────────┐
                                                  │  study_blocks     │
                                                  ├───────────────────┤
                                                  │ id (PK)           │
                                                  │ task_id (FK)      │
                                                  │ order             │
                                                  │ duration_min      │
                                                  │ scheduled_at      │
                                                  │ done (bool)       │
                                                  └───────────────────┘
```

### 5.2 Tabelas

**users**
| Campo | Tipo | Restrições |
|-------|------|------------|
| id | INTEGER | PK, autoincrement |
| name | TEXT | NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| password_hash | TEXT | NOT NULL (bcrypt) |
| created_at | DATETIME | DEFAULT now() |

**subjects**
| Campo | Tipo | Restrições |
|-------|------|------------|
| id | INTEGER | PK |
| user_id | INTEGER | FK → users.id, ON DELETE CASCADE |
| name | TEXT | NOT NULL |
| color | TEXT | hex (#RRGGBB) |
| weekly_hours | INTEGER | DEFAULT 0 |
| created_at | DATETIME | DEFAULT now() |

**tasks**
| Campo | Tipo | Restrições |
|-------|------|------------|
| id | INTEGER | PK |
| user_id | INTEGER | FK → users.id |
| subject_id | INTEGER | FK → subjects.id, ON DELETE CASCADE |
| title | TEXT | NOT NULL |
| description | TEXT | nullable |
| status | TEXT | CHECK IN ('pending','done'), DEFAULT 'pending' |
| estimated_min | INTEGER | DEFAULT 0 |
| due_date | DATETIME | nullable |
| created_at | DATETIME | DEFAULT now() |
| updated_at | DATETIME | DEFAULT now() |

**study_blocks** (gerados pela IA)
| Campo | Tipo | Restrições |
|-------|------|------------|
| id | INTEGER | PK |
| task_id | INTEGER | FK → tasks.id, ON DELETE CASCADE |
| order | INTEGER | NOT NULL |
| duration_min | INTEGER | NOT NULL |
| scheduled_at | DATETIME | nullable |
| done | BOOLEAN | DEFAULT false |

### 5.3 Relacionamentos
- `users` 1 — N `subjects`
- `users` 1 — N `tasks`
- `subjects` 1 — N `tasks`
- `tasks` 1 — N `study_blocks`

---

## 6. Riscos do Projeto

### 6.1 Riscos Técnicos

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Limitações do SQLite em concorrência | Médio | Média | Manter ORM agnóstico (SQLAlchemy/Prisma) para migração rápida a PostgreSQL. |
| Latência da IA degradando UX | Médio | Média | Executar heurística local no MVP; chamadas a LLM em background com fallback. |
| Acoplamento entre frontend e contratos da API | Alto | Média | Gerar tipos a partir do OpenAPI (FastAPI já expõe); versionar API (`/v1`). |
| Crescimento descontrolado do schema | Médio | Baixa | Adotar migrations (Alembic/Prisma Migrate) desde o dia 1. |

### 6.2 Riscos Operacionais

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Escopo inflando antes do MVP | Alto | Alta | Travar escopo MVP neste PRD; novas ideias vão para backlog. |
| Falta de testes | Alto | Média | Definir gates de CI (lint + testes mínimos) antes de merge. |
| Indisponibilidade do banco (arquivo SQLite corrompido) | Alto | Baixa | Backups diários automatizados; volume persistente em produção. |

### 6.3 Riscos de Segurança

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Vazamento de dados** (e-mails/senhas) | Crítico | Senhas só armazenadas como hash bcrypt; logs sem PII; HTTPS obrigatório; criptografia em repouso quando possível. |
| **Exposição de APIs** (rotas sem auth) | Crítico | Middleware JWT obrigatório por padrão; testes automatizados verificando 401/403; revisão de rotas em code review. |
| **SQL Injection** | Crítico | Uso exclusivo de ORM com queries parametrizadas; proibido SQL cru concatenado. |
| **Brute-force em login** | Alto | Rate limiting (ex.: 5 tentativas/min/IP) + bloqueio temporário; CAPTCHA pós N falhas. |
| **XSS no frontend** | Alto | React escapa por padrão; sanitizar qualquer `dangerouslySetInnerHTML`; CSP estrita. |
| **CSRF** | Médio | Tokens em header `Authorization` (não cookies) eliminam o vetor clássico; se usar cookies, ativar `SameSite=Strict`. |
| **Vazamento de segredos** | Alto | `.env` fora do repositório; secret manager em produção; rotação periódica do `JWT_SECRET`. |
| **Dependências vulneráveis** | Médio | `pip-audit` / `npm audit` em CI; Dependabot ativo. |

---

## 7. Critérios de Aceite do MVP

- [ ] Usuário consegue se cadastrar, logar e deslogar.
- [ ] Todas as rotas de dados estão protegidas por JWT.
- [ ] CRUD completo de matérias e tarefas funcional.
- [ ] Dashboard exibe barra de progresso semanal corretamente.
- [ ] Ao acumular ≥10 tarefas pendentes, a IA sugere divisão em blocos.
- [ ] UI responsiva validada em mobile, tablet e desktop.
- [ ] Senhas armazenadas em hash; nenhuma rota crítica acessível sem token.
- [ ] Cobertura de testes ≥ 70% nos services do backend.

---

## 8. Próximas Etapas

1. **Etapa 3 — Desenvolvimento**
   - Frontend: estrutura Vite + Dashboard com barra de progresso.
   - Backend: endpoints CRUD de matérias/tarefas com FastAPI + SQLite + JWT.
2. **Etapa 4 — Segurança**
   - Análise estática (Bandit/ESLint security), `pip-audit`/`npm audit`, pentest manual nas rotas de auth.
3. **Etapa 5 — Documentação**
   - `README.md` com setup, scripts e variáveis de ambiente.
   - Documento de arquitetura (este PRD + diagramas C4).
   - Relatório de vulnerabilidades e plano de remediação.

---

*Fim do documento — PRD StudyFlow v1.0*
