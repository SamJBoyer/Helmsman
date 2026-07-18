# Copies Helmsman/canon/c_hDocs -> ./hDocs, moves HELMSMAN.md to repo root,
# then deletes the Helmsman clone. Run from the target project root.

param(
    [string]$HelmsmanDir = "Helmsman",
    [string]$ProjectRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$clone = Join-Path $ProjectRoot $HelmsmanDir
$source = [IO.Path]::Combine($ProjectRoot, $HelmsmanDir, "canon", "c_hDocs")
$hDocs = Join-Path $ProjectRoot "hDocs"
$helmsmanMd = Join-Path $hDocs "HELMSMAN.md"
$rootHelmsmanMd = Join-Path $ProjectRoot "HELMSMAN.md"

if (-not (Test-Path $source -PathType Container)) {
    Write-Error "Source not found: $source"
}

if (Test-Path $hDocs) {
    Write-Error "hDocs already exists at $hDocs — refuse to overwrite."
}

if (Test-Path $rootHelmsmanMd) {
    Write-Error "HELMSMAN.md already exists at $rootHelmsmanMd — refuse to overwrite."
}

Copy-Item -Path $source -Destination $hDocs -Recurse

if (-not (Test-Path $helmsmanMd -PathType Leaf)) {
    Write-Error "Expected HELMSMAN.md after copy, but missing: $helmsmanMd"
}

Move-Item -Path $helmsmanMd -Destination $rootHelmsmanMd

Remove-Item -Path $clone -Recurse -Force

Write-Host "Seeded hDocs from $source"
Write-Host "Moved HELMSMAN.md to $rootHelmsmanMd"
Write-Host "Removed Helmsman clone at $clone"
