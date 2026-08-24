[CmdletBinding()]
param(
    [string]$BaseRef
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot

function Invoke-Gate {
    param([string]$Name, [scriptblock]$Command)
    Write-Host "==> $Name"
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE."
    }
}

$python = (Get-Command python -ErrorAction Stop).Source
$git = (Get-Command git -ErrorAction Stop).Source
$gitRoot = Split-Path -Parent (Split-Path -Parent $git)
$bash = Join-Path $gitRoot 'bin\bash.exe'
if (-not (Test-Path -LiteralPath $bash)) {
    throw 'Git for Windows Bash was not found. Install Git for Windows.'
}
$npm = (Get-Command npm.cmd -ErrorAction Stop).Source

Push-Location $repoRoot
try {
    $env:PYTHONUTF8 = '1'
    Invoke-Gate 'Install pinned maintainer tools' {
        & $npm ci --ignore-scripts --no-audit --no-fund
    }
    $skillsRef = Join-Path $repoRoot 'node_modules\.bin\skills-ref.cmd'
    Invoke-Gate 'Maintenance unit tests' {
        & $python -m unittest discover -s tests -p 'test_*.py' -v
    }
    Invoke-Gate 'Repository contract' { & $python tools/check_repo_contract.py }
    Invoke-Gate 'mission-log harvest tests' {
        & $python skills/mission-log/tests/harvest_test.py
    }
    foreach ($shell in @('sh', 'bash')) {
        Invoke-Gate "ai-review matrix ($shell on Git Bash/NTFS)" {
            $env:SH = $shell
            & $bash skills/ai-review/tests/matrix.sh
        }
    }
    Remove-Item Env:SH -ErrorAction SilentlyContinue
    foreach ($skill in Get-ChildItem -LiteralPath skills -Directory | Sort-Object Name) {
        Invoke-Gate "skills-ref validate $($skill.Name)" {
            & $skillsRef validate $skill.FullName
        }
    }
    Invoke-Gate 'Windows AI Desktop/TUI/CLI isolated install smoke' {
        & pwsh -NoProfile -File tools/windows_agent_smoke.ps1
    }
    Invoke-Gate 'git diff --check (unstaged)' { git diff --check }
    Invoke-Gate 'git diff --cached --check (staged)' { git diff --cached --check }
    if (-not [string]::IsNullOrWhiteSpace($BaseRef)) {
        $baseCommit = (& git rev-parse --verify "$BaseRef^{commit}" 2>$null | Select-Object -First 1)
        if ($LASTEXITCODE -eq 0 -and $baseCommit) {
            Invoke-Gate "git diff --check $baseCommit..HEAD" { git diff --check "$baseCommit..HEAD" }
        } else {
            Write-Host "WARN: BaseRef '$BaseRef' is unavailable; checking HEAD commit."
            Invoke-Gate 'git show --check HEAD fallback' { git show --check --format= HEAD }
        }
    }
    Write-Host 'DEV CHECK PASSED'
} finally {
    Remove-Item Env:SH -ErrorAction SilentlyContinue
    Pop-Location
}
