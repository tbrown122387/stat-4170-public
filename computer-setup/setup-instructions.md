# DS-5005 Computer Setup Guide (First-Time Setup)

Use this guide the first time you set up your machine for DS-5005. When you finish, you should be able to:

1. Open the class folder in VS Code.
2. Use the correct Conda environment named quant-ts.
3. Run Python scripts and notebooks from VS Code.
4. Render Quarto files when needed.

## 1) Install Anaconda

If you already have Anaconda or Miniconda installed and working, you can skip to Step 2.

1. Download Anaconda Individual Edition from: https://www.anaconda.com/download
2. Install it using the default options.

Windows notes:
1. Choose "Just Me" unless this is a shared computer.
2. Do not check "Add Anaconda to PATH" during install.
3. Use Anaconda Prompt for setup commands if regular Command Prompt cannot find conda.

macOS/Linux notes:
1. Install to a standard location (commonly ~/anaconda3).
2. If your shell is zsh or bash, you will run conda init in the next step.

## 2) Initialize and verify Conda

Open a terminal and run:

```bash
conda init
```

Close and reopen the terminal. Then verify:

```bash
conda --version
python --version
```

If conda is old, update it:

```bash
conda update -n base -c defaults conda
```

## 3) Install VS Code

1. Download from: https://code.visualstudio.com/download
2. Install with default settings.

## 4) Install VS Code extensions

In VS Code, open Extensions and install:

1. Python (Microsoft)
2. Jupyter (Microsoft)
3. Pylance (Microsoft)
4. Quarto (Quarto)

Optional but useful:

1. autopep8
2. GitLens

## 5) Get the DS-5005 course folder on your machine

Use one of these methods:

1. Clone with Git.
2. Download a zip and extract it.

You should end up with a local folder named ds-5005 containing files like environment.yml and the lectures folder.

## 6) Create the class environment

In a terminal, cd into the ds-5005 folder and run:

```bash
conda env create -f environment.yml
```

Then activate:

```bash
conda activate quant-ts
```

Verify you are using the class environment:

```bash
python --version
which python
```

On Windows, use:

```bash
where python
```

The path should include envs/quant-ts.

## 7) Open the folder in VS Code

1. In VS Code, go to File > Open Folder.
2. Select your local ds-5005 folder.
3. If prompted, click "Yes, I trust the authors" for this course folder.

## 8) Select the DS-5005 Python interpreter in VS Code

This is the most important VS Code integration step.

1. Open the Command Palette.
2. Run Python: Select Interpreter.
3. Choose the interpreter for conda env quant-ts.

It may appear as:

1. conda (quant-ts)
2. A full path containing .../anaconda3/envs/quant-ts/... or .../miniconda3/envs/quant-ts/...

Confirm at the bottom-right of VS Code that the selected interpreter references quant-ts.

## 9) Configure the VS Code terminal to use the same environment

1. Open a new integrated terminal in VS Code.
2. Activate the environment if needed:

```bash
conda activate quant-ts
```

3. Check:

```bash
python --version
```

You should see quant-ts at the shell prompt (or confirm via which/where python).

## 10) Test Python execution in VS Code

Open any .py file (for example, one in lectures/module01) and test one of the following:

1. Highlight code and press Shift+Enter to run selection in Python terminal.
2. Click the Run button (top-right) to run the file.
3. Use Terminal > Run Task only if instructed for a specific assignment.

If Shift+Enter does nothing, open Keyboard Shortcuts and search for:

1. Python: Run Selection/Line in Python Terminal

Then assign a shortcut.

## 11) Test notebook support in VS Code

1. Open an .ipynb notebook, or create one.
2. In the notebook kernel picker, choose Python environment quant-ts.
3. Run a test cell:

```python
import sys
print(sys.executable)
```

The executable path should point to the quant-ts environment.

## 12) Keep environment packages synced with class updates

The `environment.yml` file contains the list of packages that are guaranteed to reproduce all provided code.

If environment.yml changes during the semester, run from the ds-5005 folder:

```bash
conda activate quant-ts
conda env update -f environment.yml --prune
```

## 13) Quarto integration (for .qmd files)

If you will render lecture or assignment .qmd files:

1. Ensure Quarto extension is installed in VS Code.
2. Install Quarto CLI if not already installed: https://quarto.org/docs/get-started/
3. From terminal in project folder, test:

```bash
quarto check
```

4. Install TinyTeX, needed to render any `.qmd` file to PDF (e.g. the syllabus):

```bash
quarto install tinytex
```

5. Render a file when needed:

```bash
quarto render path/to/file.qmd
```

## 14) Troubleshooting quick fixes

Problem: conda command not found.
1. Restart terminal.
2. Run conda init again.
3. On Windows, try Anaconda Prompt.

Problem: VS Code uses wrong interpreter.
1. Run Python: Select Interpreter again.
2. Close all terminals and open a fresh one.
3. Re-activate conda activate quant-ts.

Problem: imports fail but package should exist.
1. Confirm interpreter is quant-ts.
2. Run conda list in terminal.
3. Update env with conda env update -f environment.yml --prune.

Problem: notebook kernel missing.
1. Install/enable Jupyter extension.
2. Pick kernel manually in top-right of notebook.
3. Restart VS Code.

## 15) First-day checklist

Before class work begins, confirm all are true:

1. conda works in terminal.
2. You can activate quant-ts.
3. VS Code interpreter is set to quant-ts.
4. A Python file runs successfully.
5. A notebook cell runs with quant-ts kernel.
6. quarto check runs without critical errors (if using .qmd files).
7. quarto install tinytex has been run (if you'll be rendering any .qmd files to PDF).