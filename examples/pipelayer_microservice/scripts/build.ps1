. .\scripts\_lib.ps1

Write_Header "Build Package"
Clean_Project

Setup_Venv
Install_Requirements

Run_PreCommit_Checks
Run_Unit_Tests

Write_Footer "Build Complete. The package is ready to be published."
