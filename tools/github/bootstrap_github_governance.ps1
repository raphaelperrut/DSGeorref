[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Repo = "raphaelperrut/DSGeorref",

    [Parameter(Mandatory = $false)]
    [string]$ProjectOwner = "raphaelperrut",

    [Parameter(Mandatory = $true)]
    [int]$ProjectNumber,

    [Parameter(Mandatory = $false)]
    [ValidateSet("user", "organization")]
    [string]$OwnerType = "user",

    [Parameter(Mandatory = $false)]
    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$applyArg = @()
if ($Apply) {
    $applyArg = @("--apply")
}

Write-Host "=== DSGeorref GitHub Governance Bootstrap ==="
Write-Host "Mode: $($(if ($Apply) { 'APPLY' } else { 'DRY-RUN' }))"

python tools/github/sync_project_fields.py `
    --repo $Repo `
    --owner $ProjectOwner `
    --owner-type $OwnerType `
    --project-number $ProjectNumber `
    --sprint SPRINT-001 `
    --sprint SPRINT-002 `
    --create-missing-fields `
    --sync-field-options `
    --add-missing-items `
    @applyArg
if ($LASTEXITCODE -ne 0) { throw "sync_project_fields.py falhou" }

python tools/github/sync_labels.py `
    --repo $Repo `
    @applyArg
if ($LASTEXITCODE -ne 0) { throw "sync_labels.py falhou" }

python tools/github/sync_milestones.py `
    --repo $Repo `
    --sprint SPRINT-001 `
    --sprint SPRINT-002 `
    @applyArg
if ($LASTEXITCODE -ne 0) { throw "sync_milestones.py falhou" }

python tools/github/configure_project_automations.py `
    --owner $ProjectOwner `
    --owner-type $OwnerType `
    --project-number $ProjectNumber `
    @applyArg
if ($LASTEXITCODE -ne 0) { throw "configure_project_automations.py falhou" }

python tools/github/enable_native_fields.py `
    --owner $ProjectOwner `
    --owner-type $OwnerType `
    --project-number $ProjectNumber `
    @applyArg
if ($LASTEXITCODE -ne 0) { throw "enable_native_fields.py falhou" }

Write-Host "=== Concluído ==="
Write-Host "Os workflows built-in e os campos visíveis por view ainda exigem a etapa manual descrita no README."
