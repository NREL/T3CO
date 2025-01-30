import pytest
from pathlib import Path
import os
import shutil
from t3co.utils.demo_files_installer import main, copy_demo_input_files


def test_main_copy_files(mocker):
    mocker.patch("builtins.input", side_effect=["y", "/path/to/destination"])
    mock_copy_demo_input_files = mocker.patch(
        "t3co.utils.demo_files_installer.copy_demo_input_files"
    )

    main()
    mock_copy_demo_input_files.assert_called_once_with("/path/to/destination")


def test_main_no_copy_files(mocker, capsys):
    mocker.patch("builtins.input", side_effect=["n"])
    mock_copy_demo_input_files = mocker.patch(
        "t3co.utils.demo_files_installer.copy_demo_input_files"
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
