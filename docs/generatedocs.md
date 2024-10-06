# Generate Documentation
## Generate MD Documentation from Docstrings (For Developers)
**On Windows**

```bash
pip install --user pipx
pipx ensurepath
```

**On Mac**
```bash
brew install pipx
pipx ensurepath
```

Then from T3CO root directory
```bash
pipx install pydoc-markdown
pydoc-markdown -I . -p t3co --render-toc > docs/functions/CodeReference.md
```
for specific modules, specify the module name after `-m`:
`pydoc-markdown -I . -m t3co/sweep --render-toc > docs/functions/sweep.md`

This generates CodeReference.md including a Table of Contents from all python docstrings in the T3CO package

## Generate MKDocs server for documentation website  (For Developers)
Use the `mkdocs.yml` file to configure the documentation website on localhost. `mkdocs` and `mkdocstrings` should get installed along with other dependencies when running `pip install -e .` from the root directory. In case it throws an error, these packages can be installed separately:
```bash
pip install mkdocs mkdocstrings-python
```
**On Mac**

List the processes using the 8000 port on localhost using the command:
```bash
lsof -i tcp:8000
```
if a PID number shows up in the list for a process called `Python`, clear the port by killing it by replacing <PID> in the following command: 
```bash
kill -9 <PID>
```
Once the port is cleared, run the following line from the T3CO root directory to generate an MKDocs interactive documentation website on your localhost
```bash
mkdocs serve
```