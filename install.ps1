param (
    [switch]$Wsl
)

python -m build
pip install --force-reinstall ".\dist\aoc-0.0.2-py3-none-any.whl"

