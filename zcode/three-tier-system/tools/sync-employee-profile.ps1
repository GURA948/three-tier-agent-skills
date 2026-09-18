# Sync or compare the distributable employee profile with ZCode's live profile.

param(
  [string]$Target,
  [switch]$Check,
  [switch]$Replace
)

$ErrorActionPreference = "Stop"

function Get-Sha256([string]$Path) {
  $stream = [IO.File]::OpenRead($Path)
  try {
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
      return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace("-", "")
    } finally {
      $sha.Dispose()
    }
  } finally {
    $stream.Dispose()
  }
}

$sourcePath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\profiles\employee.md"))
if (-not $Target) {
  $Target = Join-Path $env:USERPROFILE ".zcode\agents\employee.md"
}
$targetPath = [IO.Path]::GetFullPath($Target)

if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
  Write-Error "canonical employee profile not found: $sourcePath"
  exit 5
}

if ($Check) {
  if (-not (Test-Path -LiteralPath $targetPath -PathType Leaf)) {
    Write-Output "MISSING: $targetPath"
    exit 3
  }
  $sourceHash = Get-Sha256 $sourcePath
  $targetHash = Get-Sha256 $targetPath
  if ($sourceHash -ne $targetHash) {
    Write-Output "DRIFT: canonical=$sourceHash live=$targetHash target=$targetPath"
    exit 3
  }
  Write-Output "MATCH: $targetPath"
  exit 0
}

$sourceHash = Get-Sha256 $sourcePath
if (Test-Path -LiteralPath $targetPath -PathType Leaf) {
  $targetHash = Get-Sha256 $targetPath
  if ($sourceHash -eq $targetHash) {
    Write-Output "MATCH: $targetPath"
    exit 0
  }
  if (-not $Replace) {
    Write-Output "CONFLICT: existing profile differs; inspect it and rerun with -Replace only if this overwrite is intended: $targetPath"
    exit 3
  }
}

$targetDir = Split-Path -Parent $targetPath
if (-not (Test-Path -LiteralPath $targetDir -PathType Container)) {
  New-Item -ItemType Directory -Path $targetDir | Out-Null
}
$backupPath = $null
if (Test-Path -LiteralPath $targetPath -PathType Leaf) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss-fffffff"
  $backupPath = $targetPath + ".backup." + $stamp
}
$tempPath = $targetPath + ".tmp." + $PID
[IO.File]::WriteAllBytes($tempPath, [IO.File]::ReadAllBytes($sourcePath))
if (Test-Path -LiteralPath $targetPath -PathType Leaf) {
  [IO.File]::Replace($tempPath, $targetPath, $backupPath)
  Write-Output "BACKUP: $backupPath"
} else {
  Move-Item -LiteralPath $tempPath -Destination $targetPath
}
Write-Output "SYNCED: $sourcePath -> $targetPath"
Write-Output "Restart ZCode or open a new session before relying on the updated role."
