. .\scripts\_lib.ps1

Write_Header "Project Setup"
Setup_Venv ".venv"
Install_Requirements
Install_PreCommit_Hooks
Install_Tools
