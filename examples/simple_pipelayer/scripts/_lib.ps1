function Write_Header {
    param(
        [string] $message
    )
    Write-Host ================================================================================ -ForegroundColor DarkCyan
    Write-Host $message
}

function Write_Banner {
    param(
        [string] $message
    )
    Write-Host -------------------------------------------------------------------------------- -ForegroundColor DarkCyan
    Write-Host $message -ForegroundColor Gray
}

function Write_Footer {
    param(
        [string] $message
    )
    Write-Host -------------------------------------------------------------------------------- -ForegroundColor DarkCyan
    Write-Host $message
    Write-Host ================================================================================ -ForegroundColor DarkCyan
    Write_GreaterThan
}

function Write_GreaterThan {
    Write-Host greater -NoNewline -ForegroundColor DarkCyan
    Write-Host Than -NoNewline -ForegroundColor DarkGreen
    Write-Host ", LLC    " -NoNewline -ForegroundColor DarkGray
    Write-Host info -NoNewline -ForegroundColor DarkGreen
    Write-Host "@" -NoNewline -ForegroundColor Gray
    Write-Host greaterthan.solutions -NoNewline -ForegroundColor DarkGreen
    Write-Host " | " -NoNewline -ForegroundColor DarkGray
    Write-Host https://github.com/greater-than -ForegroundColor DarkGreen
    Write-Host
}

function Write_Command {
    param(
        [string] $command,
        [string] $arguments
    )
    Write-Host "CMD: " -NoNewline -ForegroundColor DarkCyan
    Write-Host $command $arguments
    Write-Host
}

function Execute_Command {
    param(
        [string] $command,
        [string] $arguments
    )
    Write_Command $command $arguments
    $process = Start-Process -FilePath $command -ArgumentList $arguments -NoNewWindow -Wait -PassThru

    if ($process.ExitCode -ne 0) {
        Write-Host "Process ended with exit code: " $process.ExitCode
        throw "Error during process"
    }
}

function Setup_Venv {
    param(
        [string] $pythonPath,
        [string] $venvName
    )

    try {
        if (-not($venvName)) { $venvName = ".venv" }
        if ($pythonPath) { $python = " --python=$pythonPath" }

        Write_Banner "Installing virtualenv"
        $arguments = "install virtualenv"
        Execute_Command "pip" $arguments

        Write_Banner "Create Virtual Environment: $venvName"
        $arguments = "-m virtualenv $venvName --pip=21.0.0 --download $python"
        Execute_Command "python" $arguments

        Activate_Venv $venvName
    }
    Catch {
        Write-Host "*** Setup/Activation of Virtual Environment failed ***"
        Write-Host "##vso[task.complete result=Failed]"
        throw
    }
}

function Activate_Venv {
    param(
        [string] $venvName
    )

    if (-not($venvName)) { $venvName = ".venv" }
    if (Test-Path -Path $venvName -PathType Container) {
        Write_Banner "Activate Virtual Environment: $venvName"
        & ".\$venvName\Scripts\activate.ps1"
    }
    else {
        Write-Host "WARNING: No venv, using build host installed packages"
    }
}

function Install_Requirements {
    try {
        Write_Banner "Install Requirements"
        $arguments = "install -r requirements.txt"
        Execute_Command "pip" $arguments
    }
    catch {
        Write-Host "*** Installing Requirements Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Install_Poetry {
    try {
        if (-Not(Get-Command -Name "poetry")) {
            Write_Banner "Install Poetry"
            (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
        }
        else {
            Write_Banner "Upgrading Poetry"
            $arguments = "self update"
            Execute_Command "poetry" $arguments
        }
    }
    catch {
        Write-Host "*** Installing Poetry Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Install_PreCommit_Hooks {
    try {
        Write_Banner "Install Pre-Commit Hooks"
        $arguments = "install"
        Execute_Command "pre-commit" $arguments
    }
    catch {
        Write-Host "*** Installing Pre-Commit Hooks Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Run_Linting {
    try {
        Write_Banner "Run Linting"
        $arguments = "-m flake8 --config=.flake8"
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Linting Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Run_PreCommit_Checks {
    try {
        Write_Banner "Run Pre-Commit Checks"
        $arguments = "run --all-files"
        Execute_Command "pre-commit" $arguments
    }
    catch {
        Write-Host "*** Pre-Commit Checks Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Run_MyPy {
    param(
        [string] $directories
    )
    if (-not($directories)) { $directories = "src" }
    try {
        Write_Banner "Run MyPy Analysis"
        Execute_Command "mypy" $directories
    }
    catch {
        Write-Host "*** MyPy Analysis Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Delete_PyCache {
    try {
        Write_Banner "Delete .py[co] files"
        $arguments = "-Bc ""import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"""
        Execute_Command "python" $arguments

        Write_Banner "Delete __pycache__ directories"
        $arguments = "-Bc ""import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"""
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Delete PyCache Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Delete_Virtual_Environment {
    param(
        [string] $venvName
    )

    if (-not($venvName)) { $venvName = ".venv" }
    if (Test-Path -Path $venvName -PathType Container) {
        Write_Banner "De-activate Virtual Environment"
        & ".\$venvName\Scripts\deactivate.bat"
    }

    if (Test-Path -Path $venvName) {
        Write_Banner "Delete Virtual Environment"
        Remove-Item $venvName -Recurse -Force
    }
}

function Clean_Project {
    try {
        Write_Header "Clean Project"
        Delete_Virtual_Environment
        Delete_PyCache
    }
    catch {
        Write-Host "*** Delete PyCache Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Run_Unit_Tests {
    param(
        [string] $markers
    )
    if ($markers) { $markers = "unit and $markers" } else { $markers = "unit" }
    try {
        Write_Banner "Run Unit Tests"
        $arguments = "-m pytest -m ""$markers"" --nunit-xml=.test_results/unit-test-results.xml --cov=src --cov-config=pyproject.toml"
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Run Unit Tests Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Run_Integration_Tests {
    param(
        [string] $markers
    )
    if ($markers) { $markers = "integration and $markers" } else { $markers = "integration" }
    try {
        Write_Banner "Run Integration Tests"
        $arguments = "-m pytest -m ""$markers"" --nunit-xml=.test_results/integration-test-results.xml"
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Run Integration Tests Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}
