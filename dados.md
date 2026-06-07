# DADOS — Dashboard PP Colaboradores V2

## Fonte de dados

A V2 **não calcula nada**. Ela consome os dados gerados pela V1.

### Fluxo de dados

```
[Isabelly]
  ↓ Substitui os 4 arquivos em /entrada
  ↓ Executa gerar_pp_colaboradores.py (V1)
  ↓ V1 gera: conferencia.xlsx + painéis PNG + mensagem WhatsApp
  ↓
[V2 — Dashboard]
  ↓ Lê conferencia.xlsx (ou JSON intermediário)
  ↓ Serve os dados via dashboard web
```

---

## Arquivo intermediário: `dados_dashboard.json`

Para evitar que a V2 dependa do formato do Excel (que pode mudar), a V1 gerará um arquivo `dados_dashboard.json` na pasta `saida/`.

A V2 lê exclusivamente este JSON.

### Estrutura do JSON

```json
{
  "gerado_em": "2026-06-07T09:00:00",
  "periodo": {
    "inicio": "2026-06-01",
    "fim": "2026-06-05"
  },
  "lojas": {
    "MATRIZ": {
      "resumo": {
        "total_colaboradores": 8,
        "faturamento_realizado": 410000.00,
        "faturamento_previsto": 618000.00,
        "id_medio": 0.9182,
        "premio_total_ganho": 3100.00,
        "premio_total_possivel": 5600.00
      },
      "colaboradores": [
        {
          "nome": "ELOY",
          "total_dias": 26,
          "dias_trabalhados": 4,
          "dias_restantes": 22,
          "base_calculo": 700.00,
          "id_geral": 0.9182,
          "situacao": "NAO ATINGIU",
          "premio_total": 350.00,
          "val_perdido": 350.00,
          "falta_mes": 47230.78,
          "val_nec_dia": 2146.85,
          "indicadores": {
            "venda_geral": {
              "meta": 55000.00,
              "realizado": 7769.22,
              "previsao": 50499.93,
              "id_pct": 0.9182,
              "escala": 0.00,
              "peso": 0.50,
              "premio_base": 350.00,
              "premio_ganho": 0.00,
              "sem_meta": false,
              "is_quantidade": false
            },
            "vitaminas": {
              "meta": 115.0,
              "realizado": 31.0,
              "previsao": 202.0,
              "id_pct": 1.7522,
              "escala": 1.00,
              "peso": 0.20,
              "premio_base": 140.00,
              "premio_ganho": 140.00,
              "sem_meta": false,
              "is_quantidade": true
            },
            "nao_medicamentos": {
              "meta": 11000.00,
              "realizado": 1938.01,
              "previsao": 12597.07,
              "id_pct": 1.1452,
              "escala": 1.00,
              "peso": 0.30,
              "premio_base": 210.00,
              "premio_ganho": 210.00,
              "sem_meta": false,
              "is_quantidade": false
            }
          }
        }
      ]
    }
  }
}
```

---

## Campos utilizados por tela

### Card do colaborador
| Campo | Origem |
|-------|--------|
| Nome | `colaborador.nome` |
| Situação (badge) | `colaborador.situacao` |
| ID% geral | `colaborador.id_geral` |
| Dias trabalhados / total | `dias_trabalhados` / `total_dias` |
| Base de cálculo | `base_calculo` |
| Prêmio ganho | `premio_total` |
| Falta mês | `falta_mes` |
| Necessário por dia | `val_nec_dia` |
| Por indicador: meta / real / prev / ID% / escala / prêmio | `indicadores.*` |

### KPIs da loja (resumo)
| Campo | Origem |
|-------|--------|
| Faturamento realizado | `loja.resumo.faturamento_realizado` |
| Faturamento previsto | `loja.resumo.faturamento_previsto` |
| ID% médio da equipe | `loja.resumo.id_medio` |
| Total de prêmio ganho | `loja.resumo.premio_total_ganho` |
| Total de prêmio possível | `loja.resumo.premio_total_possivel` |

---

## Atualização dos dados

- A V2 verifica a data/hora de modificação do `dados_dashboard.json` a cada carregamento de página
- O campo `gerado_em` é exibido no header como "Última atualização: DD/MM/AAAA HH:MM"
- Se o arquivo não existir, a V2 exibe: "Dados ainda não disponíveis — execute a automação V1"
- **Não há auto-execução da V1 pela V2.** O gatilho é sempre manual (Isabelly executa o script)

---

## Alteração necessária na V1

Adicionar ao final da função `main()` em `gerar_pp_colaboradores.py`:

```python
gerar_json_dashboard(resultados, data_inicio, data_fim)
```

Esta função serializa `resultados` no formato acima e salva em `saida/dados_dashboard.json`.

Nenhuma regra de negócio é alterada — apenas um novo output é gerado.
