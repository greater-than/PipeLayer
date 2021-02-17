. .\scripts\_lib.ps1

Setup_Venv
)

. .\scripts\_lib.ps1

if (-not($venvName)) { $venvName = ".venv" }

Setup_Venv $pythonPath $name
