import shutil
import os
from pathlib import Path

def main():
    """
    This function requests user inputs for whether and where to copy T3CO demo input files from the t3co.resources folder. It then calls the copy_demo_input_files function.
    """
    choice = input("Do you want to copy the T3CO demo input files? (y/n): ").strip().lower()
    if choice == "y":
        destination_path = input("Enter the path where you want to copy demo input files: ").strip()
        copy_demo_input_files(destination_path)
    else:
        print("Demo input files were not copied.")

def copy_demo_input_files(destination_path:str):
    """
    This function copies the t3co.resources folder that includes demo input files to a user input destination_path.

    Args:
        destination_path (str | Path): Path of destination directory for copying t3co.resources folder
    """
    source_path = Path(__file__).parents[1] / 'resources'
    destination_path = Path(destination_path)/'demo_inputs'

    if not destination_path.exists():
        os.makedirs(destination_path)

    for item in source_path.iterdir():
        if item.is_file():
            shutil.copy(item, destination_path / item.name)
        else:
            shutil.copytree(item, destination_path / item.name)
    print(f"T3CO demo input files copied to {destination_path.resolve()}")
