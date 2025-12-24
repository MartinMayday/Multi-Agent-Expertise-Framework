---
description: Apply First Principles Thinking to reframe problems and generate novel solutions
category: thinking-frameworks
argument-hint: <problem_statement|@context_file.md>
allowed-tools: Read, Write, Edit, Code, Terminal
---

# First Principles Thinking

A structured slash-command that walks the agent (and human) through a rigorous **First Principles** reasoning workflow. Use it whenever you need to break out of analogy-based thinking and uncover fresh approaches.

## Quick Usage
```bash
/first-principles-thinking "How can we reduce build times by 50%?"
/first-principles-thinking @pp_slow-build-times.md
/first-principles-thinking --help   # Show full docs
```

### Argument Formats
1. **Inline prompt** – Provide the question or challenge in quotes.
2. **@file reference** – Point to a Markdown file that contains the scenario context.

---

## Framework Steps
The command will guide the LLM through **five deliberate phases**:

1. **Clarify & Goal-Set**  
   • Translate the prompt into a clear objective statement.  
   • Define explicit success metrics.

2. **List Assumptions**  
   • Enumerate all assumed constraints, resources, and “givens.”  
   • Mark each assumption with a confidence score (High / Medium / Low).

3. **Deconstruct to Fundamentals**  
   • Break the problem into elemental truths that cannot be reduced further.  
   • Cite credible sources or logical proofs for each fundamental fact.

4. **Reconstruct Solutions**  
   • Using only the fundamentals, reason *upwards* to generate options—no legacy constraints allowed.  
   • Evaluate each option against the success metrics.

5. **Synthesize & Next Actions**  
   • Present top-ranked solution(s) with rationale.  
   • Propose concrete next steps and validation tests.

> ⚡ **Tip:** If any assumption has Low confidence, loop back and gather evidence before continuing.

---

## Output Template
The command returns a Markdown report following this skeleton:

```md
# First Principles Analysis: <Problem>

## 1. Goal Statement
<goal>

## 2. Assumptions
| # | Assumption | Confidence |
|---|------------|------------|
| 1 | ... | High |

## 3. Fundamental Truths
- Fact 1 – citation/reference
- Fact 2 – …

## 4. Solution Reconstruction
### Option A – …
### Option B – …

## 5. Recommended Plan & Tests
1. …
2. …
```

---

## Examples
1. **Reduce Build Times**
```bash
/first-principles-thinking "Cut CI pipeline duration from 20 → 5 minutes without sacrificing test coverage"
```

2. **Pricing Strategy**
```bash
/first-principles-thinking "How can we price our SaaS for SMBs in emerging markets?"
```

---

## References
- Aristotle – *Physics* (root of first principles)
- René Descartes – *Discourse on Method*
- Elon Musk interviews on engineering design (SpaceX, Tesla)
- Farnam Street Blog – “First Principles: The Building Blocks of True Knowledge”

---

## Implementation Notes
Behind the scenes this command can:
- Read the referenced context file automatically (`@filename.md`).
- Create a temporary working file `analysis/<slug>-fp.md` capturing intermediate reasoning (optional).
- Suggest adding key insights to your project’s knowledge base.

---

*Use this command whenever you sense you’re defaulting to “that’s how it’s always been done.”*
