# Research & References

## LLM-as-a-Judge

### Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement
Cho et al. — [arXiv:2606.27226](https://arxiv.org/abs/2606.27226) · full text: [arxiv.org/html/2606.27226](https://arxiv.org/html/2606.27226)

**Why it matters for testing:** A practical recipe for using an LLM as a *judge* in your test/eval pipeline that is more interpretable and better-calibrated than asking the model for a single holistic score.

**Method (BinEval).** Instead of "rate this output 1–5," decompose the criteria into atomic yes/no questions, answer each independently, then aggregate:
1. **Summarize** the task prompt into a set of explicit requirements.
2. **Decompose** each requirement into binary questions where "yes" = satisfied, grouped by dimension (coherence, consistency, fluency, relevance, …).
3. **Aggregate**: per-dimension score = fraction of "yes" answers; overall score = fraction across all questions. Scores in [0,1], affine-scalable to a 1–5 scale. Every verdict carries a natural-language explanation.
   - The meta-prompt is task-agnostic; only the task prompt changes per use.

**Why binary beats holistic:** complexity reduction (each question isolates one verifiable property), variance reduction via aggregation (~1/N), and explicit failure-mode coverage.

**Results (Spearman ρ vs. human):**
- SummEval: BinEval (Claude) 0.563 avg vs. G-Eval (GPT-4) 0.514, UniEval 0.474, BARTScore 0.385, BERTScore 0.225. Largest gain on **consistency** (0.655).
- Topical-Chat: 0.632 vs. G-Eval 0.575. QAGS (hallucination): 0.620, best of the set.
- Avoids the **ceiling effect** of holistic judges → better discrimination between borderline and clearly-flawed outputs. Case study: a plausible-but-fabricated summary scored 5.0 from G-Eval/UniEval but 1.57 from BinEval (human: 2.0).

**Practical guidance / when to use:**
- **Best for concrete, claim-level criteria** — factual consistency, format/constraint compliance, presence of specific content. Decomposed checks catch misattributions and fabrications holistic scores miss.
- **Weaker for subjective/holistic qualities** (e.g. relevance) — over-decomposition makes the judge *more severe than humans*. Don't shatter a fuzzy criterion into many granular questions.
- **Cost trade-off:** more model calls (generate + answer each question) in exchange for diagnostic signal.

**Limitations (read before trusting the score):**
- Score quality depends entirely on question quality — missing criteria → silently missing from the score.
- Assumes "fraction satisfied" maps ~linearly to quality, which isn't always true.

**Self-improvement loop (optional):** binary-question disagreements between two evaluators (or between generator output and the judge) become targeted "lessons" used to rewrite prompts. Gains: +0.07–0.075 Spearman on SummEval; IFBench generation +3.4pp.
- **Caveat:** most gains land in the **first 1–2 iterations**; later iterations degrade as lessons accumulate into competing instructions (IFBench collapsed 38%→26% by iteration 4).
- Prompt-tuning only helps when the model *has* the capability but needs guidance (format constraints: +17pp). It does **not** fix capability gaps (counting/ratio constraints: ~0pp).
