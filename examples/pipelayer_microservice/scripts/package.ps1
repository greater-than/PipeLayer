. .\scripts\_lib

try {
    Delete_Build_Artifacts
    Create_Package
}
catch {
    Write-Host "*** Creating Python Package Failed ***"
    Write-Host "##vso[task.complete result=failed]"
    throw
}
