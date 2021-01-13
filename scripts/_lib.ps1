function Write_Header {
    param(
        [string] $message
    )
    Write-Host "================================================================================"
    Write-Host $message
}

function Write_Banner {
    param(
        [string] $message
    )
    Write-Host "--------------------------------------------------------------------------------"
    Write-Host $message
}

function Write_Command {
    param(
        [string] $command,
        [string] $arguments
    )
    Write-Host "CMD: " -NoNewline
    Write-Host $command $arguments
    Write-Host ""
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
        [Parameter(Mandatory = $false)][string] $venvName
    )

    try {
        if (-not($venvName)) { $venvName = ".venv" }

        if (-not (Get-Command "virtualenv")) {
            Write_Banner "Installing virtualenv"
            $arguments = "install virtualenv"
            Execute_Command "pip" $arguments
        }

        Write_Banner "Creating Virtual Environment: $venvName"
        $arguments = "-m virtualenv $venvName --pip=20.3.3 --download"
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
        [Parameter(Mandatory = $false)][string] $venvName
    )

    if (-not($venvName)) { $venvName = ".venv" }
    if (Test-Path -Path $venvName -PathType Container) {
        Write_Banner "Activating Virtual Environment: $venvName"
        & ".\$venvName\Scripts\activate.ps1"
    }
    else {
        Write-Host "WARNING: No venv, using build host installed packages"
    }
}

function Install_Requirements {
    try {
        Write_Banner "Install Packages"
        $arguments = "install -r requirements.txt"
        Execute_Command "pip" $arguments
    }
    catch {
        Write-Host "*** Installing Requirements Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Install_Tools {
    if (-Not(Test-Path -Path ".tools" -PathType Container)) {
        New-Item -Name ".tools" -ItemType Directory
    }
    Write_Banner "Installing NuGet"
    Invoke-WebRequest -Uri https://dist.nuget.org/win-x86-commandline/latest/nuget.exe -Outfile .tools\nuget.exe
    .tools\nuget.exe install GitVersion.CommandLine -Version 5.3.7 -outputdirectory .tools
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
        [string] $sourceDirectory
    )
    try {
        Write_Banner "Run MyPy Analysis"
        Execute_Command "mypy" $sourceDirectory
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

function Run_Unit_Tests {
    try {
        Write_Banner "Run Unit Tests"
        $arguments = "-m pytest -m unit --nunit-xml=.test_results/unit-test-results.xml"
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Run Unit Tests Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Run_Integration_Tests {
    try {
        Write_Banner "Run Unit Tests"
        $arguments = "-m pytest -m integration --nunit-xml=.test_results/integration-test-results.xml"
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Run Integration Tests Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}

function Create_Package {
    try {
        Write_Banner "Create Package"
        $arguments = "./src/setup.py sdist bdist_wheel"
        Execute_Command "python" $arguments
    }
    catch {
        Write-Host "*** Create Package Failed ***"
        Write-Host "##vso[task.complete result=failed]"
        throw
    }
}


