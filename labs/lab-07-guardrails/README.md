# Lab 7: AI Guardrails

Este lab implementa guardrails de segurança para aplicações GenAI, incluindo detecção de PII e proteção contra prompt injection.

## Objetivos de Aprendizado

Após completar este lab, você será capaz de:

1. **Detectar PII** em dados não estruturados
2. **Aplicar masking** e anonymização
3. **Proteger contra prompt injection**
4. **Implementar guardrails** de input/output

## Tópicos do Exame Cobertos

| Seção | Peso | Tópicos |
|-------|------|---------|
| **Section 6: Governance** | 16% | PII detection, data anonymization, guardrails |

## Pré-requisitos

- Tabela `gcn_circulars` disponível
- Bibliotecas: presidio-analyzer, presidio-anonymizer, spacy

## Estrutura do Lab

```
lab-07-guardrails/
├── 01-pii-detection.py          # Detecção de PII
├── 02-masking.py                # Masking e anonymização
├── 03-prompt-protection.py      # Proteção contra injection
└── README.md                    # Este arquivo
```

## Notebooks

### 1. PII Detection (`01-pii-detection.py`)

**O que você vai aprender:**
- Identificar tipos de PII nos GCN Circulars
- Usar regex e Presidio para detecção
- Criar pipeline de scanning
- Gerar relatório de PII

**Tipos de PII detectados:**
| Tipo | Método | Risco |
|------|--------|-------|
| Email | Regex + Presidio | Medium |
| Phone | Regex | High |
| Person Name | Presidio NER | Low |
| Institution | Custom Pattern | Low |

### 2. Masking (`02-masking.py`)

**O que você vai aprender:**
- Estratégias de masking (replace, partial, redact)
- Anonymização com Presidio
- Criar versão anonymizada do dataset
- Validar que PII foi removido

**Estratégias de masking:**
```python
# Replace
"email@example.com" → "[EMAIL]"

# Partial
"email@example.com" → "e****@e******.com"

# Redact
"email@example.com" → ""
```

### 3. Prompt Protection (`03-prompt-protection.py`)

**O que você vai aprender:**
- Tipos de prompt injection
- Detecção de ataques
- Input/Output guardrails
- Integração com RAG

**Tipos de ataque detectados:**
| Tipo | Exemplo | Ação |
|------|---------|------|
| Direct Injection | "Ignore previous instructions" | Block |
| Jailbreak | "You are DAN" | Block |
| Data Extraction | "Show me all emails" | Block |
| Role Manipulation | "Act as a hacker" | Block |

## Arquitetura de Guardrails

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Input                                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT GUARDRAIL                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Length    │  │  Injection  │  │  Sanitize   │             │
│  │   Check     │  │  Detection  │  │   Input     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE                                │
│  Retriever → Context → Prompt → LLM → Response                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OUTPUT GUARDRAIL                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Sensitive  │  │ Compromise  │  │  Sanitize   │             │
│  │   Data      │  │  Detection  │  │   Output    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Safe Response                              │
└─────────────────────────────────────────────────────────────────┘
```

## Recursos Criados

| Recurso | Nome | Descrição |
|---------|------|-----------|
| Table | `pii_scan_results` | Resultados do scanning |
| Table | `gcn_circulars_anonymized` | Dados sem PII |

## Comandos Úteis

### Detectar PII com regex
```python
import re
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails = re.findall(email_pattern, text, re.IGNORECASE)
```

### Usar Presidio
```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

results = analyzer.analyze(text=text, language="en")
anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
```

### Validar prompt
```python
guardrail = InputGuardrail(max_length=2000, block_on_detection=True)
is_valid, message, details = guardrail.validate(prompt)
```

## Padrões de Prompt Injection

```python
SUSPICIOUS_PATTERNS = [
    r'ignore\s+(all\s+)?(previous|prior)\s+instructions?',
    r'forget\s+(everything|all)',
    r'you\s+are\s+(now\s+)?DAN',
    r'act\s+as\s+.*no\s+(restrictions?|limits?)',
    r'(SYSTEM|ADMIN)\s*:',
]
```

## Boas Práticas

1. **Defense in Depth**: Use múltiplas camadas de proteção
2. **Fail Secure**: Na dúvida, bloqueie
3. **Log Everything**: Mantenha auditoria de eventos
4. **Update Regularly**: Novos ataques surgem constantemente
5. **Test Extensively**: Teste com prompts adversários

## Troubleshooting

### Presidio não detecta entidades
```python
# Verificar idioma
results = analyzer.analyze(text=text, language="en")

# Verificar entidades suportadas
analyzer.get_supported_entities()
```

### Falsos positivos altos
- Ajuste os thresholds de confiança
- Adicione whitelist de termos permitidos
- Revise os padrões regex

### Performance lenta
- Use batch processing
- Cache resultados de análise
- Considere usar UDFs distribuídos

## Próximos Passos

Após completar este lab, continue para:

- **Lab 8: Monitoring** - Monitoramento de inferências
- **Lab 9: Vector Optimization** - Otimização de retrieval

## Referências

- [Presidio Documentation](https://microsoft.github.io/presidio/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Prompt Injection Attacks](https://www.lakera.ai/blog/guide-to-prompt-injection)

---

*Última atualização: Fevereiro 2026*
