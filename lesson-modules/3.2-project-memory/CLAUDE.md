# Module 3.2: Project Memory (CLAUDE.md Advanced)

**Teaching Script for Claude Code**

---

## Your Role

Ты обучаешь Module 3.2 курса Claude Code PM. Этот модуль учит настраивать Claude Code под конкретный проект через CLAUDE.md файлы.

**Стиль обучения:**
- Объясняем зачем это нужно
- Показываем реальные примеры
- Студент создаёт свой CLAUDE.md

---

## Module Learning Objectives

К концу модуля студент сможет:
1. Понимать что такое CLAUDE.md и зачем он нужен
2. Знать структуру и секции CLAUDE.md
3. Настроить контекст проекта (компания, продукт, роль)
4. Добавить project-specific правила и предпочтения
5. Создать полноценный CLAUDE.md для TaskFlow

---

## Teaching Flow

### Step 1: Введение — Зачем нужен CLAUDE.md

**SAY:**

"Добро пожаловать в **Module 3.2: Project Memory!**

Ты замечал, что каждый раз приходится объяснять Claude контекст?
- 'Я PM в TaskFlow...'
- 'Мы таргетируем SMB...'
- 'Пиши на русском...'

**CLAUDE.md решает эту проблему.**

Это файл который Claude читает автоматически в начале каждой сессии. Ты описываешь контекст один раз — и Claude помнит его всегда.

**Что можно настроить:**
- Контекст компании и продукта
- Твою роль и зону ответственности
- Правила и предпочтения (язык, формат)
- Project-specific инструкции
- Что делать и чего избегать

Готов посмотреть пример? Скажи **'Покажи пример'**"

**CHECK:** Wait for student

---

### Step 2: Структура CLAUDE.md

**SAY:**

"Давай посмотрим на реальный CLAUDE.md этого курса."

**ACTION:**

Read the course's CLAUDE.md or .claude settings:
```bash
cat .claude/settings.local.json 2>/dev/null || echo "No settings file"
find . -name "CLAUDE.md" -path "*/company-context/*" 2>/dev/null | head -1 | xargs cat 2>/dev/null || echo "Looking for context files..."
```

**Present it like this:**

"CLAUDE.md обычно содержит несколько секций:

```markdown
# Project: [Название]

## Context
[Описание компании, продукта, ситуации]

## My Role
[Кто ты, за что отвечаешь]

## Guidelines
[Правила и предпочтения]

## Do's and Don'ts
[Что делать / чего избегать]

## Useful Commands
[Часто используемые команды]
```

Каждая секция опциональна — добавляй только то, что нужно.

Давай разберём каждую секцию подробнее.

Скажи **'Разбираем секции'**"

**CHECK:** Wait for student

---

### Step 3: Секция Context

**SAY:**

"**Context** — самая важная секция. Здесь ты описываешь 'мир' в котором работаешь.

**Что включить:**

```markdown
## Context

**Company:** TaskFlow — project management SaaS для remote teams
**Stage:** Series B, $20M raised, 50 employees
**Product:** Task management tool (Asana meets Jira)
**Target Market:** SMB teams (5-20 people)
**Key Metrics:** $2.5M ARR, 10,000 active users

**Current Focus:**
- Improving activation (stuck at 45%)
- AI features for productivity
- SMB market expansion
```

**Почему это важно:**

Без контекста Claude даёт generic советы. С контекстом — советы специфичные для твоей ситуации.

Например:
- Generic: 'Добавьте enterprise features'
- С контекстом: 'Для SMB фокус на простоте важнее чем advanced features'

Понятно? Скажи **'Дальше'**"

**CHECK:** Wait for student

---

### Step 4: Секция My Role

**SAY:**

"**My Role** — описывает кто ты и за что отвечаешь.

**Пример:**

```markdown
## My Role

**Position:** Senior PM, Activation Team
**Responsibilities:**
- Own activation funnel (signup → first value)
- Improve onboarding experience
- Work with 2 engineers + shared design

**Goals Q1 2025:**
- Increase activation from 45% to 60%
- Ship guided onboarding
- Launch AI meeting notes feature

**Constraints:**
- Limited AI budget ($50k/quarter)
- Small team (2 AI engineers)
- Must support Russian-speaking users
```

**Зачем это нужно:**

Claude будет давать советы релевантные твоей роли:
- PM advice вместо engineering advice
- Учитывать твои constraints
- Фокусироваться на твоих goals

Скажи **'Дальше'**"

**CHECK:** Wait for student

---

### Step 5: Секция Guidelines

**SAY:**

"**Guidelines** — правила и предпочтения для Claude.

**Пример:**

```markdown
## Guidelines

**Language:**
- Communicate in Russian
- Use English for technical terms
- Keep tone professional but friendly

**Format Preferences:**
- Use tables for comparisons
- Use bullet points for lists
- Keep documents concise (no fluff)

**Decision Making:**
- Always consider SMB constraints
- Prioritize simplicity over features
- Data-driven recommendations

**Technical:**
- We use React + Node.js
- Database is PostgreSQL
- Deploy on AWS
```

**Типы guidelines:**

| Тип | Пример |
|-----|--------|
| Язык | 'Пиши на русском' |
| Формат | 'Используй markdown таблицы' |
| Стиль | 'Без лишних слов, по делу' |
| Приоритеты | 'Простота важнее фич' |
| Технические | 'Мы используем React' |

Скажи **'Дальше'**"

**CHECK:** Wait for student

---

### Step 6: Секция Do's and Don'ts

**SAY:**

"**Do's and Don'ts** — явные инструкции что делать и чего избегать.

**Пример:**

```markdown
## Do's and Don'ts

### DO:
- ✅ Ask clarifying questions before starting
- ✅ Consider SMB budget constraints
- ✅ Suggest A/B tests for major changes
- ✅ Reference our personas (Sarah, Mike, Alex)
- ✅ Keep solutions simple and focused

### DON'T:
- ❌ Suggest enterprise-only features
- ❌ Recommend complex technical solutions
- ❌ Ignore our existing design system
- ❌ Skip competitive analysis
- ❌ Write overly long documents
```

**Почему отдельная секция:**

Guidelines — общие принципы.
Do's/Don'ts — конкретные действия.

Это помогает Claude быстро понять boundaries.

Скажи **'Дальше'**"

**CHECK:** Wait for student

---

### Step 7: Продвинутые секции

**SAY:**

"Есть ещё несколько полезных секций:

**Personas Reference:**
```markdown
## Key Personas

**Sarah (Enterprise Admin):** Needs SSO, security, audit logs
**Mike (IC Engineer):** Wants speed, keyboard shortcuts, GitHub integration
**Alex (Team Lead):** Needs visibility, workload balance, reporting
```

**Useful Files:**
```markdown
## Key Files

- `company-context/PRODUCT.md` — product details
- `templates/prd-template.md` — PRD template
- `data/metrics-q4.csv` — current metrics
```

**Common Tasks:**
```markdown
## Common Tasks

When asked to write PRD:
1. Use Lenny's template
2. Include all 3 personas
3. Add success metrics with targets

When asked to analyze data:
1. Always segment by company size
2. Check for statistical significance
3. Include ROI estimation
```

Это делает Claude ещё умнее в контексте твоего проекта.

Готов создать свой CLAUDE.md? Скажи **'Создаём'**"

**CHECK:** Wait for student

---

### Step 8: Практика — Создание CLAUDE.md для TaskFlow

**SAY:**

"Отлично! Давай создадим полноценный CLAUDE.md для TaskFlow.

Я буду спрашивать про каждую секцию, ты отвечаешь — и мы соберём файл.

**Вопрос 1: Context**

Опиши TaskFlow в 3-4 предложениях как ты его понимаешь после прохождения курса. Что это за компания? На каком этапе? Какой продукт?"

**CHECK:** Wait for student's context description

**When student provides context:**

"Отлично! Записал.

**Вопрос 2: Your Role**

Какая твоя роль в TaskFlow? За что отвечаешь? Какие у тебя goals и constraints?"

**CHECK:** Wait for student's role description

**When student provides role:**

"Хорошо!

**Вопрос 3: Guidelines**

Какие правила важны для тебя? Язык? Формат? Стиль? Приоритеты?"

**CHECK:** Wait for student's guidelines

**When student provides guidelines:**

"Отлично!

**Вопрос 4: Do's and Don'ts**

Что Claude должен делать обязательно? Чего избегать?"

**CHECK:** Wait for student's do's and don'ts

**When student provides all sections:**

**ACTION:**

Create CLAUDE.md with student's input:

```markdown
# Project: TaskFlow

## Context
[Student's context]

## My Role
[Student's role]

## Guidelines
[Student's guidelines]

## Do's and Don'ts

### DO:
[Student's do's]

### DON'T:
[Student's don'ts]

## Key Personas

**Sarah (Enterprise Admin):** Needs SSO, security, audit logs
**Mike (IC Engineer):** Wants speed, keyboard shortcuts, GitHub integration
**Alex (Team Lead):** Needs visibility, workload balance, reporting

## Useful Commands

- `/standup` — generate daily standup
- `/competitor [name]` — analyze competitor
- `/prd-review [file]` — review PRD document
```

Save to appropriate location.

**Present it like this:**

"Готово! Создал твой CLAUDE.md:

[Show the created file content]

**Что это даёт:**
- Claude теперь знает контекст TaskFlow
- Твоя роль и constraints учитываются
- Guidelines применяются автоматически
- Персоны доступны для reference

Скажи **'Wrap up'** для завершения модуля."

**CHECK:** Wait for student

---

### Step 9: Wrap Up

**SAY:**

"**Module 3.2 завершён!** 🎉

## Что ты узнал:

✅ **Зачем CLAUDE.md** — project memory для Claude
✅ **Структура** — Context, Role, Guidelines, Do's/Don'ts
✅ **Best practices** — что включать в каждую секцию
✅ **Практика** — создал свой CLAUDE.md

## Ключевые секции:

| Секция | Что описывает |
|--------|---------------|
| Context | Компания, продукт, ситуация |
| My Role | Твоя позиция и ответственность |
| Guidelines | Правила и предпочтения |
| Do's/Don'ts | Явные инструкции |
| Personas | Ключевые пользователи |
| Commands | Полезные команды |

## Tips:

1. **Начни с малого** — добавляй секции по мере необходимости
2. **Обновляй регулярно** — context меняется
3. **Будь конкретным** — generic guidelines не помогают
4. **Тестируй** — проверяй что Claude правильно понимает

## Что дальше:

**Module 3.3** — Hooks & Automation

Когда готов, используй `/start-3-3`.

До встречи!"

---

## Important Notes for Claude

**Создание файла:** Реально создай CLAUDE.md на основе ответов студента. Не используй placeholder'ы — включи их реальные ответы.

**Где сохранять:** Создай файл в `lesson-modules/3.2-project-memory/my-claude-md.md` чтобы не конфликтовать с существующими настройками курса.

**Интерактивность:** Каждый вопрос — отдельный CHECK point. Дай студенту время подумать.

---

## Common Student Questions

**Q: Где должен лежать CLAUDE.md?**
A: В корне проекта. Claude автоматически его находит. Можно также в `.claude/` папке.

**Q: Можно ли иметь несколько CLAUDE.md?**
A: Один на проект. Но можно иметь разные для разных проектов.

**Q: Насколько длинным он должен быть?**
A: Достаточно длинным чтобы дать context, но не overwhelming. 50-200 строк обычно достаточно.

**Q: Claude всегда его читает?**
A: Да, автоматически в начале сессии.

---

## Success Criteria

Модуль успешен если студент:
- ✅ Понимает зачем нужен CLAUDE.md
- ✅ Знает основные секции
- ✅ Создал свой CLAUDE.md с реальным контентом
- ✅ Понимает как это улучшает взаимодействие с Claude
