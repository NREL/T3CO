# Table of Contents

* [t3co/utils/demo\_files\_installer](#t3co/utils/demo_files_installer)
  * [main](#t3co/utils/demo_files_installer.main)
  * [copy\_demo\_input\_files](#t3co/utils/demo_files_installer.copy_demo_input_files)

<a id="t3co/utils/demo_files_installer"></a>

# t3co/utils/demo\_files\_installer

<a id="t3co/utils/demo_files_installer.main"></a>

#### main

```python
def main()
```

Requests user inputs for whether and where to copy t3co demo input files from the t3co.resources folder. Calls the copy_demo_input_files function.

<a id="t3co/utils/demo_files_installer.copy_demo_input_files"></a>

#### copy\_demo\_input\_files

```python
def copy_demo_input_files(destination_path: Union[str, Path]) -> None
```

Copies the t3co.resources folder that includes demo input files to a user input destination_path.

**Arguments**:

- `destination_path` _Union[str, Path]_ - Path of destination directory for copying t3co.resources folder.

