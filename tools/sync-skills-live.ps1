<#
.SYNOPSIS
  Keeps D:\Git_Virevo\skills-live (the live vault folder the local application reads) identical to
  its git-tracked twins in Virevo-Project: vault\chat for the regular chat's files, and vault\tools
  for the tool request bundle (staged under skills-live\tools since 30 Sep 2026).

.DESCRIPTION
  Two pairs are checked, every run:
    vault\chat   <->  skills-live            (skills-live\backup and skills-live\tools ignored)
    vault\tools  <->  skills-live\tools
  Default: compare and list every difference. Exit code 0 when both pairs are identical, 1 when not.
  -Apply : copy vault -> skills-live for both pairs (after showing the differences). Never deletes; a
           file that exists only in skills-live is reported, not removed.
  -Pull  : copy skills-live -> vault for both pairs, for changes made directly in the live folder, so
           git has them before the next drop is applied. Never deletes.

  The tool bundle can sit inside skills-live because the vault loader and the publisher enumerate
  top-level *.md only: a subfolder is invisible to the regular chat and to a publish.

.EXAMPLE
  .\tools\sync-skills-live.ps1            # check
  .\tools\sync-skills-live.ps1 -Apply     # vault -> skills-live
  .\tools\sync-skills-live.ps1 -Pull      # skills-live -> vault
#>
param(
  [switch]$Apply,
  [switch]$Pull,
  [string]$Repo = (Split-Path $PSScriptRoot -Parent),
  [string]$Live = "D:\Git_Virevo\skills-live"
)
$ErrorActionPreference = "Stop"
if ($Apply -and $Pull) { throw "Use -Apply or -Pull, not both." }
if (-not (Test-Path $Live)) { throw "Live folder not found: $Live" }
$Repo = (Resolve-Path $Repo).Path

$pairs = @(
  @{ Name = "vault\chat  <-> skills-live";       Vault = (Join-Path $Repo "vault\chat");  Live = $Live;                    Skip = @("backup", "tools") },
  @{ Name = "vault\tools <-> skills-live\tools"; Vault = (Join-Path $Repo "vault\tools"); Live = (Join-Path $Live "tools"); Skip = @() }
)

function Get-Files($root, [string[]]$skip) {
  if (-not (Test-Path $root)) { return @() }
  $root = (Resolve-Path $root).Path.TrimEnd('\')
  Get-ChildItem -Path $root -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($root.Length).TrimStart('\')
    $skipped = $false
    foreach ($s in $skip) { if ($rel -like "$s\*") { $skipped = $true } }
    if (-not $skipped) { [pscustomobject]@{ Rel = $rel; Full = $_.FullName } }
  }
}
function Same($a, $b) { (Get-FileHash $a -Algorithm SHA256).Hash -eq (Get-FileHash $b -Algorithm SHA256).Hash }

$allClean = $true
foreach ($p in $pairs) {
  $v = @{}; Get-Files $p.Vault $p.Skip | ForEach-Object { $v[$_.Rel] = $_.Full }
  $l = @{}; Get-Files $p.Live  $p.Skip | ForEach-Object { $l[$_.Rel] = $_.Full }

  $onlyVault = @($v.Keys | Where-Object { -not $l.ContainsKey($_) } | Sort-Object)
  $onlyLive  = @($l.Keys | Where-Object { -not $v.ContainsKey($_) } | Sort-Object)
  $differ    = @($v.Keys | Where-Object { $l.ContainsKey($_) -and -not (Same $v[$_] $l[$_]) } | Sort-Object)

  Write-Host ("{0}: {1} files in the repo, {2} live" -f $p.Name, $v.Count, $l.Count)
  $onlyVault | ForEach-Object { Write-Host "  only in the repo  : $_" }
  $onlyLive  | ForEach-Object { Write-Host "  only in skills-live : $_" }
  $differ    | ForEach-Object { Write-Host "  differs           : $_" }

  $clean = ($onlyVault.Count + $onlyLive.Count + $differ.Count) -eq 0
  if ($clean) { Write-Host "  identical" -ForegroundColor Green; continue }
  $allClean = $false

  if ($Apply) {
    foreach ($rel in ($onlyVault + $differ)) {
      $dst = Join-Path $p.Live $rel
      New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
      Copy-Item -LiteralPath $v[$rel] -Destination $dst -Force
      Write-Host "  repo -> skills-live : $rel"
    }
    if ($onlyLive.Count) { Write-Host "  left in place (only in skills-live, nothing deleted): $($onlyLive -join ', ')" -ForegroundColor Yellow }
  } elseif ($Pull) {
    foreach ($rel in ($onlyLive + $differ)) {
      $dst = Join-Path $p.Vault $rel
      New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
      Copy-Item -LiteralPath $l[$rel] -Destination $dst -Force
      Write-Host "  skills-live -> repo : $rel"
    }
    if ($onlyVault.Count) { Write-Host "  left in place (only in the repo, nothing deleted): $($onlyVault -join ', ')" -ForegroundColor Yellow }
  }
}

if ($allClean) { Write-Host "IDENTICAL - skills-live is current (both pairs)." -ForegroundColor Green; exit 0 }
if ($Apply) { Write-Host "APPLIED. Run again without switches to confirm." -ForegroundColor Green; exit 0 }
if ($Pull)  { Write-Host "PULLED. Review with git diff, then run again without switches to confirm." -ForegroundColor Green; exit 0 }
Write-Host "NOT IDENTICAL - use -Apply (repo -> skills-live) or -Pull (skills-live -> repo)." -ForegroundColor Red
exit 1
