# 06. Будущая интеграция с CanLine OS

**Статус: предложение для дальнейшего проектирования.** Никакой связи с текущей установкой CanLine OS здесь не создаётся.

CanLine OS — модульная промышленная платформа SCADA + MES + ERP + MWS + QMS на общем core. Важные исходные принципы платформы: multi-plant, изоляция tenant, универсальные assets/tags, модульность, on-prem без интернета и security by default. Будущий Task & Workflow Manager также представляет интерес.

## Архитектурная граница

\`\`\`text
[Оператор / Инженер]
        |
[Voice Assist: STT, commands, policy]
        | authenticated read requests
        v
[CanLine API / gateway + identity + audit]
        |
       [Core Asset Registry / typed APIs]
         |        |       |       |       |
       SCADA     MES     MWS     QMS     ERP
         \___________ Task & Workflow ___________/
\`\`\`

- Ассистент **не открывает соединение к PLC**, не пишет в MQTT control topics и не обращается напрямую к SCADA/DB с обходом прикладной авторизации.
- Изоляция tenants, plants, lines and assets enforced **на сервере**. Наличие фразы «на моём заводе» недостаточно для определения области.
- Read-only scopes для пилота. Нет \`write\` endpoint в установленном credentials наборе.
- Ответы формируются на основе информации из API и содержат source_timestamp, status/quality и context.
- Вопросы, требующие действий, превращаются в *предложение открыть UI*, а не автоматические технологические команды.

## Функциональные привязки

| Область | Возможные данные |
|---|---|
| Core Asset Registry | tenant, plant, line, asset ID, equipment hierarchy |
| Template registry | Человеко-понятные названия оборудования и параметров |
| SCADA | Скорость, state, активные alarm, quality/staleness тегов |
| MES | Production count, OEE, runtime, downtime, shift context |
| MWS/Maintenance | Work orders, priority, status, responsible person |
| QMS | QC status, deviations, inspection context |
| ERP | Запчасти, заказ/остаток/поставка по разрешённому scope |
| Task & Workflow (позже) | Задачи, назначения, прогресс, ссылки на events/assets |

**Внимание:** API для этих запросов может отсутствовать или иметь другую схему; это список потребностей Voice Assist, не утверждение об имеющихся эндпоинтах.

## Сценарий пилота

1. Авторизованный инженер активирует голосовой режим на доверенном ПК.
2. Говорит «Скорость Cupper 1 на линии L1»; STT преобразует в текст.
3. Resolver возвращает тип \`get_asset_speed\` и параметры запроса; policy проверяет read scope.
4. Gateway проверяет реальную личность, tenant, plant, rights; разрешает доступ только к нужным данным.
5. API возвращает \`value\`, \`unit\`, \`observed_at\`, \`quality\`, \`asset_id\`, \`source\`.
6. Ответ: «По состоянию на ... скорость ...; источник SCADA». Если stale/unauthorized — сообщить об этом.

## Открытые проектные задачи

- Согласовать auth flow (device/user delegated token, short-lived, revocation) и API gateway.
- Сопоставлять голосовые названия с реестром assets без неоднозначных совпадений.
- Определить API contract и единицы измерения/периоды для OEE и downtime.
- Рассмотреть работу в локальной сети при полном отсутствии доступа в Интернет.
- В промышленном шуме протестировать гарнитуры и push-to-talk; не считать wake-word надёжной аутентификацией.
- Определить audit trail запросов, минимизацию текста и ограничения на хранение аудио.
- Обеспечить zero write scopes и hard deny любых опасных intents.

## Exit criteria будущего read-only pilot

Подтверждённый API contract; тестовый tenant/line; роли «разрешено/запрещено»; запросы с различными объектами; stale/unknown/unavailable ответы; аудит; тесты в шуме; безопасность проверена отдельно. До этого интеграция — только концепция.
