# Installation Guide

This guide will walk you through installing T3CO step-by-step, even if you have no prior experience with Python.

## Before You Start

T3CO is a Python-based tool that requires:

- Python (version 3.8, 3.9, or 3.10)
- A terminal or command prompt to run commands
- A few megabytes of free disk space

If you're new to Python or command-line tools, don't worry! We'll guide you through each step.

## Installing Python (if needed) <a name="installing-python"></a>

If you don't already have Python installed:

1. Visit the [Python downloads page](https://www.python.org/downloads/)
2. Download the installer for Python 3.10 (recommended) for your operating system
3. Run the installer
   - On Windows: Make sure to check "Add Python to PATH" during installation
   - On macOS: Follow the installer instructions
   - On Linux: Most distributions come with Python, but you can use your package manager if needed

To verify Python is installed, open a terminal or command prompt and type:

```bash
python --version
```

or

```bash
python3 --version
```

You should see output like `Python 3.10.x` (where x is any number).

## Setting Up a Python Environment <a name="setting-up-env"></a>

A Python environment is a dedicated space for installing packages without affecting your system Python. This helps avoid conflicts between different projects.

There are two recommended ways to create an environment:

### Option 1: Using Conda (Recommended for Beginners)

1. First, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (a lightweight version of Anaconda)
   - Download the installer for your operating system
   - Run the installer and follow the prompts

2. Once installed, open a terminal:
   - On Windows: Open "Anaconda Prompt" from the Start menu
   - On macOS/Linux: Open your regular terminal

3. Create a new environment for T3CO:

    ```bash
    conda create -n t3co python=3.10
    ```

    This creates a new environment named "t3co" with Python 3.10.

4. Activate the environment:

    ```bash
    conda activate t3co
    ```

    You'll notice the prompt changing to show `(t3co)` at the beginning, indicating the environment is active.

### Option 2: Using venv (Python's built-in tool)

1. Open a terminal or command prompt

2. Create a new environment:

    ```bash
    python3.10 -m venv t3co
    ```

    This creates a new folder named "t3co" containing your environment.

3. Activate the environment:

    On macOS/Linux:

    ```bash
    source t3co/bin/activate
    ```

    On Windows (using Command Prompt):

    ```bash
    t3co\Scripts\activate.bat
    ```

    On Windows (using PowerShell):

    ```bash
    t3co\Scripts\Activate.ps1
    ```

    When activated, you'll see `(t3co)` at the beginning of your command prompt.

## Installing T3CO Python Package

Now that you have a Python environment set up, you can install T3CO. There are two ways to do this:

### Option 1: Installing from PyPI (Recommended for Most Users) <a name=install-from-pypi></a>

This is the simplest method and recommended for most users who just want to run analyses:

1. With your environment activated (you should see `(t3co)` in your prompt), run:

   ```bash
   pip install t3co
   ```

2. To verify installation, run:

   ```bash
   pip show t3co
   ```

   This should display information about the installed T3CO package.

### Option 2: Installing from GitHub (For Advanced Users)

This method gives you access to the latest code and demo files:

1. First, you need to install Git if you don't have it:
   - For Windows: Download from [git-scm.com](https://git-scm.com/downloads)
   - For macOS: Install via [Homebrew](https://brew.sh/) with `brew install git` or download from [git-scm.com](https://git-scm.com/downloads)
   - For Linux: Use your package manager (e.g., `sudo apt install git` for Ubuntu)

2. Clone (download) the repository:

   ```bash
   git clone https://github.com/NREL/T3CO.git T3CO
   ```

   This will create a folder named `T3CO` in your current directory.

3. Navigate to the T3CO folder:

   ```bash
   cd T3CO
   ```

4. Install T3CO and its dependencies:

   ```bash
   pip install -e .
   ```

   The `-e` flag makes the installation "editable," meaning changes to the code will be reflected without reinstalling.

If you encounter a `ModuleNotFoundError: No module named 'fastsim'` error, you can fix it by running:

```bash
pip install fastsim==2.1.1
```

## Getting Demo Input Files <a name=copy-demo-inputs></a>

T3CO comes with demo input files that help you get started. To copy these files to a location of your choice:

1. Make sure your T3CO environment is activated

2. Run this command:

   ```bash
   install_t3co_demo_inputs
   ```

3. When prompted with `Do you want to copy the T3CO demo input files? (y/n):`, type `y` and press Enter

4. When asked `Enter the path where you want to copy demo input files:`:
   - To copy to your current directory, type `.` (a single period) and press Enter
   - To copy to a specific folder, type the full path to that folder and press Enter

This will create a `demo_inputs` folder with all the files needed to run T3CO.

## What's Next?

Now that you have T3CO installed, you can:

1. Proceed to the [Quick Start Guide](./quick_start.md) to learn how to run your first analysis
2. Explore the demo input files to understand how to configure T3CO
3. Read the [T3CO Overview](./T3CO_Overview.md) to learn about the tool's capabilities

## Troubleshooting

If you encounter any issues during installation:

- Make sure your Python environment is activated (you should see `(t3co)` in your terminal prompt)
- Check that you're using a compatible Python version (3.8, 3.9, or 3.10)
- For permission errors, try adding `--user` to your pip commands (e.g., `pip install --user t3co`)
- If you're behind a corporate firewall, you might need to configure pip to use a proxy
