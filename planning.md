# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Domain: Course and Professor Reviews

I choose to work with the domain of course and professor reviews because students heavily rely on other students' experiences and opinion when deciding which classes to take and professors to choose. This knowledge is valuable because it provides insights into teaching style, workload, grading practices, exam difficulty, and overall course quality.
This information is difficult to find through official channels because university course catalogs and department websites typically only provide basic descriptions, prerequisites, and schedules. Detailed student experiences are scattered across platforms or website like Rate My Professors, Reddit discussions, university forums, and unofficial review sites, making it time-consuming for students to gather and compare information.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate my Professor|Georgia State University page on Rate My Professors|https://www.ratemyprofessors.com/school/360|
| 2 |Rate my Professor|Searchable directory of GSU professors|https://www.ratemyprofessors.com/search/professors/360|
| 3 |Rate my Professor|Mark Grinshpon (Mathematics) professor reviews|https://www.ratemyprofessors.com/professor/949752|
| 4 |Rate my Professor|Cyntoria Johnson (Criminal Justice) professor reviews|https://www.ratemyprofessors.com/professor/1597666|
| 5 |Reddit|"Prof recommendations" discussion thread|https://www.reddit.com/r/GaState/comments/1on3m4y|
| 6 |Reddit|Accounting professor recommendations for georgia state university|https://www.reddit.com/r/GaState/comments/1s9sp6e/best_professor_for_accounting_2102/|
| 7 |Coursicle|CIS 3260 course reviews and professor feedback|https://www.coursicle.com/gsu/courses/CIS/3260/|
| 8 |Reddit|Discussion about poor professor experiences and reporting concerns|https://www.reddit.com/r/GaState/comments/1bjs1cq|
| 9 |Professor dicrectory|Georgia State professor review directory|https://www.professors.directory/school/ga-georgia_state_university/|
| 10 |Reddit|Georgia State University subreddit (general source for professor/course discussions)|https://www.reddit.com/r/GaState/|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 400 characters

**Overlap:** 50 characters between consecutive chunks

**Reasoning:** This chunk size is appropriate because most sources consist of short student reviews and discussion comments rather than long articles or guides. A 400-character chunk is usually large enough to capture a complete review, including details about teaching style, workload, grading, and exam difficulty, without combining multiple unrelated opinions into the same chunk. The 50-character overlap helps preserve context when an important point extends across chunk boundaries. Since the corpus is review-heavy, smaller chunks are preferable to large ones because they allow the retrieval system to return highly relevant student experiences for specific queries, such as finding information about difficult exams, attendance policies, or recommended professors.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers` (runs locally, no API key)

**Top-k:** 5 — enough to cover multiple professors/perspectives per query without drowning the LLM in noise

**Production tradeoff reflection:** For a real deployment you'd consider `text-embedding-3-large` (OpenAI) for higher accuracy, but it costs per token and requires an API. `all-MiniLM-L6-v2` is fast and free but has a 256-token context limit, which is fine for short reviews. If GSU had international students writing in other languages, you'd want a multilingual model like `paraphrase-multilingual-MiniLM-L12-v2`.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Mark Grinshpon's exams in Mathematics? | Student reviews describe his courses as challenging with relatively high difficulty. Grading is strict, and success requires strong preparation and understanding. |
| 2 | Is Cyntoria Johnson considered a good professor for Criminal Justice? | Reviews are mixed: some call her caring, engaging, and knowledgeable. Others cite heavy reading, tough grading, unclear instructions, and slow email responses. |
| 3 | What accounting professors do students recommend at GSU? | Students commonly recommend Edie Oliff, William Dowis, and Jessica Miller for Accounting courses. Oliff is noted for ACCT 2101/2102, Dowis as a favorite, and Miller for ACCT 2102. |
| 4 | What do students say about the workload in CIS 3260? | CIS 3260 is described as a demanding programming course requiring consistent effort. Reviews mention challenging exams, significant programming work, and the need for regular practice. |
| 5 | What are common complaints students have about GSU professors generally? | Common complaints include unresponsive faculty, unclear materials, poor communication, and difficult grading practices. Students also mention heavy self-teaching, long slides, and unclear instructions. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splits a professor's name from their review** — if a review starts with "Professor Smith is great" but the name got cut into the previous chunk, retrieval for "Professor Smith" might miss it entirely.

2. **Off-topic Reddit content** — the r/GaState subreddit covers more than just professors. A thread about professor issues might include comments about financial aid, parking, or dorms that end up in chunks and pollute retrieval results.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
