---
title: "Design specimen"
subtitle: "What the site's theme does to each kind of element"
---

<!-- Rendered only by the design-update comparison (.dataimago/design-update.json): CI
     copies it in as an extra chapter in a throwaway checkout. Quarto never publishes
     files under .dataimago/, so this page is not part of your book. Safe to delete. -->

This page exercises the theme. A paragraph of running text carries an
[inline link](https://quarto.org), some *emphasis*, some **strong text**, and
`inline code`. Accented names (Dvořák, Łódź, Nguyễn) and Greek letters in text
(α, β, θ) use the same face.

## A second-level heading

- A list item
- Another, with a [link](https://example.org)

1. A numbered item
2. Another

> A block quotation, set off from the running text.

### A third-level heading

```r
fit <- lm(score ~ prior, data = students)
summary(fit)
```

::: {.callout-note}
## A note

Callouts carry the theme's semantic colours.
:::

::: {.callout-warning}
A warning without a title.
:::

| Measure | Estimate | SE   |
|---------|---------:|-----:|
| Mean    | 0.42     | 0.03 |
| SD      | 1.07     | 0.02 |

: A table with a caption.

Display maths: $$P(X_{ij} = 1 \mid \theta_i) = \frac{1}{1 + e^{-a_j(\theta_i - b_j)}}$$
and inline maths, $\hat{\theta} \pm 1.96\,\mathrm{SE}$.

A footnote reference.[^1]

[^1]: The footnote text.
