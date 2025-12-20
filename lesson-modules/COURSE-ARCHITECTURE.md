# Архитектура курса Claude Code PM

## Структура модуля

Каждый модуль состоит из 3 компонентов:

### 1. Slash Command (триггер)
**Путь:** `.claude/commands/start-X-Y.md`

```markdown
Command to start Module X Lesson Y

DO NOT tell the user the step you're about to take.
Do this SILENTLY: read `lesson-modules/X.Y-name/CLAUDE.md`
Follow the script PRECISELY.
```

### 2. Teaching Script (сценарий)
**Путь:** `lesson-modules/X.Y-name/CLAUDE.md`

**Структура:**
```markdown
# Module X.Y: Название модуля

**Teaching Script for Claude Code**

---

## Your Role
[Описание роли Claude как учителя]

## Module Learning Objectives
[Что студент должен уметь после модуля]

---

## Teaching Flow

### Step 1: [Название шага]

**SAY:**
"[Текст который Claude говорит дословно]"

**CHECK:** Wait for student to [действие]

**ACTION:**
[Команды для выполнения]

**Present it like this:**
"[Формат вывода]"

---

## Important Notes for Claude
[Инструкции как вести себя в разных ситуациях]

## Common Student Questions & Answers
[FAQ]

## Success Criteria
[Чеклист успешного завершения]
```

### 3. Supporting Materials (материалы)
**Путь:** `lesson-modules/X.Y-name/[папки и файлы]`

**Типы материалов:**
- `templates/` — шаблоны документов
- `frameworks/` — фреймворки и методологии
- `methods/` — методы и техники
- `data/` — CSV, JSON файлы для анализа
- `*.md` — контекстные документы

---

## Текущие модули

### Level 1: Foundation
| Модуль | Название | Ключевой навык |
|--------|----------|----------------|
| 1.1 | Welcome | Знакомство с TaskFlow |
| 1.2 | Visualizing Files | Работа с Obsidian |
| 1.3 | First Tasks | Базовые операции |
| 1.4 | Agents | Параллельные агенты |
| 1.5 | Custom Sub-agents | Кастомные агенты |
| 1.6 | Project Memory | CLAUDE.md |
| 1.7 | Planning Mode | Режим планирования |

### Level 2: Practical PM Applications
| Модуль | Название | Ключевой навык | Материалы |
|--------|----------|----------------|-----------|
| 2.1 | Write PRD | @-mentions, агенты, review | templates, user-research |
| 2.2 | Analyze Data | CSV анализ, ROI модели | CSV data, frameworks |
| 2.3 | Product Strategy | Rumelt Kernel, devil's advocate | frameworks, methods, skills |

### Level 3: Advanced Features (TODO)
| Модуль | Название | Ключевой навык |
|--------|----------|----------------|
| 3.1 | ? | ? |
| 3.2 | ? | ? |
| 3.3 | ? | ? |

---

## Принципы создания модулей

### 1. Interactive Learning
- Студент ДЕЛАЕТ, не только читает
- Каждый шаг требует действия
- Check points заставляют думать

### 2. Real Context
- Все упражнения в контексте TaskFlow
- Реальные PM-задачи
- Артефакты которые можно использовать

### 3. Progressive Complexity
- Каждый модуль строится на предыдущем
- Новые концепции вводятся постепенно
- Повторение через практику

### 4. Socratic Method
- Вопросы перед ответами
- Студент приходит к выводам сам
- Devil's advocate для critical thinking

---

## Паттерны Teaching Script

### Паттерн: Выбор из вариантов
```markdown
**SAY:**
"Какой подход выбираешь?

**A) [Вариант A]** - [описание]
**B) [Вариант B]** - [описание]
**C) [Вариант C]** - [описание]

Скажи 'Выбор A', 'Выбор B' или 'Выбор C'"

**CHECK:** Wait for student choice
```

### Паттерн: Devil's Advocate
```markdown
**SAY:**
"Ты выбрал [X]. Но адвокат дьявола:

**CHALLENGE:**
[Контраргументы]

Зная это:
**A) STICK** - Остаюсь при своём
**B) RECONSIDER** - Пересматриваю

Скажи 'Остаюсь' или 'Пересматриваю'"

**CHECK:** Wait for decision
```

### Паттерн: Параллельные агенты
```markdown
**SAY:**
"Запускаю N агентов для [задача]..."

**ACTION:**
Launch N Task agents in parallel:
- Agent 1: [задача]
- Agent 2: [задача]
- Agent N: [задача]

**Present it like this:**
"Результаты:
**[AGENT 1]:** [summary]
**[AGENT 2]:** [summary]
..."
```

### Паттерн: Создание документа
```markdown
**SAY:**
"Создаю [документ]..."

**ACTION:**
Write file to `path/filename.md` with:
[содержание]

**Present it like this:**
"Готово! Создал `filename.md`

**Содержание:**
[краткое описание]"
```

---

## Checklist создания модуля

- [ ] Определить Learning Objectives (3-5 пунктов)
- [ ] Создать Teaching Script (CLAUDE.md)
- [ ] Создать Slash Command (start-X-Y.md)
- [ ] Подготовить Supporting Materials
- [ ] Добавить Check points после каждого шага
- [ ] Написать Success Criteria
- [ ] Протестировать flow от начала до конца
