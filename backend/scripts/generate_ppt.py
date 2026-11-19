from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[2] / "Automating_Answer_Assessment_PPT_7slides.pptx"

TEAL = RGBColor(0x16, 0x3F, 0x39)
ACCENT = RGBColor(0x1A, 0x7A, 0x6E)
INK = RGBColor(0x1B, 0x2E, 0x29)
MUTED = RGBColor(0x5B, 0x66, 0x60)
CREAM = RGBColor(0xF3, 0xEF, 0xE6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xC8, 0xBE, 0xA8)
SOFT = RGBColor(0xE7, 0xF0, 0xEE)


def set_run(run, text, size=18, bold=False, color=INK):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"


def add_bg(slide, prs):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CREAM
    shape.line.fill.background()


def add_chrome(slide, prs):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.22), prs.slide_height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
    strip.fill.solid()
    strip.fill.fore_color.rgb = ACCENT
    strip.line.fill.background()


def textbox(slide, left, top, width, height):
    box = slide.shapes.add_textbox(left, top, width, height)
    box.text_frame.word_wrap = True
    return box.text_frame


def heading(slide, title):
    tf = textbox(slide, Inches(0.9), Inches(0.4), Inches(11.5), Inches(0.7))
    set_run(tf.paragraphs[0].add_run(), title, 30, True, TEAL)
    rule = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.1), Inches(2.0), Inches(0.05)
    )
    rule.fill.solid()
    rule.fill.fore_color.rgb = ACCENT
    rule.line.fill.background()


def blank_field(slide, label, left, top, width):
    tf = textbox(slide, left, top, width, Inches(0.28))
    set_run(tf.paragraphs[0].add_run(), label, 13, False, MUTED)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top + Inches(0.4), width, Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = LINE
    line.line.fill.background()
    tf2 = textbox(slide, left, top + Inches(0.1), width, Inches(0.32))
    set_run(tf2.paragraphs[0].add_run(), "_______________________________", 15, False, LINE)


def flow_box(slide, left, top, width, height, title, subtitle=""):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = ACCENT
    shape.line.width = Pt(1.5)
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    set_run(tf.paragraphs[0].add_run(), title, 13, True, TEAL)
    if subtitle:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        set_run(p.add_run(), subtitle, 11, False, MUTED)
    return shape


def arrow_right(slide, left, top):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, Inches(0.35), Inches(0.22))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()


def arrow_down(slide, left, top):
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, left, top, Inches(0.22), Inches(0.32))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ----- 1. Title -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)

    tf = textbox(slide, Inches(0.9), Inches(1.05), Inches(11.5), Inches(0.35))
    set_run(tf.paragraphs[0].add_run(), "MAJOR PROJECT  |  5-MINUTE PRESENTATION", 13, True, ACCENT)

    tf = textbox(slide, Inches(0.9), Inches(1.5), Inches(11.5), Inches(1.3))
    set_run(tf.paragraphs[0].add_run(), "Automating Answer Assessment", 38, True, TEAL)
    p = tf.add_paragraph()
    p.space_before = Pt(6)
    set_run(
        p.add_run(),
        "RAG-based model answers with Gemini and dynamic trait evaluation",
        20,
        False,
        MUTED,
    )

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(3.4), Inches(11.2), Inches(3.2)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = LINE

    blank_field(slide, "Name", Inches(1.3), Inches(3.7), Inches(4.8))
    blank_field(slide, "Roll No.", Inches(6.8), Inches(3.7), Inches(4.5))
    blank_field(slide, "Subject", Inches(1.3), Inches(4.75), Inches(4.8))
    blank_field(slide, "Mentor / Guide", Inches(6.8), Inches(4.75), Inches(4.5))

    tf = textbox(slide, Inches(1.3), Inches(5.85), Inches(10), Inches(0.4))
    set_run(
        tf.paragraphs[0].add_run(),
        "Department of Computer Science  |  Academic Year 2025–26",
        13,
        False,
        MUTED,
    )

    # ----- 2. Problem Statement (paragraph) -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)
    heading(slide, "Problem Statement")

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.5), Inches(11.2), Inches(5.1)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = LINE

    tf = textbox(slide, Inches(1.25), Inches(1.85), Inches(10.5), Inches(4.4))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.JUSTIFY
    p.line_spacing = 1.35
    set_run(
        p.add_run(),
        "Evaluating descriptive answers manually is time-consuming and often inconsistent, "
        "because different teachers may award different marks for similar responses. In many "
        "classrooms, the reference “model answer” is either written once and reused, or created "
        "from memory, so it may not fully match the actual textbook content taught to students. "
        "Students also receive limited guidance on why marks were deducted—whether due to missing "
        "concepts, weak structure, poor wording, or grammar issues. This project addresses that "
        "gap by automatically building a textbook-grounded model answer using Retrieval-Augmented "
        "Generation (RAG), then comparing the student’s response against it to produce a fair "
        "score and clear, improvement-focused feedback.",
        20,
        False,
        INK,
    )

    # ----- 3. Solution Overview -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)
    heading(slide, "Our Solution")

    points = [
        ("Textbook-grounded grading", "Model answers are generated from uploaded textbooks using RAG, not from generic AI memory alone."),
        ("Explainable scoring", "Answers are judged on content, coherence, vocabulary, and grammar with clear improvement tips."),
        ("Teacher–student workflow", "Teachers share textbooks; students submit answers; history is saved for review."),
        ("Modern full-stack system", "React frontend, FastAPI backend, Gemini AI, Firebase Auth, and MongoDB storage."),
    ]
    y = 1.45
    for title, desc in points:
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(y), Inches(11.2), Inches(1.15)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = LINE
        tf = textbox(slide, Inches(1.2), Inches(y + 0.18), Inches(10.6), Inches(0.85))
        set_run(tf.paragraphs[0].add_run(), title, 18, True, TEAL)
        p = tf.add_paragraph()
        p.space_before = Pt(4)
        set_run(p.add_run(), desc, 16, False, INK)
        y += 1.3

    # ----- 4. Flowchart -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)
    heading(slide, "System Flow")

    # Row 1
    flow_box(slide, Inches(0.7), Inches(1.55), Inches(2.4), Inches(1.05), "1. Login", "Firebase Auth")
    arrow_right(slide, Inches(3.2), Inches(1.95))
    flow_box(slide, Inches(3.65), Inches(1.55), Inches(2.5), Inches(1.05), "2. Upload Textbook", "PDF / TXT")
    arrow_right(slide, Inches(6.25), Inches(1.95))
    flow_box(slide, Inches(6.7), Inches(1.55), Inches(2.6), Inches(1.05), "3. Index with RAG", "Chunk + Embed")
    arrow_right(slide, Inches(9.4), Inches(1.95))
    flow_box(slide, Inches(9.85), Inches(1.55), Inches(2.6), Inches(1.05), "4. Ask + Answer", "Student input")

    arrow_down(slide, Inches(10.9), Inches(2.75))

    # Row 2 (right to left visually continuing)
    flow_box(slide, Inches(9.85), Inches(3.2), Inches(2.6), Inches(1.05), "5. Retrieve Context", "Top-k passages")
    # left arrow
    shape = slide.shapes.add_shape(
        MSO_SHAPE.LEFT_ARROW, Inches(9.35), Inches(3.6), Inches(0.35), Inches(0.22)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()
    flow_box(slide, Inches(6.6), Inches(3.2), Inches(2.6), Inches(1.05), "6. Model Answer", "Gemini + RAG")
    shape = slide.shapes.add_shape(
        MSO_SHAPE.LEFT_ARROW, Inches(6.1), Inches(3.6), Inches(0.35), Inches(0.22)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()
    flow_box(slide, Inches(3.35), Inches(3.2), Inches(2.6), Inches(1.05), "7. Dynamic Traits", "Weighted scoring")
    shape = slide.shapes.add_shape(
        MSO_SHAPE.LEFT_ARROW, Inches(2.85), Inches(3.6), Inches(0.35), Inches(0.22)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()
    flow_box(slide, Inches(0.7), Inches(3.2), Inches(2.0), Inches(1.05), "8. Feedback", "Score + tips")

    note = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(4.7), Inches(11.75), Inches(2.0)
    )
    note.fill.solid()
    note.fill.fore_color.rgb = SOFT
    note.line.color.rgb = ACCENT
    tf = textbox(slide, Inches(1.0), Inches(4.95), Inches(11.2), Inches(1.55))
    set_run(tf.paragraphs[0].add_run(), "In one line:", 16, True, TEAL)
    p = tf.add_paragraph()
    p.space_before = Pt(6)
    set_run(
        p.add_run(),
        "Textbook → RAG retrieval → Gemini model answer → trait-based evaluation → saved history "
        "(MongoDB) for teachers and students.",
        17,
        False,
        INK,
    )

    # ----- 5. Dynamic Traits -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)
    heading(slide, "Dynamic Evaluation Traits")

    tf = textbox(slide, Inches(0.9), Inches(1.3), Inches(11.3), Inches(1.0))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.JUSTIFY
    set_run(
        p.add_run(),
        "Dynamic traits means the system does not use fixed marks for every question. Based on the "
        "question type, Gemini first assigns weightage (out of 100%) to four traits, then grades "
        "the student answer against the model answer using those weights.",
        17,
        False,
        INK,
    )

    traits = [
        ("Content Accuracy", "Are facts complete and correct compared to the textbook-based model answer?"),
        ("Coherence & Structure", "Does the answer flow logically with clear organization?"),
        ("Vocabulary & Clarity", "Are words precise, academic, and easy to understand?"),
        ("Grammar & Language", "Are sentences grammatically correct and readable?"),
    ]
    positions = [
        (0.9, 2.5),
        (7.0, 2.5),
        (0.9, 4.7),
        (7.0, 4.7),
    ]
    for (title, desc), (x, y) in zip(traits, positions):
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.4), Inches(1.85)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = ACCENT
        tf = textbox(slide, Inches(x + 0.25), Inches(y + 0.3), Inches(4.9), Inches(1.35))
        set_run(tf.paragraphs[0].add_run(), title, 18, True, TEAL)
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        set_run(p.add_run(), desc, 15, False, INK)

    # ----- 6. Tech + Demo (short) -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)
    heading(slide, "Implementation & Demo")

    left = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.45), Inches(5.6), Inches(5.2)
    )
    left.fill.solid()
    left.fill.fore_color.rgb = WHITE
    left.line.color.rgb = LINE
    tf = textbox(slide, Inches(1.2), Inches(1.7), Inches(5.1), Inches(4.7))
    set_run(tf.paragraphs[0].add_run(), "Tech Stack", 20, True, TEAL)
    for item in [
        "React + TypeScript frontend",
        "FastAPI REST backend",
        "Google Gemini (LLM + embeddings)",
        "RAG with local vector search",
        "Firebase Authentication",
        "MongoDB history storage",
    ]:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        set_run(p.add_run(), f"• {item}", 16, False, INK)

    right = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.45), Inches(5.6), Inches(5.2)
    )
    right.fill.solid()
    right.fill.fore_color.rgb = WHITE
    right.line.color.rgb = LINE
    tf = textbox(slide, Inches(7.1), Inches(1.7), Inches(5.1), Inches(4.7))
    set_run(tf.paragraphs[0].add_run(), "Live Demo Steps", 20, True, TEAL)
    for item in [
        "Login as teacher/student",
        "Upload a textbook",
        "Enter question + student answer",
        "View model answer & sources",
        "See trait weights, score, feedback",
        "Check saved evaluation history",
    ]:
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        set_run(p.add_run(), f"• {item}", 16, False, INK)

    # ----- 7. Conclusion -----
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, prs)
    add_chrome(slide, prs)
    heading(slide, "Conclusion")

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.45), Inches(11.2), Inches(3.6)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = LINE
    tf = textbox(slide, Inches(1.25), Inches(1.75), Inches(10.5), Inches(3.1))
    points = [
        "We automated descriptive answer assessment using RAG and Gemini.",
        "Model answers stay grounded in the actual textbook content.",
        "Dynamic traits make scoring adaptive and feedback easy to understand.",
        "The system supports real teacher–student use with auth and history.",
    ]
    first = True
    for item in points:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(12)
        set_run(p.add_run(), f"• {item}", 18, False, INK)

    tf = textbox(slide, Inches(0.9), Inches(5.4), Inches(11.2), Inches(1.2))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), "Thank You", 34, True, TEAL)
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(8)
    set_run(p.add_run(), "Questions are welcome", 18, False, MUTED)

    prs.save(OUT)
    print(f"saved {OUT}")
    print(f"slides={len(prs.slides)}")


if __name__ == "__main__":
    main()
