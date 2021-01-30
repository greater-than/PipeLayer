. .\scripts\_lib.ps1

Write_Header "Building..."
Clean_Project

Setup_Venv
Install_Requirements

Run_PreCommit_Checks
Run_Unit_Tests
