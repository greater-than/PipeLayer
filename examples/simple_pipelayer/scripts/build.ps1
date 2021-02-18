param(
    [string] $pythonPath,
    [string] $venvName
)

. .\scripts\_lib.ps1

if (-not($venvName)) { $venvName = ".venv" }

Write_Header "Building..."
Clean_Project

Setup_Venv $pythonPath $venvName
Install_Requirements

Run_PreCommit_Checks
Run_Unit_Tests
