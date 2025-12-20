#!/usr/bin/env python3
"""Create PDF with Claude Code PM Methods using ReportLab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Arial Unicode font for Russian text
pdfmetrics.registerFont(TTFont('ArialUni', '/Library/Fonts/Arial Unicode.ttf'))

def create_pdf():
    output_path = '/Users/lance/Documents/claude-code-course/lesson-modules/claude-code-pm-methods.pdf'
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           leftMargin=1.5*cm, rightMargin=1.5*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                 fontName='ArialUni', fontSize=28,
                                 textColor=HexColor('#2F5496'),
                                 alignment=1, spaceAfter=20)

    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
                                    fontName='ArialUni', fontSize=16,
                                    textColor=HexColor('#666666'),
                                    alignment=1, spaceAfter=30)

    chapter_style = ParagraphStyle('Chapter', parent=styles['Heading1'],
                                   fontName='ArialUni', fontSize=20,
                                   textColor=HexColor('#2F5496'),
                                   spaceBefore=20, spaceAfter=15)

    section_style = ParagraphStyle('Section', parent=styles['Heading2'],
                                   fontName='ArialUni', fontSize=14,
                                   textColor=HexColor('#404040'),
                                   spaceBefore=15, spaceAfter=8)

    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                fontName='ArialUni', fontSize=10,
                                textColor=HexColor('#000000'),
                                spaceBefore=3, spaceAfter=5,
                                leading=14)

    code_style = ParagraphStyle('Code', parent=styles['Normal'],
                                fontName='ArialUni', fontSize=9,
                                textColor=HexColor('#404040'),
                                backColor=HexColor('#F5F5F5'),
                                spaceBefore=3, spaceAfter=5,
                                leftIndent=10)

    highlight_style = ParagraphStyle('Highlight', parent=styles['Normal'],
                                     fontName='ArialUni', fontSize=10,
                                     textColor=HexColor('#2F5496'),
                                     spaceBefore=5, spaceAfter=5)

    # Build document content
    content = []

    # Title page
    content.append(Spacer(1, 3*inch))
    content.append(Paragraph('Claude Code', title_style))
    content.append(Paragraph('для Product Managers', title_style))
    content.append(Spacer(1, 0.5*inch))
    content.append(Paragraph('Справочник методов и техник', subtitle_style))
    content.append(Spacer(1, 1*inch))
    content.append(Paragraph('Module 2 Complete', subtitle_style))
    content.append(PageBreak())

    # MODULE 2.1
    content.append(Paragraph('МОДУЛЬ 2.1: НАПИСАНИЕ PRD', chapter_style))

    content.append(Paragraph('@-mentions (Контекстные ссылки)', section_style))
    content.append(Paragraph('Что это: Подключение файлов и контекста к разговору через @', body_style))
    content.append(Paragraph('Как использовать:', body_style))
    content.append(Paragraph('@company-context/PRODUCT.md - подключить контекст<br/>@templates/prd-template.md - использовать шаблон<br/>@user-research/interviews.md - добавить исследования', code_style))
    content.append(Paragraph('Когда применять:<br/>• Написание PRD с контекстом компании<br/>• Использование шаблонов документов<br/>• Подключение user research к анализу', body_style))

    content.append(Paragraph('Параллельные агенты', section_style))
    content.append(Paragraph('Что это: Запуск нескольких AI-агентов одновременно для генерации вариантов', body_style))
    content.append(Paragraph('"Запусти 3 агента для генерации 3 разных подходов к PRD"', code_style))
    content.append(Paragraph('Преимущества:<br/>• Экономия времени (параллельно, не последовательно)<br/>• Разнообразие подходов<br/>• Возможность выбрать лучший вариант', body_style))

    content.append(Paragraph('Multi-perspective Review (Sub-agents)', section_style))
    content.append(Paragraph('Что это: Получение feedback от разных "персон" через агентов', body_style))
    content.append(Paragraph('Доступные агенты:<br/>• Engineer - Техническая feasibility<br/>• Executive - Бизнес-impact<br/>• User Researcher - User needs', body_style))
    content.append(Paragraph('"Получи ревью от engineer, executive и user researcher"', code_style))
    content.append(PageBreak())

    # MODULE 2.2
    content.append(Paragraph('МОДУЛЬ 2.2: АНАЛИЗ ДАННЫХ', chapter_style))

    content.append(Paragraph('CSV/Data Analysis', section_style))
    content.append(Paragraph('Что это: Анализ данных из CSV файлов через Claude Code', body_style))
    content.append(Paragraph('Типичные задачи:<br/>• Анализ воронок конверсии<br/>• Поиск drop-off точек<br/>• Расчёт метрик (conversion rates, retention)', body_style))

    content.append(Paragraph('Сегментация данных', section_style))
    content.append(Paragraph('Что это: Разбивка данных по сегментам для deeper insights', body_style))
    content.append(Paragraph('Типы сегментации:<br/>• По размеру компании (SMB, Mid-market, Enterprise)<br/>• По роли (PM, Engineer, Designer, Manager)<br/>• По индустрии<br/>• По cohort/времени', body_style))
    content.append(Paragraph('Ключевой инсайт: Topline метрики часто маскируют segment wins/losses', highlight_style))

    content.append(Paragraph('ROI Моделирование', section_style))
    content.append(Paragraph('Что это: Построение финансовых моделей для оценки impact', body_style))
    content.append(Paragraph('Impact = Users Affected x Current Rate x Expected Lift x Value', code_style))
    content.append(Paragraph('Три сценария:<br/>• Pessimistic - Всё идёт плохо (minimum case)<br/>• Realistic - Ожидаемый результат (baseline)<br/>• Optimistic - Всё идёт отлично (upside)', body_style))

    content.append(Paragraph('A/B Test Analysis', section_style))
    content.append(Paragraph('Процесс анализа:<br/>1. Topline результаты<br/>2. Сегментация по ключевым dimensions<br/>3. Quality metrics для активированных<br/>4. Leading indicators<br/>5. Рекомендация (ship/iterate/kill)', body_style))
    content.append(PageBreak())

    # MODULE 2.3
    content.append(Paragraph('МОДУЛЬ 2.3: ПРОДУКТОВАЯ СТРАТЕГИЯ', chapter_style))

    content.append(Paragraph('Competitive Research (Parallel Agents)', section_style))
    content.append(Paragraph('Что это: Быстрое исследование конкурентов через параллельных агентов', body_style))
    content.append(Paragraph('Что исследовать:<br/>• Запущенные фичи<br/>• Ценообразование и positioning<br/>• Целевая аудитория<br/>• Стратегическое направление', body_style))
    content.append(Paragraph('Результат: Competitive landscape за минуты вместо часов', highlight_style))

    content.append(Paragraph("Rumelt's Strategy Kernel", section_style))
    content.append(Paragraph('Фреймворк для разработки стратегии из трёх компонентов:', body_style))
    content.append(Paragraph('1. ДИАГНОЗ - "Что на самом деле происходит?"', highlight_style))
    content.append(Paragraph('   Идентифицирует ядро проблемы/возможности', body_style))
    content.append(Paragraph('2. РУКОВОДЯЩАЯ ПОЛИТИКА - "Какой наш подход?"', highlight_style))
    content.append(Paragraph('   Делает жёсткие выборы, говорит НЕТ некоторым возможностям', body_style))
    content.append(Paragraph('3. СОГЛАСОВАННЫЕ ДЕЙСТВИЯ - "Как мы исполняем?"', highlight_style))
    content.append(Paragraph('   Конкретные инициативы, усиливающие друг друга', body_style))

    content.append(Paragraph("Devil's Advocate", section_style))
    content.append(Paragraph('Техника pressure-testing решений:<br/>1. Принять решение<br/>2. Получить challenge с контраргументами<br/>3. Либо защитить решение, либо пересмотреть<br/>4. Финальное решение более robust', body_style))

    content.append(Paragraph('Skills (Трансформация документов)', section_style))
    content.append(Paragraph('Доступные skills:<br/>• pptx - PowerPoint для executive presentations<br/>• xlsx - Excel для финансовых моделей<br/>• pdf - PDF для формальных документов<br/>• docx - Word для отчётов', body_style))
    content.append(PageBreak())

    # Key principle
    content.append(Paragraph('КЛЮЧЕВОЙ ПРИНЦИП', chapter_style))
    content.append(Spacer(1, 0.5*inch))

    key_principle = ParagraphStyle('KeyPrinciple', parent=styles['Normal'],
                                   fontName='ArialUni', fontSize=16,
                                   textColor=HexColor('#2F5496'),
                                   alignment=1, spaceBefore=20, spaceAfter=20)
    content.append(Paragraph('AI не заменяет PM-мышление.<br/>AI усиливает его.', key_principle))
    content.append(Spacer(1, 0.3*inch))
    content.append(Paragraph('• PRD - ты выбираешь подход и принимаешь feedback<br/>• Данные - ты задаёшь вопросы и интерпретируешь<br/>• Стратегия - ты делаешь tradeoffs и защищаешь решения', body_style))
    content.append(Spacer(1, 0.3*inch))
    content.append(Paragraph('AI ускоряет исследования, генерацию вариантов, stress-testing. Но judgment остаётся твоим.', body_style))
    content.append(PageBreak())

    # Checklist
    content.append(Paragraph('ЧЕКЛИСТ ПРИМЕНЕНИЯ', chapter_style))

    content.append(Paragraph('При написании PRD:', section_style))
    content.append(Paragraph('☐ Подключить контекст через @-mentions<br/>☐ Сгенерировать варианты через parallel agents<br/>☐ Получить multi-perspective review<br/>☐ Итерировать на основе feedback', body_style))

    content.append(Paragraph('При анализе данных:', section_style))
    content.append(Paragraph('☐ Начать с topline метрик<br/>☐ Сегментировать по ключевым dimensions<br/>☐ Проверить quality metrics<br/>☐ Построить ROI модель с 3 сценариями', body_style))

    content.append(Paragraph('При разработке стратегии:', section_style))
    content.append(Paragraph("☐ Исследовать конкурентов (parallel agents)<br/>☐ Применить Rumelt's Kernel<br/>☐ Pressure-test через devil's advocate<br/>☐ Создать executive presentation (pptx skill)", body_style))

    # Build PDF
    doc.build(content)
    print(f'PDF saved to: {output_path}')
    return output_path

if __name__ == '__main__':
    create_pdf()
