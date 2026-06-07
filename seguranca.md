# SEGURANÇA — Dashboard PP Colaboradores V2

## HTTPS obrigatório

O sistema será acessado exclusivamente via HTTPS em produção.

- URL de produção: `https://painel.farmanello.com.br`
- Certificado SSL: obtido via **Let's Encrypt** (gratuito, renovação automática)
- Todo tráfego HTTP é redirecionado automaticamente para HTTPS (redirect 301)
- Em desenvolvimento local, HTTPS não é obrigatório

### Por que HTTPS é crítico aqui
Os dados exibidos incluem metas, prêmios e performance individual de colaboradores — informações sensíveis que não podem trafegar em texto claro.

---

## Autenticação e sessão

### Hash de senha
- Senhas armazenadas com **bcrypt** (custo mínimo: 12 rounds)
- Nunca armazenar senha em texto simples, nem em log
- Na troca de senha, validar força: mínimo 8 caracteres, ao menos 1 número

### Sessão segura
- Token de sessão gerado com `secrets.token_hex(32)` (256 bits)
- Cookie de sessão com flags: `HttpOnly=True`, `Secure=True`, `SameSite=Lax`
- Tempo de expiração da sessão: **4 horas** de inatividade
- No logout, a sessão é invalidada no servidor (não apenas apagada no cliente)

### Proteção contra força bruta (rate limiting)
- Máximo de **5 tentativas de login** por IP em 15 minutos
- Após o limite, bloqueio temporário de 15 minutos com mensagem ao usuário
- Registro de todas as tentativas falhas em log

---

## Proteção de rotas

- Todas as rotas do dashboard verificam autenticação a cada requisição
- Verificação de perfil (gestor X diretor X admin) em cada endpoint protegido
- Gestor que tenta acessar dados de outra loja recebe **HTTP 403**
- Usuário inativo não consegue fazer login mesmo com senha correta

---

## Backup

| Item | Frequência | Destino |
|------|-----------|---------|
| Banco de usuários (`usuarios.db`) | Diário | Pasta backup local + Google Drive |
| Arquivo de dados (`dados_dashboard.json`) | A cada atualização da V1 | Versionado junto com a pasta saida/ |
| Código-fonte | Contínuo | Repositório Git privado |

---

## Proteção de dados dos colaboradores (LGPD)

Os dados exibidos no sistema incluem desempenho individual e remuneração variável — classificados como **dados de gestão de pessoas**, sujeitos à LGPD (Lei 13.709/2018).

### Medidas adotadas

| Medida | Implementação |
|--------|--------------|
| Acesso restrito ao necessário | Gestor vê apenas sua loja |
| Dados mínimos expostos | Apenas o necessário para gestão de performance |
| Sem armazenamento de dados pessoais sensíveis | O sistema não guarda CPF, endereço, etc. |
| Controle de acesso com autenticação | Login obrigatório para qualquer dado |
| Log de acesso | Registrar quem acessou o quê e quando |
| Responsável pelo tratamento | Jacqueline Silva (Gerente Financeira) |

### O que NÃO deve ser feito
- Não exportar dados de colaboradores para fora do sistema sem autorização
- Não compartilhar login ou senha com terceiros
- Não acessar dados de colaboradores de outras lojas sem perfil adequado

---

## Variáveis de ambiente (não versionar)

As seguintes informações **nunca** devem estar no código-fonte ou em repositório:

```
SECRET_KEY=<chave aleatória gerada na configuração>
DATABASE_URL=<caminho do banco>
ADMIN_PASSWORD_HASH=<hash bcrypt da senha inicial>
```

Armazenar em arquivo `.env` (excluído do Git via `.gitignore`).

---

## Opções de hospedagem para produção

### Comparativo

| Opção | Custo estimado | HTTPS automático | Facilidade | Recomendado para |
|-------|---------------|-----------------|-----------|-----------------|
| **Render** | Gratuito (com limites) ou ~$7/mês | ✓ Automático | ⭐⭐⭐⭐⭐ | **1ª versão — recomendado** |
| Railway | ~$5/mês | ✓ Automático | ⭐⭐⭐⭐ | Boa alternativa ao Render |
| VPS (DigitalOcean/Linode) | ~$6–12/mês | Manual (Certbot) | ⭐⭐⭐ | Controle total, mais técnico |
| Servidor próprio | Custo de hardware | Manual (Certbot) | ⭐⭐ | Rede interna, sem acesso externo fácil |
| Vercel | Gratuito | ✓ Automático | ⭐⭐ | Não recomendado (projetado para frontend estático, não Flask) |

### Recomendação para a primeira versão: **Render**

**Por quê:**
- Deploy direto do repositório Git (GitHub)
- HTTPS automático com Let's Encrypt — zero configuração
- Domínio customizado gratuito (`painel.farmanello.com.br`)
- Plano gratuito funciona para carga leve (uso interno)
- Sem necessidade de configurar servidor Linux, nginx ou certbot
- Fácil rollback em caso de problema

**Limitação do plano gratuito:** o servidor "dorme" após 15 minutos sem acesso — o primeiro acesso do dia pode demorar ~30 segundos. O plano pago ($7/mês) elimina isso.

---

## Checklist de segurança pré-deploy

- [ ] HTTPS ativo e HTTP redireciona para HTTPS
- [ ] `SECRET_KEY` gerada aleatoriamente e em variável de ambiente
- [ ] Senhas de todos os usuários com hash bcrypt
- [ ] Rate limiting de login configurado
- [ ] Cookies com `HttpOnly`, `Secure`, `SameSite=Lax`
- [ ] Sessões expiram após inatividade
- [ ] Rotas protegidas verificam perfil
- [ ] Arquivo `.env` no `.gitignore`
- [ ] Backup do banco configurado
- [ ] Log de acesso ativo
