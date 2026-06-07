# ROADMAP — Dashboard PP Colaboradores V2

## Visão geral

```
FASE 1 → FASE 2 → FASE 3 → FASE 4 → FASE 5
Base     Dashboard  Admin    Produção  Melhorias
```

---

## FASE 1 — Estrutura base e autenticação local

**Objetivo:** sistema funcionando localmente com login e proteção de rotas

**Entregáveis:**
- [ ] Estrutura de pastas do projeto V2
- [ ] Banco SQLite com tabela de usuários
- [ ] Script de seed com usuários iniciais
- [ ] Página de login (HTML + Flask)
- [ ] Autenticação com sessão segura
- [ ] Rate limiting (bloqueio após 5 tentativas)
- [ ] Rotas protegidas por perfil
- [ ] Logout funcional
- [ ] Leitura do `dados_dashboard.json` gerado pela V1
- [ ] Adição da função `gerar_json_dashboard()` na V1

**Critério de conclusão:** conseguir fazer login com cada perfil e ser redirecionado para a tela correta

---

## FASE 2 — Dashboard por loja

**Objetivo:** dashboard visual completo conforme design aprovado (HubSpot Clean)

**Entregáveis:**
- [ ] Layout base responsivo com Bootstrap 5
- [ ] Header com logo, nome do usuário e botão sair
- [ ] Banner "Última atualização: DD/MM/AAAA HH:MM"
- [ ] KPI cards de resumo por loja
- [ ] Cards individuais por colaborador
- [ ] Barras de progresso coloridas por performance
- [ ] Badge ATINGIU / PARCIAL / NÃO ATINGIU
- [ ] Indicadores: Venda Geral, Vitaminas, Não Medicamentos
- [ ] Rodapé: Falta mês, Por dia, Perdeu
- [ ] Gestor vê apenas sua loja
- [ ] Diretor/Admin vê todas as lojas em abas

**Critério de conclusão:** gestor consegue ver apenas sua loja; diretor consegue navegar pelas abas

---

## FASE 3 — Visão consolidada e painel admin

**Objetivo:** visão gerencial completa para diretoria e gestão de usuários

**Entregáveis:**
- [ ] Aba "Consolidado" com KPIs da rede (apenas Diretor/Admin)
- [ ] Ranking geral entre lojas
- [ ] Painel `/admin/usuarios` — lista de usuários
- [ ] Criar usuário com perfil e loja
- [ ] Editar usuário
- [ ] Desativar / reativar usuário
- [ ] Resetar senha (gera senha temporária)
- [ ] Log de acesso básico

**Critério de conclusão:** admin consegue criar e gerenciar todos os usuários sem tocar no banco diretamente

---

## FASE 4 — Publicação em produção

**Objetivo:** sistema acessível via internet com domínio e HTTPS

### 4.1 — Preparação para deploy
- [ ] Criar repositório Git privado (GitHub)
- [ ] Configurar `.env` com variáveis de produção
- [ ] Confirmar que `.env` e `dados_dashboard.json` estão no `.gitignore`
- [ ] Criar `requirements.txt` com todas as dependências
- [ ] Criar `Procfile` para o Render: `web: gunicorn app:app`
- [ ] Testar build local com gunicorn

### 4.2 — Configuração no Render
- [ ] Criar conta no Render (render.com)
- [ ] Conectar repositório GitHub ao Render
- [ ] Configurar variáveis de ambiente no painel do Render
- [ ] Fazer primeiro deploy
- [ ] Verificar que a aplicação está online

### 4.3 — Domínio e HTTPS
- [ ] Adquirir domínio `farmanello.com.br` (se ainda não tiver) — Registro.br
- [ ] Criar subdomínio: `painel.farmanello.com.br`
- [ ] Configurar DNS: apontar `painel.farmanello.com.br` → Render
- [ ] Ativar HTTPS no Render (automático com Let's Encrypt)
- [ ] Verificar redirect HTTP → HTTPS

### 4.4 — Criação dos usuários em produção
- [ ] Admin executa script de seed no banco de produção
- [ ] Criar conta de cada gestor com senha inicial
- [ ] Criar conta Diretor/Jacqueline
- [ ] Testar login com cada conta
- [ ] Enviar credenciais iniciais para cada gestor com instrução de troca de senha

### 4.5 — Upload dos dados
- [ ] Isabelly executa a V1 localmente
- [ ] V1 gera `dados_dashboard.json`
- [ ] JSON é transferido para o servidor (via Git push ou upload manual)
- [ ] Verificar que o dashboard exibe os dados corretos

**Critério de conclusão:** acessar `https://painel.farmanello.com.br` e fazer login com cada perfil

---

## FASE 5 — Homologação com gestores

**Objetivo:** validar com os usuários reais antes do uso em produção

- [ ] Reunião de apresentação com cada gestor
- [ ] Cada gestor testa login com suas credenciais
- [ ] Cada gestor valida que vê apenas sua loja
- [ ] Jacqueline valida visão consolidada e todas as abas
- [ ] Coleta de feedback
- [ ] Correção de bugs e ajustes visuais
- [ ] Aprovação formal para uso em produção

---

## Melhorias futuras (pós-homologação)

| Melhoria | Prioridade |
|----------|-----------|
| Troca de senha pelo próprio usuário | Alta |
| Histórico de períodos anteriores | Alta |
| Notificação por e-mail quando dados são atualizados | Média |
| Exportar PDF do painel por loja | Média |
| Gráfico de evolução do ID% ao longo do mês | Média |
| Integração com upload automático via formulário web | Baixa |
| Autenticação via Google (SSO) | Baixa |

---

## Responsabilidades

| Responsável | Papel |
|-------------|-------|
| Jacqueline Silva | Aprovação de entregas, decisões de negócio |
| Isabelly | Operação: atualizar arquivos de entrada e executar V1 |
| Desenvolvedor | Implementação técnica das fases 1 a 4 |
| Gestores | Homologação e uso em produção |
