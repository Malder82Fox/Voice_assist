# 09. Предварительный backlog (IDEAS — НЕ открытые GitHub Issues)

Ниже — будущая структура GitHub Issues. **Эти задачи не заведены в GitHub и не запущены в работу.** Создать их только при возобновлении проекта и пересмотреть приоритет.

| Epic ID | Название | Выходной артефакт | Зависимость |
|---|---|---|---|
| VA-DISC-01 | Reconfirm scope & target users | Подписанный MVP brief | — |
| VA-SEC-01 | Legacy secret review & credential rotation | Перечень закрытых инцидентов без ключей | — |
| VA-CORE-01 | Python package, dependencies & CI | Воспроизводимая сборка/тесты | DISC |
| VA-CORE-02 | Typed command model, router and skill registry | Unit/contract tests | CORE-01 |
| VA-CORE-03 | Permission model, no-op default, confirmations | Deny/allow tests | CORE-02 |
| VA-VOICE-01 | Compare offline Russian STT providers | Benchmarks and ADR | CORE-02 |
| VA-VOICE-02 | TTS abstraction and Russian voices | Audible demo and fallback | CORE-02 |
| VA-VOICE-03 | Push-to-talk, UX, noisy environments | Measured false-positive tests | VOICE-01 |
| VA-PLUGIN-01 | Personal skills & provider integration | Isolated adapter tests | CORE-03 |
| VA-AI-01 | Optional structured NLU | Schema + prompt-injection tests | CORE-03 |
| VA-CL-01 | CanLine API requirements & RBAC contract | Reviewed endpoint spec | CORE-03 |
| VA-CL-02 | Read-only CanLine voice proof-of-concept | Test-tenant demo with auditing | CL-01, VOICE |
| VA-OPS-01 | Logging, privacy, packaging, releases | Operator/dev guides | CORE/VOICE |

## Примеры acceptance criteria

**VA-CORE-02:** добавление нового навыка не требует изменения логики STT/TTS; неизвестный intent не приводит к side effects; все сценарии тестируются без реального микрофона.

**VA-CORE-03:** deny по умолчанию; разрешение проверяется до действия; провал идентификации или недоступная целевая система означает отказ.

**VA-CL-02:** scope ограничен read-only; разные tenants изолированы; любой ответ содержит timestamp/source; при пропавших данных система не изобретает измерения.

## Принцип работы в GitHub

- Одна задача — одна короткоживущая ветка.
- Draft PR можно открыть рано для ревью, объединять только после тестов и review.
- Отдельно фиксировать реальные результаты тестов; планы не закрывают задачи.
- \`master\` не использовать как актуальную разработческую ветку без специального migration plan.
- Документацию актуализировать в том же PR, когда меняется решение.

## Приоритет при ограниченных ресурсах

Наиболее полезный путь для CanLine OS: CORE → SECURITY → read-only API contract → text demo → voice demo. Это предотвращает преждевременную привязку архитектуры к конкретному STT провайдеру.
