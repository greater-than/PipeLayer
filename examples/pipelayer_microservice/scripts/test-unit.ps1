param(
    [parameter(Mandatory = $false)][string] $markers
)

. .\scripts\_lib.ps1

Run_Unit_Tests $markers
