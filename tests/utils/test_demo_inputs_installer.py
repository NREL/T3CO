import shutil
import subprocess
import tempfile
from pathlib import Path

from t3co.utils.demo_inputs_installer import copy_demo_input_files, main


def test_install_t3co_demo_inputs():
    # Create a temporary directory to act as the destination for demo input files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define the command to run the script
        command = ["install_t3co_demo_inputs"]

        # Use subprocess to run the command
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Simulate user input for the script
        stdout, stderr = process.communicate(input=f"y\n{temp_dir}\n")

        # Check the output and error streams
        assert (
            "Do you want to copy the t3co demo input files? (y/n): Enter the path where you want to copy demo input files: "
            in stdout
        )
        assert process.returncode == 0

        # Verify that the demo input files were copied to the temporary directory
        # Replace 'expected_file' with the actual file you expect to be copied
        expected_folder = Path(temp_dir) / "demo_inputs"
        assert expected_folder.exists()

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)


def test_main_copy_files(mocker):
    mocker.patch("builtins.input", side_effect=["y", "/path/to/destination"])
    mock_copy_demo_input_files = mocker.patch(
        "t3co.utils.demo_inputs_installer.copy_demo_input_files"
    )

    main()
    mock_copy_demo_input_files.assert_called_once_with("/path/to/destination")


def test_main_no_copy_files(mocker, capsys):
    mocker.patch("builtins.input", side_effect=["n"])
    mock_copy_demo_input_files = mocker.patch(
        "t3co.utils.demo_inputs_installer.copy_demo_input_files"
    )

    main()
    mock_copy_demo_input_files.assert_not_called()
    captured = capsys.readouterr()
    assert "Demo input files were not copied." in captured.out


def test_copy_demo_input_files(mocker):
    mock_makedirs = mocker.patch("os.makedirs")
    mock_copy = mocker.patch("shutil.copy")
    mock_copytree = mocker.patch("shutil.copytree")
    mock_iterdir = mocker.patch("pathlib.Path.iterdir")
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)

    mock_file = mocker.Mock()
    mock_file.is_file.return_value = True
    mock_file.name = "file.txt"
    mock_dir = mocker.Mock()
    mock_dir.is_file.return_value = False
    mock_dir.name = "dir"
    mock_iterdir.return_value = [mock_file, mock_dir]

    copy_demo_input_files("/path/to/destination")

    mock_makedirs.assert_called_once_with(Path("/path/to/destination/demo_inputs"))
    mock_copy.assert_called_once_with(
        mock_file, Path("/path/to/destination/demo_inputs/file.txt")
    )
    mock_copytree.assert_called_once_with(
        mock_dir, Path("/path/to/destination/demo_inputs/dir")
    )


def test_copy_demo_input_files_existing_destination(mocker):
    mock_makedirs = mocker.patch("os.makedirs")
    mock_copy = mocker.patch("shutil.copy")
    mock_copytree = mocker.patch("shutil.copytree")
    mock_iterdir = mocker.patch("pathlib.Path.iterdir")
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)

    mock_file = mocker.Mock()
    mock_file.is_file.return_value = True
    mock_file.name = "file.txt"
    mock_dir = mocker.Mock()
    mock_dir.is_file.return_value = False
    mock_dir.name = "dir"
    mock_iterdir.return_value = [mock_file, mock_dir]

    copy_demo_input_files("/path/to/destination")

    mock_makedirs.assert_not_called()
    mock_copy.assert_called_once_with(
        mock_file, Path("/path/to/destination/demo_inputs/file.txt")
    )
    mock_copytree.assert_called_once_with(
        mock_dir, Path("/path/to/destination/demo_inputs/dir")
    )
