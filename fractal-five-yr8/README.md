# The Fractal Five — Year 8 warm-ups (v3, for 2027)

Four student booklets (one per term) and four teacher answer files. Each booklet has 30 sessions of 5 questions, a two-page formula and rule reference, and a score tracker that lists the Stage 4 outcomes.

The finished PDFs are in `out/`:

| File | Pages |
|---|---|
| `Yr8_The_Fractal_Five_Term_N_Warm-Ups_v3.pdf` | 34 (cover, 30 sessions, 2 reference pages, tracker) |
| `Yr8_The_Fractal_Five_Term_N_Answers_v3.pdf` | 2 (teacher copy) |

## What the questions follow (agreed 7 Nov 2026)

### Sequence

- The sequence follows the Year 8 mixed ability strand in the Master Information Kiosk (T1 2027 and T2 2027).
- Year 7 content (NCM 7 Ch 1–11) can appear from Term 1 Week 1.
- Ratios, rates and time (NCM 7 Ch 12) are held back until Year 8 teaches them, so none appear this year.
- Each Year 8 unit starts in the first session after its teaching ends:

| Unit | Outcome | NCM 8 | First session |
|---|---|---|---|
| Rational numbers, percentages & financial maths | MA4-FRC-C-01 | §6.04–6.10 | T1 Wk 5 S3 |
| Index laws (numerical bases) | MA4-IND-C-01 | §2.08, 2.10–2.12 | T1 Wk 7 S1 |
| Pythagoras' theorem | MA4-PYT-C-01 | Ch 1 | T1 Wk 10 S3 |
| Algebra 2 | MA4-ALG-C-01 | §3.01–3.10 | T2 Wk 4 S1 |
| Equations 2 | MA4-EQU-C-01 | §9.01–9.03, 9.05–9.07 | T2 Wk 9 S1 |

- Terms 3–4 use only Year 7 content and these five units. The kiosk has no 2027 plan for Terms 3–4 yet.
- Year 8 questions per term: 20, 60, 90 and 100 of 150, so Term 4 is about two-thirds Year 8.
- There is no simple interest (Stage 5), no binomial products, no equations with brackets and no change of subject.

### Session design

- Q1–Q2 come from recently completed Year 8 units; Q3–Q5 rotate through earlier content.
- Every question is kept easy and mostly non-calculator. A calculator icon marks the rest.
- There is one reasoning question per week, tagged EXPLAIN or REASON.
- No question is repeated, including the same numbers with only the units changed.

### Formula boxes

- Formula boxes say FORMULA or METHOD.
- Support fades through the year:
  - **Terms 1–2:** the formula or rule is given.
  - **Term 3:** the formula or rule has a gap to fill.
  - **Term 4:** students write it from memory, with the reference pages at the back.
- Notation follows NCM 7 and 8 (A = lw, V = lwh).
- Circumference and Pythagoras answers use the π and √ keys. Where π ≈ 3.14 gives a different answer, the answer file lists it too.

## Rebuilding

You need Python 3 with `pypdf` and `pdfplumber`, plus Node with Playwright and Chromium.

```bash
python3 src/build.py
```

```bash
python3 src/check.py
```

`build.py` writes `build/year.json` and the PDFs in `out/`. `check.py` re-works every answer independently from what is printed and checks the sequencing rules. It exits non-zero if anything fails.

To change the schedule (for example, once the 2027 Term 3–4 plan is known), edit `UNLOCK` and `n_year8()` in `src/schedule.py`. To add a new unit, add its generators in a `bank_*.py` file. Each question has its own random seed, so changing one generator does not reshuffle the rest of the year.

## Files

| File | What it does |
|---|---|
| `src/bank_geo.py` | Angle and triangle generators |
| `src/bank_meas.py` | Measurement generators |
| `src/bank_num.py` | Number generators |
| `src/bank_alg.py` | Algebra generators |
| `src/bank_stat.py` | Statistics and probability generators |
| `src/bank_y8.py` | Year 8 unit generators. Every answer is computed in code. |
| `src/svg.py` | Diagrams, drawn to scale, with automatic label-collision checks |
| `src/schedule.py` | Scope-and-sequence rules, slot mix, reasoning items, uniqueness |
| `src/build.py`, `src/style.css`, `src/layout.js`, `src/render.js` | Page layout (measured from v2) and rendering to PDF |
| `assets/` | Fonts (Poppins and Open Sans, SIL OFL), school logo, page bands, v2 covers |

The v2 covers are reused with a corrected caption: "each circle fills a gap between three touching circles; every curvature (1 ÷ radius) is an integer". The Term 3 cover badge reads FILL THE GAP and the Term 4 badge reads FORMULAS FROM MEMORY.
