pushd ..\python

if not exist ".\.venv" (
    echo "python virtual environment not found, creating"
    python -m venv .venv
)

if not exist ".\.venv" (
    echo "failed to create python virtual environment, this script may fail if python 3 is not installed"
)

if exist ".\.venv" (
    .\.venv\Scripts\activate.bat
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt
)

popd