#! /bin/bash

echo "Setting up virtual environment for Pybuster"
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt -q

while getopts ":h" option; do
    case "$option" in
        h|--help)
            python3 backend/cli.py --help
            exit
            ;;
    esac
done

TARGET_HOST=$1
echo "Running Pybuster for: ${TARGET_HOST}"
python3 backend/cli.py $TARGET_HOST
