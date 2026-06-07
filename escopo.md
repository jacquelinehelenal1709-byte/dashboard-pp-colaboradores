# ESCOPO — Dashboard PP Colaboradores V2

## Objetivo

Criar um sistema web de visualização do Painel de Performance dos colaboradores da rede FarmaNello, com autenticação por login e senha, controle de acesso por perfil e exibição dos dados já calculados pela automação V1.

---

## Separação de responsabilidades

| Versão | Responsabilidade |
|--------|-----------------|
| V1 — `gerar_pp_colaboradores.py` | Leitura dos arquivos, cálculos, regras de negócio, geração do `conferencia.xlsx` e painéis PNG |
| V2 — `dashboard_pp_colaboradores` | Visualização web, autenticação, controle de acesso por perfil, experiência do usuário |

**A V2 não calcula nada. Ela consome o output da V1.**

---

## O que está DENTRO do escopo

- Página de login com usuário e senha
- Dashboard web responsivo (mobile + desktop)
- Abas por loja conforme perfil do usuário
- Visualização dos cards de colaboradores com indicadores de performance
- Visão consolidada para Sócios/Diretoria
- Painel de administração para gerenciar usuários
- Atualização automática dos dados quando a V1 for executada
- Controle de acesso por perfil (gestor vê apenas sua loja)

## O que está FORA do escopo

- Recálculo de metas, prêmios ou indicadores (responsabilidade da V1)
- Edição de planilhas ou dados diretamente pelo sistema
- Envio automático por WhatsApp (mantido na V1)
- Integração com ERP ou sistemas externos
- Histórico de períodos anteriores (fase futura)

---

## Premissas

1. A V1 já foi executada e gerou o arquivo `conferencia.xlsx` (ou JSON intermediário)
2. Isabelly é responsável por substituir os 4 arquivos na pasta `entrada` e executar a V1
3. Os gestores acessam o dashboard via navegador na rede local
4. Cada gestor já possui login e senha definidos pelo Administrador
5. O sistema roda localmente (servidor na máquina da FarmaNello)

## Restrições

- A V1 continua inalterada — a V2 jamais modifica arquivos de entrada ou saída da V1
- Senhas devem ser armazenadas com hash (bcrypt ou equivalente), nunca em texto simples
- Acesso ao painel admin restrito ao perfil Administrador

---

## Lojas cadastradas

| ID | Nome |
|----|------|
| MATRIZ | Matriz |
| PIRAQUARA_I | Piraquara I |
| PIRAQUARA_II | Piraquara II |
| MARIA_ANTONIETA | Maria Antonieta |
