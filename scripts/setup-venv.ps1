param(
    [string] $pythonPath,
    [string] $venvName
)

. .\scripts\_lib.ps1

if (-not($venvName)) { $venvName = ".venv" }

Setup_Venv $pythonPath $name
