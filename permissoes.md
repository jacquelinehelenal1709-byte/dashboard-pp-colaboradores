# PERMISSÕES — Dashboard PP Colaboradores V2

## Matriz de acesso por perfil

| Recurso / Tela | admin | diretor | gestor_loja |
|----------------|:-----:|:-------:|:-----------:|
| Login | ✓ | ✓ | ✓ |
| Dashboard — loja própria | ✓ | ✓ | ✓ |
| Dashboard — outras lojas | ✓ | ✓ | ✗ |
| Visão consolidada (todas as lojas) | ✓ | ✓ | ✗ |
| Ranking geral entre lojas | ✓ | ✓ | ✗ |
| Painel de Administração | ✓ | ✗ | ✗ |
| Criar usuário | ✓ | ✗ | ✗ |
| Editar usuário | ✓ | ✗ | ✗ |
| Desativar usuário | ✓ | ✗ | ✗ |
| Resetar senha | ✓ | ✗ | ✗ |
| Ver dados de colaboradores de outra loja | ✓ | ✓ | ✗ |

---

## Regras de acesso por perfil

### Administrador (`admin`)
- Acessa todas as telas do sistema
- Gerencia usuários: criar, editar, desativar, resetar senha
- Visualiza dados de todas as lojas
- Pode alterar seu próprio perfil (exceto desativar sua própria conta)

### Sócio / Diretoria (`diretor`)
- Acessa dashboard de todas as lojas simultaneamente
- Visualiza visão consolidada com KPIs gerais da rede
- Não acessa painel de administração de usuários
- Pode ver ranking comparativo entre lojas

### Gestor de Loja (`gestor_*`)
- Acessa **exclusivamente** os dados da loja vinculada ao seu perfil
- Ao fazer login, é redirecionado diretamente para a aba da sua loja
- Qualquer tentativa de acessar dados de outra loja retorna **HTTP 403**
- Não visualiza informações de outras lojas nem a visão consolidada

---

## Regras de redirecionamento pós-login

| Perfil | Página de destino após login |
|--------|------------------------------|
| `admin` | Dashboard — visão completa (todas as lojas) |
| `diretor` | Dashboard — visão consolidada |
| `gestor_matriz` | Dashboard — aba Matriz |
| `gestor_piraquara1` | Dashboard — aba Piraquara I |
| `gestor_piraquara2` | Dashboard — aba Piraquara II |
| `gestor_maria_antonieta` | Dashboard — aba Maria Antonieta |

---

## Bloqueio de acesso indevido

- Rotas protegidas verificam o perfil do usuário logado a cada requisição
- Se um gestor tentar acessar `/loja/MATRIZ` estando vinculado à `PIRAQUARA_I`, o sistema retorna **HTTP 403 — Acesso negado**
- Sessões expiram após **4 horas** de inatividade
- Após 5 tentativas de login erradas, o acesso é bloqueado por 15 minutos

---

## Dados visíveis por colaborador

Cada card de colaborador exibe:

| Dado | Gestor própria loja | Gestor outra loja | Diretor | Admin |
|------|:-------------------:|:-----------------:|:-------:|:-----:|
| Nome | ✓ | ✗ | ✓ | ✓ |
| Indicadores (meta/real/prev/ID%) | ✓ | ✗ | ✓ | ✓ |
| Prêmio | ✓ | ✗ | ✓ | ✓ |
| Falta mês / Por dia | ✓ | ✗ | ✓ | ✓ |
| Base de cálculo | ✓ | ✗ | ✓ | ✓ |
