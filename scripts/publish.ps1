param(
    [parameter(Mandatory = $true)][boolean] $live
)

Write-Host $live

. .\scripts\_lib.ps1

Publish_Package  $live
if ($live) { Delete_Build_Artifacts }
