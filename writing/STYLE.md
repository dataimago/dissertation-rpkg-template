<!-- source: dataimago-design/templates/WRITING-STYLE.md@aade34e (provenance — do not edit this line; replace the whole file to vendor your own style guide) -->

# The dataimago technical writing spec

<!-- canonical: dataimago-design/templates/WRITING-STYLE.md
     Copies of this file ship into generated repos as writing/STYLE.md with a
     provenance header naming this source and its commit SHA.
     Governing decision: dataimago-design/wiki/decisions/technical-writing-spec.md
     Pattern: dataimago-design/wiki/patterns/technical-writing-3-mode.md -->

This is the default register for technical prose in this repository — thesis
chapters, knowledge-base pages, methods writing, README-class documents. It
is a **default, not a mandate**: your `dataimago-spec.yaml` selects it
(`thesis.writingStyle.mode: shipped`), replaces it with your own guide
(`vendored`), or asks your AI to distill a personal spec from your exemplar
prose (`generated`).

What this spec governs is *epistemic register* — how claims are stated,
scaffolded, and bounded. What it deliberately does not govern is *voice*:
your personality, domain idiom, and rhetorical taste are yours. An AI
assistant writing under this spec should apply every rule below and still
sound like the author, not like the spec.

---

## The seven moves

### 1. Thesis-first paragraphs, with a reframe when introducing known ideas

Open every paragraph with its claim; develop after. When introducing a
familiar concept, state the received reading first, then elevate or correct
it — the reframe is the engine that makes technical prose feel like an
argument rather than a catalogue.

- **Don't:** "There are several ways to think about cross-validation. It was
  introduced in the 1970s and has many variants, which we now review."
- **Do:** "Cross-validation is usually presented as a variance-reduction
  device. Here we treat it as something stronger: an *estimator of the
  deployment gap*, whose bias — not its variance — is the property the
  design must control."

### 2. Formal results live inside plain-language scaffolding

Motivate every formal statement before it appears (why it is needed, what
hinge it provides) and interpret it immediately after ("Put plainly: …").
Mathematics never arrives unannounced and never leaves uninterpreted. The
reader should be able to skip the formalism and still follow the argument —
or read only the formalism and know exactly what it is for.

- **Don't:** state a theorem, then start the next section.
- **Do:** "The following lemma is the formal hinge used throughout: it
  characterizes exactly when two scores carry the same ordinal information.
  [lemma] Put plainly: if two scoring rules agree about order, they differ
  only by a relabeling — and any conclusion that survives relabeling is a
  conclusion about order alone."

### 3. Say what the result does NOT establish

Every capability or superiority claim is paired, structurally, with an
explicit boundary: what the method does not buy, which question it leaves
open, which stronger reading the evidence does not support. This is not
hedging — hedging weakens every sentence; boundary-setting strengthens the
claims you keep by showing which ones you decline.

- **Don't:** "The estimator performed well across all conditions." (Vague
  strength, no boundary.)
- **Do:** "The estimator dominated the baseline on held-out log-loss in all
  three designs. Two things this does not establish: it says nothing about
  calibration in the tails, which our metric never probes; and the gain
  vanished under the misspecified margin, so the advantage is a property of
  the dependence model, not of the procedure as a whole."

### 4. Named, numbered scaffolding

When a problem has parts, enumerate them — and make later structure answer
earlier structure (four numbered problems met by three numbered
requirements; a description-list mapping each concept to what it
contributes). Close long arguments with a compressed numbered credo the
reader can carry away. Signpost paper organization explicitly.

- **Don't:** a page of prose in which four difficulties and three design
  responses are interleaved.
- **Do:** "The difficulty has three parts: (1) …; (2) …; (3) … . A usable
  method must therefore (a) …, (b) …, and (c) … — and (a) answers (1)
  directly, while (b) and (c) split (2) and (3) between them."

### 5. Controlled personality, in precise doses

Voice is allowed — a vivid title, one wry aside per section at most, an
earned aphorism at a section close — inside an otherwise formal register.
The test: personality should mark the places where the argument turns, not
decorate every sentence. If a joke would survive deletion without the
argument noticing, delete it.

- **Don't:** breezy hedges and asides sprinkled through the methods section.
- **Do:** open a foundational section by naming the deflationary way the
  field usually presents the idea, spend the section earning the reversal,
  and end with one line the reader will quote ("The residual is not noise;
  it is the part of the signal the model declined to hear.").

### 6. Citation-anchored claims and disciplined terminology

Load-bearing claims carry citations; when the claim rests on specific
wording, cite to the page and quote briefly. Terms-of-art are *italicized at
first use*, defined in place, and then used with total consistency —
never alternating synonyms for elegant variation. Prefer the field's
canonical term over a coined one unless the coinage is itself a
contribution (then define it as such).

- **Don't:** "It is well known that rank-based statistics are essentially
  copula-based."
- **Do:** "the study of rank statistics is, in a precise sense, the study of
  copula-invariant properties [Schweizer & Wolff 1981, p. 884]."

### 7. Dialectical structure: voice the critique fully, then bound it

Opposing positions and known critiques get stated in their strongest form —
never strawmanned, never silently dropped — and then *bounded*: state
precisely which part of the critique the present work accepts, which part it
answers, and which part remains open. Disagreement is a structural element,
not an obstacle.

- **Don't:** "Some authors have questioned interval-scale assumptions, but
  we set this aside."
- **Do:** "The critique is stronger than its reception suggests: if the
  attribute lacks additive structure, interval claims are not approximations
  but category errors. Whether or not one accepts the full diagnosis, its
  methodological core survives: the burden of proof sits with the interval
  claim, not against it. This paper accepts that burden for the marginal
  scales and shows the dependence structure never needed it."

---

## Register rules (apply throughout)

- **Tense and person.** "We" for the authors' actions; present tense for
  what the paper does and what is true; past tense for what was run.
- **Sentence mechanics.** Em-dash appositions and colon-hinged sentences are
  house moves; use them to attach a consequence or definition to a claim,
  not to chain three thoughts into one sentence.
- **Numbers and claims.** Any number a reader might act on is either
  computed in place (executable documents) or carries a pointer to the
  artifact it came from. No hand-retyped results.
- **Uncertainty.** State it once, quantitatively if possible, at the claim
  it attaches to — not as a diffuse fog of "may," "might," and "perhaps"
  across the paragraph.
- **Abstracts and openers.** An abstract states the contribution and its
  strongest honest boundary; it never promises "we discuss" or "we explore."

## Addendum: reference-doc prose (roxygen, README, wiki stubs)

Reference writing uses moves 1, 3, and 6 in compressed form: first sentence
= what the function/page does (thesis-first); one sentence of boundary where
behavior surprises ("does not impute; missing entries are skipped"); exact
terminology matching the rest of the corpus. Moves 2, 4, 5, and 7 apply only
when the reference doc carries an argument (design notes, vignettes).

## If you are the repo's AI assistant

Read this file before drafting any prose surface. When the spec's
`writingStyle.mode` is `generated`, your first task is different: read the
exemplars in `raw/` (see `context.styleExemplars` in `dataimago-spec.yaml`),
distill the author's own moves into a replacement for this file, and have
the author approve it before adopting it. When editing existing prose,
apply the spec to the *edit*, not as a license to rewrite surrounding text
wholesale.
