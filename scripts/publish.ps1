param(
    [parameter(Mandatory = $true)][boolean] $live
)

. .\scripts\_lib.ps1

Publish_Package  $live
Delete_Build_Artifacts
