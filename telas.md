# TELAS — Dashboard PP Colaboradores V2

## Mapa de telas

```
[Acesso público]
    └── /login                    → Tela de Login

[Autenticado — Gestor]
    └── /dashboard                → Dashboard (aba da sua loja apenas)

[Autenticado — Diretor / Admin]
    ├── /dashboard                → Dashboard (todas as abas + visão consolidada)
    └── /admin                    → Painel Administração (somente Admin)
        ├── /admin/usuarios       → Lista de usuários
        ├── /admin/usuarios/novo  → Criar usuário
        └── /admin/usuarios/:id   → Editar / desativar usuário
```

---

## Tela 1 — Login

**URL:** `/login`
**Acesso:** público (sem autenticação)

**Conteúdo:**
- Logo FarmaNello centralizado
- Título: "Painel de Performance — Colaboradores"
- Campo: Usuário
- Campo: Senha (mascarada)
- Botão: Entrar
- Mensagem de erro para credenciais inválidas
- Mensagem de bloqueio após 5 tentativas

**Comportamento:**
- Login bem-sucedido → redireciona conforme perfil (ver permissoes.md)
- Sessão inválida ou expirada → redireciona para login com mensagem
- Já logado → redireciona direto para dashboard

**Visual:** página centralizada, fundo com cor da marca, card branco com formulário, mobile-first.

---

## Tela 2 — Dashboard (perfil Gestor)

**URL:** `/dashboard`
**Acesso:** autenticado — qualquer perfil

**Conteúdo — Gestor (vê apenas sua loja):**
- Header: logo + nome do usuário + nome da loja + botão Sair
- Barra de informações: período atual + data da última atualização
- **Resumo da Loja** (KPI cards):
  - Faturamento realizado vs meta
  - ID% médio da equipe
  - Total de prêmios gerados
  - Valor total que a loja pode perder
- **Ranking Top 3** — colaboradores com melhor ID%
- **Cards individuais** por colaborador:
  - Nome
  - Badge de situação (ATINGIU / PARCIAL / NÃO ATINGIU)
  - Barra de progresso com ID%
  - Indicadores: Venda Geral, Vitaminas, Não Medicamentos
  - Prêmio ganho / Prêmio base
  - Falta mês / Necessário por dia

**Conteúdo — Diretor/Admin (vê todas as lojas):**
- Tudo acima, mais:
- **Abas por loja:** MATRIZ | PIRAQUARA I | PIRAQUARA II | MARIA ANTONIETA | CONSOLIDADO
- **Aba Consolidado:**
  - Ranking geral de colaboradores (todas as lojas)
  - KPIs da rede: faturamento total, ID% médio, prêmio total

---

## Tela 3 — Painel de Administração

**URL:** `/admin`
**Acesso:** somente perfil `admin`

**Conteúdo:**
- Header igual ao dashboard + indicador "ADMIN"
- Menu lateral: Usuários / Configurações
- Painel principal: lista de usuários

### Sub-tela: Lista de Usuários (`/admin/usuarios`)
- Tabela com: Nome, Login, Perfil, Loja, Status (Ativo/Inativo), Último acesso
- Botão: Novo usuário
- Ação por usuário: Editar | Desativar | Resetar senha

### Sub-tela: Criar / Editar Usuário (`/admin/usuarios/novo` ou `/:id`)
- Formulário: Nome, Login, Senha (+ confirmar), Perfil, Loja (se gestor)
- Botão: Salvar | Cancelar
- Opção: Desativar conta (na edição)

---

## Fluxo de navegação

```
[Acesso]
  ↓ Abre o site (https://painel.farmanello.com.br)
  ↓ Não logado → Tela de Login
  ↓ Credenciais corretas
  ↓
  ├─ [Gestor] → Dashboard (loja própria, sem abas de outras lojas)
  │
  ├─ [Diretor] → Dashboard (todas as abas + Consolidado)
  │
  └─ [Admin] → Dashboard (todas as abas) + acesso ao menu /admin
```

---

## Componentes visuais reutilizáveis

| Componente | Descrição |
|------------|-----------|
| `CardColaborador` | Card individual com badge, barras de progresso, KPIs |
| `CardKPI` | Mini-card para totais de loja (faturamento, ID%, prêmio) |
| `BadgeStatus` | Pill colorida ATINGIU / PARCIAL / NÃO ATINGIU |
| `BarraProgresso` | Barra horizontal com fill colorido por performance |
| `RankingTop3` | Destaque dos 3 melhores colaboradores |
| `AbaLoja` | Tab de navegação por loja |
| `Header` | Barra superior com logo, usuário e botão sair |
| `AlertaAtualizacao` | Banner mostrando data/hora da última atualização |

---

## Padrão visual

- Framework CSS: Bootstrap 5
- Referência de estilo: HubSpot Clean (Proposta A aprovada na V1)
- Mobile-first obrigatório
- Cores semânticas: verde ≥100%, âmbar 95-99%, vermelho <95%
- Paleta FarmaNello: azul `#1A2B4A`, accent `#2563EB`
