---
name: dev-workflow
description: "Execute o fluxo completo de desenvolvimento para este projeto NASA GCN. Use quando precisar fazer alterações no código, criar features, corrigir bugs, ou fazer qualquer modificação que precisa passar pelo processo de CI/CD. Triggers: 'implementar', 'adicionar feature', 'corrigir', 'alterar', 'modificar', 'criar branch', 'fazer deploy'."
---

# Dev Workflow - NASA GCN Pipeline

## Visão Geral

Este skill implementa o fluxo de desenvolvimento padrão para o projeto NASA GCN Pipeline. Ele garante que todas as alterações passem por um processo consistente de validação antes de chegar à produção.

## Fluxo de Desenvolvimento

```
┌─────────────────────────────────────────────────────────────┐
│  1. FEATURE BRANCH                                          │
│     git checkout -b feature/<nome-descritivo>               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. IMPLEMENTAÇÃO                                           │
│     Fazer as alterações necessárias no código               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. TESTES UNITÁRIOS                                        │
│     pytest tests/ -v                                        │
│     (1 teste conhecido falha: test_get_logger)              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. DEPLOY EM DEV                                           │
│     ./deploy.sh                                             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  5. VALIDAÇÃO DO PIPELINE EM DEV                            │
│     ./deploy.sh run-only                                    │
│     Aguardar conclusão e verificar métricas                 │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  6. COMMIT E PUSH                                           │
│     git add <arquivos>                                      │
│     git commit -m "<mensagem>"                              │
│     git push -u origin feature/<nome>                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  7. PULL REQUEST                                            │
│     gh pr create --title "<título>" --body "<descrição>"    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  8. MERGE E CLEANUP                                         │
│     gh pr merge <PR#> --merge --delete-branch               │
│     git checkout main && git pull                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  9. DEPLOY EM PROD (opcional)                               │
│     TARGET=prod ./deploy.sh                                 │
└─────────────────────────────────────────────────────────────┘
```

## Comandos Detalhados

### 1. Criar Feature Branch

```bash
git checkout main
git pull
git checkout -b feature/<nome-descritivo>
```

**Convenções de nome:**
- `feature/add-<funcionalidade>` - Nova funcionalidade
- `feature/fix-<problema>` - Correção de bug
- `feature/refactor-<área>` - Refatoração
- `feature/migrate-<de>-to-<para>` - Migrações
- `feature/remove-<item>` - Remoções

### 2. Testes Unitários

```bash
# Executar todos os testes
pytest tests/ -v

# Resultado esperado: 18 passed, 1 failed (test_get_logger é conhecido)
```

### 3. Lint e Formatação

```bash
# Verificar lint
ruff check src/ tests/

# Corrigir automaticamente
ruff check src/ tests/ --fix

# Formatar código
ruff format src/ tests/
```

### 4. Deploy em Dev

```bash
# Apenas deploy
./deploy.sh

# Deploy + executar job
./deploy.sh run

# Apenas executar (sem deploy)
./deploy.sh run-only
```

### 5. Validar Pipeline em Dev

```bash
./deploy.sh run-only
```

**Verificar no output:**
- Todas as tasks devem ter `result_state: SUCCESS`
- Bronze, Silver, Gold devem processar registros
- Métricas devem ser exibidas no relatório final

### 6. Commit

```bash
git add <arquivos>
git commit -m "$(cat <<'EOF'
<tipo>: <descrição curta>

<descrição detalhada opcional>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

**Tipos de commit:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `refactor`: Refatoração sem mudança de comportamento
- `chore`: Tarefas de manutenção
- `docs`: Documentação
- `test`: Testes

### 7. Push e PR

```bash
# Push
git push -u origin feature/<nome>

# Criar PR
gh pr create --title "<título>" --body "$(cat <<'EOF'
## Summary
- <bullet points>

## Test plan
- [x] pytest passed (18/19)
- [x] Deployed to dev
- [x] Pipeline executed successfully

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 8. Merge

```bash
gh pr merge <PR#> --merge --delete-branch
git checkout main
git pull
```

### 9. Deploy em Prod (se necessário)

```bash
TARGET=prod ./deploy.sh
```

## Checklist de Validação

Antes de criar o PR, verificar:

- [ ] Código está formatado (`ruff format`)
- [ ] Lint passa (`ruff check`)
- [ ] Testes unitários passam (18/19 expected)
- [ ] Deploy em dev bem-sucedido
- [ ] Pipeline executou com sucesso em dev
- [ ] Métricas do pipeline estão corretas

## Troubleshooting

### Autenticação expirada

```bash
databricks auth login --profile dltreinamentos.data@gmail.com \
  --host https://dbc-5fa38af7-00ad.cloud.databricks.com
```

### Credenciais não encontradas

```bash
# Verificar .env existe e tem credenciais
cat .env | grep GCN_CLIENT

# Se necessário, recodificar
python scripts/encode_credentials.py
```

### Pipeline falhou

```bash
# Ver detalhes do job run
databricks jobs get-run <RUN_ID> -p dltreinamentos.data@gmail.com

# Ver eventos do pipeline
databricks pipelines get-events --pipeline-id <PIPELINE_ID>
```

## Ambientes

| Target | Catálogo | Uso |
|--------|----------|-----|
| `dev` (padrão) | `sandbox` | Desenvolvimento e testes |
| `prod` | `nasa_gcn` | Produção |
