param(
    [parameter(Mandatory = $false)][string] $markers
)

. .\scripts\_lib.ps1

Run_Integration_Tests $markers
