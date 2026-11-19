from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).resolve().parents[2] / "sample_textbook_20pages.pdf"


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=18,
        alignment=TA_CENTER,
    )
    h1 = ParagraphStyle(
        "H1Custom",
        parent=styles["Heading1"],
        fontSize=16,
        spaceBefore=14,
        spaceAfter=10,
    )
    h2 = ParagraphStyle(
        "H2Custom",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=10,
        spaceAfter=8,
    )
    body = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )

    story: list = []

    chapters = [
        (
            "Chapter 1: The Indus Valley Civilization",
            [
                (
                    "Overview",
                    "The Indus Valley Civilization (c. 3300-1300 BCE) was one of the world's earliest urban civilizations. "
                    "It developed along the Indus River and nearby regions in present-day Pakistan and northwest India. "
                    "Archaeologists regard it as a major Bronze Age culture because of its planned cities, craft specialization, "
                    "long-distance trade, and distinctive material culture. The civilization is also called the Harappan Civilization "
                    "after the site of Harappa, which was among the first excavated settlements.",
                ),
                (
                    "Urban Planning",
                    "Cities such as Mohenjo-Daro and Harappa had carefully planned grid layouts. Streets were often oriented "
                    "north-south and east-west, creating rectangular blocks. Houses were built with baked bricks of standardized "
                    "proportions. Many homes had private wells, bathing areas, and covered drains that connected to larger street drains. "
                    "This advanced drainage system shows civic planning and collective maintenance of public infrastructure.",
                ),
                (
                    "Public Architecture",
                    "Important public structures include the Great Bath at Mohenjo-Daro, large granaries, citadel mounds, "
                    "and assembly areas. The Great Bath appears to have had ritual or communal significance. The presence of "
                    "uniform building techniques across distant sites suggests shared standards and organized administration.",
                ),
                (
                    "Trade and Economy",
                    "The civilization engaged in extensive trade with Mesopotamia and surrounding regions. Standardized weights "
                    "and measures supported commercial exchange. Crafts such as bead making, pottery, shell working, and metallurgy "
                    "were important economic activities. Seals with animal motifs and short inscriptions were likely used in trade "
                    "and administration.",
                ),
                (
                    "Writing and Society",
                    "A script, still undeciphered, was used for communication and record-keeping. Evidence suggests a well-organized "
                    "society with less clear proof of a strong centralized monarchy. Public works and uniform planning point to "
                    "organized civic administration. The civilization declined due to factors such as climate change, river shifts, "
                    "or possible invasions, yet it remains significant for early urban development.",
                ),
                (
                    "Decline and Legacy",
                    "By the later Harappan phase, many urban centers shrank or were abandoned. Scholars debate whether ecological "
                    "stress, tectonic change, altered river courses, or social transformation played the largest role. "
                    "Even after urban decline, cultural practices continued in regional forms. The Indus tradition influenced later "
                    "settlement patterns and remains a foundation for understanding South Asian protohistory.",
                ),
            ],
        ),
        (
            "Chapter 2: Foundations of Neural Networks",
            [
                (
                    "What Is a Neural Network?",
                    "A neural network is a computational model inspired by the structure and function of the human brain. "
                    "It consists of layers of interconnected nodes called neurons. Each connection has a weight that determines "
                    "signal strength, and each neuron may include a bias that fine-tunes activation. Neural networks learn patterns "
                    "from data rather than relying only on hand-written rules.",
                ),
                (
                    "Layers and Information Flow",
                    "The input layer receives raw data for processing. Hidden layers perform computations, extract patterns, "
                    "and transform information using weights, biases, and activation functions. The output layer produces the final "
                    "result based on learned patterns. Deep networks contain many hidden layers and can model complex relationships.",
                ),
                (
                    "Learning and Optimization",
                    "Neural networks learn through training using algorithms such as backpropagation. An optimizer like gradient "
                    "descent updates parameters to reduce a loss function. Training involves forward pass prediction, loss calculation, "
                    "backward pass gradient computation, and parameter updates. Regularization methods help reduce overfitting.",
                ),
                (
                    "Activation Functions",
                    "Activation functions introduce non-linearity so networks can learn complex mappings. Common examples include "
                    "sigmoid, tanh, ReLU, and softmax. ReLU is widely used in hidden layers because it is computationally efficient "
                    "and helps mitigate vanishing gradients in many practical settings.",
                ),
                (
                    "Applications",
                    "Neural networks power applications in image recognition, natural language processing, speech recognition, "
                    "recommendation systems, medical diagnosis support, and autonomous control. Architectures such as convolutional "
                    "networks, recurrent networks, and transformers specialize in different data types and tasks.",
                ),
                (
                    "Practical Challenges",
                    "Successful training depends on data quality, hyperparameter choices, compute resources, and careful evaluation. "
                    "Poor labels, class imbalance, or leakage can distort results. Practitioners monitor validation metrics, use "
                    "early stopping, and compare baselines before deploying a model.",
                ),
            ],
        ),
        (
            "Chapter 3: Photosynthesis and Energy in Plants",
            [
                (
                    "Purpose of Photosynthesis",
                    "Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into "
                    "chemical energy stored in glucose. This process sustains most food chains on Earth because it produces organic "
                    "matter and releases oxygen as a by-product.",
                ),
                (
                    "Key Inputs and Outputs",
                    "The overall reaction uses carbon dioxide and water in the presence of sunlight and chlorophyll to form glucose "
                    "and oxygen. Chloroplasts contain thylakoid membranes where light-dependent reactions occur and stroma where "
                    "the Calvin cycle synthesizes sugars.",
                ),
                (
                    "Light-Dependent Reactions",
                    "In the thylakoid membrane, photosystems capture photons and excite electrons. Water molecules are split, "
                    "releasing oxygen, protons, and electrons. The electron transport chain helps create a proton gradient used "
                    "by ATP synthase to produce ATP. NADPH is also generated for use in carbon fixation.",
                ),
                (
                    "Calvin Cycle",
                    "The Calvin cycle fixes carbon dioxide into carbohydrates using ATP and NADPH. Rubisco catalyzes the initial "
                    "carboxylation step. Through reduction and regeneration phases, the cycle produces glyceraldehyde-3-phosphate, "
                    "which can form glucose and other organic molecules.",
                ),
                (
                    "Environmental Influences",
                    "Light intensity, carbon dioxide concentration, temperature, and water availability affect photosynthetic rate. "
                    "Extreme heat or drought can close stomata and reduce carbon intake. Understanding these limits helps agriculture "
                    "and climate science.",
                ),
                (
                    "Importance for Ecosystems",
                    "Photosynthesis supports ecological energy flow, atmospheric oxygen balance, and carbon cycling. Forests, "
                    "phytoplankton, and crop systems all depend on photosynthetic productivity. Human activity that alters land use "
                    "or climate can therefore reshape global carbon dynamics.",
                ),
            ],
        ),
        (
            "Chapter 4: The Water Cycle and Climate",
            [
                (
                    "Components of the Water Cycle",
                    "The water cycle describes continuous movement of water among atmosphere, land, and oceans. Major processes "
                    "include evaporation, condensation, precipitation, infiltration, runoff, and transpiration. Energy from the sun "
                    "drives much of this circulation.",
                ),
                (
                    "Evaporation and Transpiration",
                    "Evaporation converts liquid water into vapor from oceans, lakes, and soils. Transpiration releases water vapor "
                    "from plant leaves. Together they are often called evapotranspiration and strongly influence regional humidity.",
                ),
                (
                    "Cloud Formation and Precipitation",
                    "As moist air rises and cools, water vapor condenses around particles to form clouds. When droplets grow large "
                    "enough, precipitation falls as rain, snow, sleet, or hail. Mountain ranges and ocean currents can shape local "
                    "rainfall patterns.",
                ),
                (
                    "Groundwater and Runoff",
                    "Some precipitation infiltrates soil and recharges groundwater aquifers. Excess water becomes surface runoff "
                    "that enters streams and rivers. Human extraction, paving, and deforestation can change infiltration rates and "
                    "increase flood risk.",
                ),
                (
                    "Climate Connections",
                    "The water cycle is tightly linked to climate systems. Warming temperatures can intensify evaporation and "
                    "extreme rainfall events. Droughts, glacial melt, and shifting monsoon patterns are important research topics.",
                ),
                (
                    "Stewardship",
                    "Sustainable water management requires protecting watersheds, reducing pollution, and using water efficiently "
                    "in agriculture and cities. Monitoring rainfall, river discharge, and aquifer levels supports informed policy.",
                ),
            ],
        ),
        (
            "Chapter 5: Democratic Institutions and Citizenship",
            [
                (
                    "Meaning of Democracy",
                    "Democracy is a system of government in which power is derived from the people, either directly or through "
                    "elected representatives. Core ideas include political equality, rule of law, free and fair elections, and "
                    "protection of fundamental rights.",
                ),
                (
                    "Separation of Powers",
                    "Many democracies divide authority among legislature, executive, and judiciary. This separation is designed "
                    "to prevent concentration of power and to create checks and balances. Independent courts help protect rights "
                    "and interpret laws.",
                ),
                (
                    "Rights and Duties",
                    "Citizens enjoy rights such as freedom of expression, equality before law, and participation in public affairs. "
                    "They also have duties, including respecting laws, paying taxes, and engaging responsibly in civic life. "
                    "Rights are strongest when paired with informed public participation.",
                ),
                (
                    "Elections and Representation",
                    "Elections translate public preferences into governing authority. Transparent voter rolls, secret ballots, "
                    "and impartial administration are essential for legitimacy. Representative bodies debate policy, pass laws, "
                    "and oversee executive action.",
                ),
                (
                    "Civil Society",
                    "Media, community groups, universities, and civic organizations help inform citizens and hold institutions "
                    "accountable. Healthy public debate depends on accurate information and mutual respect across differences.",
                ),
                (
                    "Challenges",
                    "Modern democracies face challenges such as misinformation, inequality, corruption, and low participation. "
                    "Civic education and transparent institutions are practical ways to strengthen democratic resilience.",
                ),
            ],
        ),
        (
            "Chapter 6: Introduction to Algorithms",
            [
                (
                    "What Is an Algorithm?",
                    "An algorithm is a finite sequence of well-defined steps for solving a problem or performing a computation. "
                    "Good algorithms are correct, efficient, and clear enough to implement. Algorithmic thinking is central to "
                    "computer science and data processing.",
                ),
                (
                    "Complexity Basics",
                    "Time complexity estimates how running time grows with input size. Space complexity estimates memory needs. "
                    "Big-O notation describes upper bounds such as O(1), O(log n), O(n), O(n log n), and O(n^2). Choosing an "
                    "efficient algorithm can matter more than small coding optimizations.",
                ),
                (
                    "Searching and Sorting",
                    "Linear search checks items one by one, while binary search quickly finds values in sorted data by repeatedly "
                    "halving the search space. Sorting algorithms such as merge sort and quicksort organize data for faster lookup "
                    "and clearer analysis.",
                ),
                (
                    "Divide and Conquer",
                    "Divide-and-conquer strategies break a problem into smaller subproblems, solve them recursively, and combine "
                    "results. Merge sort is a classic example. This approach often yields efficient solutions for large inputs.",
                ),
                (
                    "Greedy and Dynamic Ideas",
                    "Greedy algorithms make locally optimal choices hoping for a global optimum. Dynamic programming stores "
                    "overlapping subproblem results to avoid repeated work. Each method fits different problem structures.",
                ),
                (
                    "Why Algorithms Matter",
                    "From routing and compression to ranking and cryptography, algorithms shape modern digital systems. "
                    "Understanding trade-offs helps engineers build software that scales reliably.",
                ),
            ],
        ),
        (
            "Chapter 7: Cell Structure and Function",
            [
                (
                    "Cells as Basic Units",
                    "Cells are the basic structural and functional units of living organisms. Unicellular organisms consist of "
                    "one cell, while multicellular organisms contain specialized tissues built from many cells. Cell theory states "
                    "that all living things are made of cells and that cells arise from pre-existing cells.",
                ),
                (
                    "Prokaryotic and Eukaryotic Cells",
                    "Prokaryotic cells lack a membrane-bound nucleus and are typical of bacteria. Eukaryotic cells have a nucleus "
                    "and membrane-bound organelles and are found in plants, animals, fungi, and protists. This distinction is "
                    "fundamental in biology.",
                ),
                (
                    "Key Organelles",
                    "The nucleus stores genetic material. Mitochondria generate ATP through cellular respiration. Ribosomes "
                    "synthesize proteins. The endoplasmic reticulum and Golgi apparatus help process and transport molecules. "
                    "Lysosomes digest waste materials in many animal cells.",
                ),
                (
                    "Plant Cell Features",
                    "Plant cells typically contain chloroplasts for photosynthesis, a cellulose cell wall for support, and a large "
                    "central vacuole for storage and turgor pressure. These features enable plants to produce food and maintain "
                    "structure.",
                ),
                (
                    "Membrane Transport",
                    "The plasma membrane controls movement of substances into and out of the cell. Diffusion and osmosis are "
                    "passive processes, while active transport requires energy to move substances against gradients. Membrane "
                    "proteins play critical roles in signaling and transport.",
                ),
                (
                    "Cell Division",
                    "Mitosis produces genetically similar body cells for growth and repair. Meiosis produces gametes with half "
                    "the chromosome number for sexual reproduction. Accurate cell division preserves genetic continuity.",
                ),
            ],
        ),
        (
            "Chapter 8: Earth's Atmosphere and Weather",
            [
                (
                    "Structure of the Atmosphere",
                    "Earth's atmosphere is layered into troposphere, stratosphere, mesosphere, thermosphere, and exosphere. "
                    "Most weather occurs in the troposphere. The ozone layer in the stratosphere absorbs harmful ultraviolet "
                    "radiation and protects living organisms.",
                ),
                (
                    "Composition",
                    "Nitrogen and oxygen make up most of dry air, with smaller amounts of argon, carbon dioxide, and other gases. "
                    "Water vapor varies by location and season and strongly affects weather and climate.",
                ),
                (
                    "Weather Elements",
                    "Temperature, humidity, pressure, wind, and precipitation are primary weather elements. High and low pressure "
                    "systems influence wind patterns and storm development. Meteorologists use instruments and satellites to observe "
                    "these variables.",
                ),
                (
                    "Winds and Circulation",
                    "Uneven heating of Earth's surface creates pressure differences that drive winds. Global circulation cells "
                    "and the Coriolis effect help shape prevailing wind belts. Local winds arise from geography such as coasts "
                    "and mountains.",
                ),
                (
                    "Storms",
                    "Thunderstorms, cyclones, and monsoonal systems can bring beneficial rain or destructive hazards. Forecasting "
                    "improves when models assimilate dense observational data and when communities receive timely warnings.",
                ),
                (
                    "Human Impact",
                    "Air pollution and greenhouse gas emissions alter atmospheric composition. Clean-air policies, renewable energy, "
                    "and climate adaptation planning are practical responses to these challenges.",
                ),
            ],
        ),
    ]

    extra_bank = [
        "In classroom settings, teachers often ask students to identify key terms, explain processes in their own words, "
        "and connect concepts to examples from daily life. A strong answer usually includes definitions, mechanisms, "
        "and consequences rather than isolated facts.",
        "When revising, students should check whether each paragraph has a clear topic sentence and supporting detail. "
        "Evidence, examples, and precise vocabulary improve academic quality and make evaluation more reliable.",
        "Comparative thinking is useful: contrast related ideas, note exceptions, and explain why one explanation is "
        "stronger than another. This habit builds coherence and deeper content accuracy.",
        "Assessment rubrics commonly reward completeness, logical organization, clarity of wording, and correct language use. "
        "Practicing under these traits helps students prepare for structured evaluation systems.",
    ]

    story.append(Paragraph("Student Learning Companion", title))
    story.append(
        Paragraph(
            "A text-based sample textbook for RAG evaluation testing. This document contains multi-chapter "
            "explanatory content designed to support retrieval, model-answer generation, and answer grading.",
            body,
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            "How to use this file: upload it in TextbookGrade, ask a chapter-based question, and submit a student answer "
            "to test retrieval quality across longer documents.",
            body,
        )
    )
    story.append(PageBreak())

    for chapter_title, sections in chapters:
        story.append(Paragraph(chapter_title, h1))
        for i, (section_title, text) in enumerate(sections):
            story.append(Paragraph(section_title, h2))
            story.append(Paragraph(text, body))
            story.append(Paragraph(extra_bank[i % len(extra_bank)], body))
            story.append(
                Paragraph(
                    f"Study note for {section_title.lower()}: summarize the main claim in one sentence, then list two supporting "
                    "details and one real-world application. This method improves retention and supports later retrieval.",
                    body,
                )
            )
        story.append(PageBreak())

    story.append(Paragraph("Chapter 9: Revision Guide and Practice Prompts", h1))
    story.append(
        Paragraph(
            "This final chapter consolidates major themes from earlier sections and provides practice prompts that are useful "
            "for testing retrieval-augmented grading systems. Students should answer in complete sentences and include "
            "specific terminology from the relevant chapter.",
            body,
        )
    )

    prompts = [
        "Explain the key features of the Indus Valley Civilization, including urban planning, trade, writing, and decline.",
        "Describe how a neural network processes information through input, hidden, and output layers.",
        "Summarize the light-dependent reactions and the Calvin cycle in photosynthesis.",
        "Outline the main stages of the water cycle and explain how climate change can intensify extremes.",
        "Define democracy and describe the roles of legislature, executive, and judiciary.",
        "Compare linear search and binary search and state when each is appropriate.",
        "Differentiate prokaryotic and eukaryotic cells and name three organelles with their functions.",
        "Explain how pressure systems and atmospheric composition influence weather.",
    ]

    story.append(Paragraph("Practice Questions", h2))
    for idx, prompt in enumerate(prompts, start=1):
        story.append(Paragraph(f"{idx}. {prompt}", body))
        story.append(
            Paragraph(
                "Model-style reminders: define key terms, use accurate factual detail, organize ideas in a logical sequence, "
                "prefer precise academic vocabulary, and check grammar before submission.",
                body,
            )
        )

    story.append(Paragraph("Extended Review Passages", h2))
    for i in range(1, 12):
        story.append(
            Paragraph(
                f"Review Passage {i}. A complete academic response integrates conceptual understanding with structured "
                "presentation. Begin with a concise definition or thesis. Continue with mechanisms, examples, and implications. "
                "Conclude by restating the significance of the topic. Across history, biology, climate, civics, and computing, "
                "this pattern remains effective because it mirrors how expert explanations communicate both what something is "
                "and why it matters. Learners who practice this pattern tend to produce answers that are easier to evaluate "
                "against rubrics focused on content accuracy, coherence, vocabulary, and grammar. "
                "Additional detail for retrieval testing includes named processes, causal links, and comparisons between related concepts "
                "so that chunked embeddings can recover relevant evidence for model-answer construction.",
                body,
            )
        )

    story.append(
        Paragraph(
            "End of sample textbook. This file is intentionally text-based so OCR is unnecessary during RAG indexing.",
            body,
        )
    )

    def _page_number(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        page = canvas.getPageNumber()
        canvas.drawCentredString(A4[0] / 2, 0.5 * inch, f"Page {page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=_page_number, onLaterPages=_page_number)

    reader = PdfReader(str(OUT))
    print(f"Wrote {OUT}")
    print(f"pages={len(reader.pages)}")
    print(f"size_kb={OUT.stat().st_size / 1024:.1f}")


if __name__ == "__main__":
    main()
