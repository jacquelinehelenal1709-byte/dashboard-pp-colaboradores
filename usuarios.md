# USUÁRIOS — Dashboard PP Colaboradores V2

## Estrutura de um usuário

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | int | Identificador único |
| `nome` | string | Nome completo |
| `login` | string | Nome de usuário (único) |
| `senha_hash` | string | Hash bcrypt da senha |
| `perfil` | enum | Ver tabela de perfis |
| `loja` | string ou null | Loja vinculada (null para perfis que veem tudo) |
| `ativo` | bool | Usuário habilitado ou desabilitado |
| `criado_em` | datetime | Data de criação |
| `ultimo_acesso` | datetime | Último login registrado |

---

## Perfis disponíveis

| Perfil | Código | Descrição |
|--------|--------|-----------|
| Administrador | `admin` | Acesso total + gerenciamento de usuários |
| Sócio / Diretoria | `diretor` | Visualiza todas as lojas + visão consolidada |
| Gestor Matriz | `gestor_matriz` | Visualiza apenas Matriz |
| Gestor Piraquara I | `gestor_piraquara1` | Visualiza apenas Piraquara I |
| Gestor Piraquara II | `gestor_piraquara2` | Visualiza apenas Piraquara II |
| Gestor Maria Antonieta | `gestor_maria_antonieta` | Visualiza apenas Maria Antonieta |

---

## Usuários iniciais (configuração de implantação)

A definir com Jacqueline Silva durante a implantação. Abaixo os usuários sugeridos como ponto de partida:

| Login | Perfil | Loja |
|-------|--------|------|
| `admin` | Administrador | — |
| `jacqueline` | Sócio/Diretoria | — |
| `gestor.matriz` | Gestor Matriz | MATRIZ |
| `gestor.piraquara1` | Gestor Piraquara I | PIRAQUARA_I |
| `gestor.piraquara2` | Gestor Piraquara II | PIRAQUARA_II |
| `gestor.antonieta` | Gestor Maria Antonieta | MARIA_ANTONIETA |

> As senhas iniciais são definidas pelo Administrador na primeira configuração.

---

## Regras de usuário

1. O login deve ser único no sistema
2. A senha deve ter no mínimo 8 caracteres
3. Senhas armazenadas com hash bcrypt (nunca em texto simples)
4. Usuários inativos não conseguem fazer login
5. O Administrador pode criar, editar, desativar e resetar senhas
6. O Administrador não pode excluir sua própria conta
7. Cada gestor está vinculado a exatamente uma loja
8. Perfis `admin` e `diretor` não possuem loja vinculada (campo null)

---

## Armazenamento

Os usuários serão armazenados em banco SQLite (`usuarios.db`) na pasta `data/` do projeto V2.

Formato do arquivo de configuração inicial (`usuarios_inicial.json`) para seed do banco:

```json
[
  {
    "login": "admin",
    "nome": "Administrador",
    "perfil": "admin",
    "loja": null,
    "ativo": true
  },
  {
    "login": "jacqueline",
    "nome": "Jacqueline Silva",
    "perfil": "diretor",
    "loja": null,
    "ativo": true
  }
]
```
