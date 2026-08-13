# STAT 4170 – Financial Time Series and Forecasting

Welcome! This is the public materials repository for **STAT 4170: Financial Time Series and Forecasting**.

This repo is published automatically from the course's private source repository. Solutions, textbook PDFs, raw market-data scripts, future surprise assignments, and the syllabus are intentionally kept out of the public copy. Everything here is meant to be safe (and useful) to read, run, and fork.

## What's in This Repository

| Folder / file | What it is |
|------------------------------------|------------------------------------|
| `lectures/moduleNN/` | One folder per "module." Each contains `index.qmd` (the Quarto source for that week's slides) and `index.html` (the rendered, browsable slide deck — open it directly in your browser). |
| `case-studies/csN/` | Case study assignment prompts (`prompt.qmd` source and `prompt.html` rendered version). These are the graded, open-ended projects referenced throughout the modules. |
| `computer-setup/` | A first-time setup guide for getting Python, Conda, and Quarto working on your own machine — start here if this is your first time opening this repo. |
| `environment.yml` | The Conda environment specification. This pins the exact packages needed to run every notebook and code chunk in this repo. |

Slide decks and case-study prompts are also rendered to standalone HTML, so you don't need Quarto installed just to *read* the materials — clone or download the repo and open the `.html` files directly.

## Setting Up Your Environment

The short version:

``` bash
conda env create -f environment.yml
conda activate quant-ts
```

That's it for running notebooks and Python scripts. For a full walkthrough (installing Anaconda and VS Code, selecting the right interpreter, troubleshooting a broken kernel, etc.), see [`computer-setup/setup-instructions.md`](computer-setup/setup-instructions.md).

## Rebuilding Materials From Source

Every slide deck and case-study prompt in this repo is written as a Quarto (`.qmd`) document and rendered to the `.html` file sitting next to it. You only need to rebuild from source if you're editing the materials yourself (e.g., re-running a code chunk with different data) — reading the pre-rendered `.html` files requires nothing beyond a browser.

To rebuild:

1.  Install [Quarto](https://quarto.org/docs/get-started/) if you don't already have it.

2.  Install TinyTeX, needed to render any document to PDF (e.g. the syllabus): `quarto install tinytex`.

3.  Activate the course environment (see above): `conda activate quant-ts`.

4.  Render a single file:

    ``` bash
    quarto render lectures/module01/index.qmd
    ```

    or a case study:

    ``` bash
    quarto render case-studies/cs1/prompt.qmd
    ```

Some code chunks are set to `eval: false` in the slide source — they're shown for reference but not re-run automatically, either because they hit a live data source or because re-running them isn't necessary to follow along. Chunks that are re-run at render time are marked `eval: true` in the `.qmd` source.

## Questions

If something here is broken, unclear, or missing, reach out to the course instructor rather than opening an issue against this repo — it's a one-way mirror of the private source, so issues/PRs filed here won't be seen.
