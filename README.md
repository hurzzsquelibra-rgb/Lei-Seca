# Lei-Seca

> Agente especializado na criação de **material teórico doutrinário** para concursos públicos.  
> Converte o texto integral de qualquer norma jurídica (lei, decreto, resolução, portaria…) em um arquivo HTML autocontido, com CSS completo e pronto para estudo e impressão.

---

## Como funciona

O agente executa quatro etapas em ordem:

1. **Leitura analítica** — extrai estrutura normativa, prazos, modalidades ("deverá"/"poderá"), percentuais, agentes, exceções e alterações legislativas.
2. **Mapeamento de armadilhas** — identifica os quatro padrões de pegadinha mais explorados em provas (troca de modalidade, adulteração de prazo, troca de agente, supressão de condição).
3. **Organização temática** — agrupa artigos em blocos com título, âncora legal, conteúdo teórico e alertas de prova.
4. **Produção do HTML** — gera um arquivo autocontido com capa, sumário, blocos temáticos, callouts semânticos, badges de prazo e seção "Pontos Críticos".

---

## Instalação

```bash
git clone https://github.com/hurzzsquelibra-rgb/Lei-Seca.git
cd Lei-Seca
pip install -r requirements.txt
cp .env.example .env
# edite .env e preencha OPENAI_API_KEY
```

---

## Uso

### Via linha de comando

```bash
python -m src.cli caminho/para/norma.txt --norm "Lei nº 8.666/1993"
```

O arquivo HTML é salvo em `/mnt/user-data/outputs/` (ou `./outputs/` em desenvolvimento local).

**Opções disponíveis:**

| Opção | Descrição | Padrão |
|---|---|---|
| `--norm` | Identificador da norma (detectado automaticamente quando omitido) | auto |
| `--model` | Modelo LLM | `gpt-4o` |
| `--output-dir` | Diretório de saída | `/mnt/user-data/outputs` |
| `--api-key` | Chave de API (alternativa à variável de ambiente) | — |

**PDF também é aceito** (requer `pdfminer.six`, já listado em `requirements.txt`):

```bash
python -m src.cli norma.pdf
```

### Via Python

```python
from src.agent import LeiSecaAgent

agent = LeiSecaAgent()
output_path = agent.process(
    document=open("lei8666.txt").read(),
    norm_identifier="Lei nº 8.666/1993",
)
print(f"Salvo em: {output_path}")
```

---

## Estrutura do projeto

```
Lei-Seca/
├── src/
│   ├── agent.py          # LeiSecaAgent — lógica principal
│   ├── cli.py            # Ponto de entrada CLI
│   ├── html_generator.py # Shell HTML + CSS completo
│   └── prompts.py        # System prompt do agente
├── tests/
│   └── test_leiseca.py   # Testes unitários (35 casos)
├── outputs/              # HTML gerados (ignorados no git)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | Chave de API OpenAI-compatible |
| `LEISECA_MODEL` | ➖ | Modelo LLM (padrão: `gpt-4o`) |
| `LEISECA_OUTPUT_DIR` | ➖ | Diretório de saída (padrão: `/mnt/user-data/outputs`) |

---

## Testes

```bash
pytest tests/ -v
```

---

## Saída HTML — componentes

O arquivo gerado inclui:

- **Capa** — fundo escuro institucional, badge da norma, título e tags de contexto
- **Sumário** — links âncora com número de artigo em fonte mono
- **Blocos temáticos** — cabeçalho de seção, explicação do instituto, listas estruturadas
- **Callouts semânticos** — azul (definição), verde (regra positiva), amarelo (armadilha ⚠), vermelho (vedação/sanção)
- **Badges de prazo inline** — dourado (prazo neutro) e vermelho (prazo com sanção)
- **Tabelas, cards comparativos e fluxos procedimentais** — gerados apenas quando os critérios de uso são satisfeitos
- **Seção "Pontos Críticos"** — armadilhas identificadas em linguagem direta
- **Responsividade** — breakpoint em 680 px + `@media print`
