# Stage everything, commit, push. Message optional.
#
#   .\scripts\push.ps1 "fix the citation validator"
#   .\scripts\push.ps1                 <- message generated from the diff
#
# Refuses to commit anything that looks like a credential. See
# scripts/precommit_check.py for what it blocks and how to override.

param([string]$Message = "")

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

# Pause before the window closes (e.g. double-clicked rather than run from
# an already-open terminal) so the output stays readable. Fires on every
# exit path, success or failure.
try {

$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command python3 -ErrorAction SilentlyContinue) }
if (-not $py) {
    Write-Error "python not found on PATH - needed for the credential scan."
    exit 1
}
$python = $py.Source

git add -A

git diff --cached --quiet
$hasStaged = ($LASTEXITCODE -ne 0)

if (-not $hasStaged) {
    Write-Host "Nothing to commit. Working tree is clean."
    $unpushed = git log '@{u}..HEAD' --oneline 2>$null
    if (-not $unpushed) { exit 0 }
    Write-Host "Local commits are ahead of the remote - pushing those."
}
else {
    & $python scripts/precommit_check.py
    if ($LASTEXITCODE -ne 0) { exit 1 }

    if ([string]::IsNullOrWhiteSpace($Message)) {
        $Message = (& $python scripts/commit_message.py).Trim()
        Write-Host "No message given, using: $Message"
    }

    git commit -q -m $Message
    if ($LASTEXITCODE -ne 0) { exit 1 }
    Write-Host "Committed: $Message"
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()

git rev-parse --abbrev-ref '@{u}' 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    git push
}
else {
    Write-Host "Branch '$branch' has no upstream yet - setting it."
    git push -u origin HEAD
}
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "Pushed $branch."

} finally {
    Start-Sleep -Seconds 8
}
