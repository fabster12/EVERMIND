<#
.SYNOPSIS
    Convert capstone .docx files to PDF using the installed Microsoft Word.

.DESCRIPTION
    LibreOffice, pandoc and docx2pdf are not installed on this machine, but
    Word is, so this drives Word over COM. Word is kept invisible and is always
    shut down in the finally block, so a failed conversion does not leave an
    orphan WINWORD.EXE holding a lock on the file.

.PARAMETER Path
    One or more .docx files. Defaults to every .docx under docs/ (gate1
    deliverables and review documents).

.EXAMPLE
    # Convert every generated .docx under docs/ (the usual case):
    powershell -ExecutionPolicy Bypass -File tools/packaging/to_pdf.ps1

    # One named file:
    powershell -ExecutionPolicy Bypass -File tools/packaging/to_pdf.ps1 -Path One.docx

    # Several files: `powershell -File` binds only the first argument to
    # -Path, so use -Command for a list.
    powershell -ExecutionPolicy Bypass -Command "& tools/packaging/to_pdf.ps1 -Path One.docx,Two.docx"
#>

param(
    [string[]]$Path
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

if (-not $Path -or $Path.Count -eq 0) {
    # Generated .docx live under docs/ - gate1 for deliverables, reviews for
    # working documents. Nothing is generated into the project root.
    $Path = Get-ChildItem -Path (Join-Path $projectRoot 'docs') -Filter '*.docx' -Recurse |
            Where-Object { $_.Name -notlike '~$*' } |
            ForEach-Object { $_.FullName }
}

if (-not $Path -or $Path.Count -eq 0) {
    Write-Error 'No .docx files found to convert.'
    exit 1
}

# Resolve to absolute paths up front - Word COM does not honour the
# PowerShell working directory and will silently look in Documents.
$docs = @()
foreach ($p in $Path) {
    $resolved = Resolve-Path -Path $p -ErrorAction SilentlyContinue
    if (-not $resolved) {
        Write-Warning "Skipping (not found): $p"
        continue
    }
    $docs += $resolved.Path
}

if ($docs.Count -eq 0) {
    Write-Error 'None of the given paths exist.'
    exit 1
}

$wdFormatPDF = 17
$word = $null
$converted = 0

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    foreach ($docPath in $docs) {
        $pdfPath = [System.IO.Path]::ChangeExtension($docPath, '.pdf')
        Write-Host "Converting: $([System.IO.Path]::GetFileName($docPath))"

        $doc = $null
        try {
            # ReadOnly, no add-ins prompt, do not add to recent files.
            $doc = $word.Documents.Open($docPath, $false, $true)

            # Refresh TOC/page-number fields so PAGE and NUMPAGES resolve in
            # the PDF rather than rendering as a stale value.
            $doc.Fields.Update() | Out-Null

            $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)
            $converted++
            Write-Host "       -> $([System.IO.Path]::GetFileName($pdfPath))"
        }
        finally {
            if ($doc) {
                $doc.Close([ref]$false)
                [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
            }
        }
    }
}
finally {
    if ($word) {
        $word.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

Write-Host ''
Write-Host "Converted $converted file(s)."
