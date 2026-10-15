# Pull the latest, keeping history readable and uncommitted work safe.
#
#   .\scripts\pull.ps1
#
# --rebase replays your commits on top of the remote instead of creating a
# merge bubble - with six people on one branch, merge-pull turns the log into
# something nobody reads. --autostash shelves uncommitted work first and
# restores it after, so a dirty tree is not a reason to refuse.

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

$branch = (git rev-parse --abbrev-ref HEAD).Trim()

git rev-parse --abbrev-ref '@{u}' 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Branch '$branch' has no upstream - nothing to pull from."
    Write-Host "Push it first:  .\scripts\push.ps1"
    exit 0
}

git pull --rebase --autostash
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Rebase stopped - the same lines changed on both sides."
    Write-Host ""
    Write-Host "  Fix the marked files, then:  git add <file> ; git rebase --continue"
    Write-Host "  Or back out entirely:        git rebase --abort"
    Write-Host ""
    Write-Host "Your uncommitted work is in the stash either way: git stash list"
    exit 1
}

Write-Host "Up to date with origin/$branch."
