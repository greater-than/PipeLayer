param(
    [string] $pythonPath,
    [string] $venv
)

. .\scripts\_lib.ps1

if (-not($venvName)) { $venvName = ".venv" }

Write_Header "Project Setup"
Clean_Project
Setup_Venv $pythonPath $name
Install_Requirements
Install_PreCommit_Hooks
