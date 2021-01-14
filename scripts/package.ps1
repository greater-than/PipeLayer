. .\scripts\_lib

try {
    Create_Package
}
catch {
    Write-Host "*** Creating Python Package Failed ***"
    Write-Host "##vso[task.complete result=failed]"
    throw
}
