param(
    [string]$CodexHome = ""
)

$ErrorActionPreference = "Stop"

$SkillName = "ecommerce-visual-strategy"
$Repo = "yy5523991-hash/ecommerce-ai-design-system"
$Branch = "main"
$SkillPath = "skills/ecommerce-visual-strategy"
$RepoIsPrivate = $true

function Initialize-ProxyFromWindows {
    if ($env:HTTPS_PROXY -or $env:HTTP_PROXY) { return }
    try {
        $settings = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -ErrorAction Stop
        if ($settings.ProxyEnable -ne 1 -or -not $settings.ProxyServer) { return }
        $proxy = [string]$settings.ProxyServer
        if ($proxy -match "=") {
            $parts = @{}
            foreach ($item in $proxy.Split(";")) {
                $kv = $item.Split("=", 2)
                if ($kv.Count -eq 2) { $parts[$kv[0].ToLowerInvariant()] = $kv[1] }
            }
            $proxy = $parts["https"]
            if (-not $proxy) { $proxy = $parts["http"] }
            if (-not $proxy) { return }
        }
        if ($proxy -notmatch "^[a-zA-Z][a-zA-Z0-9+.-]*://") { $proxy = "http://$proxy" }
        $env:HTTP_PROXY = $proxy
        $env:HTTPS_PROXY = $proxy
    } catch {
        return
    }
}

function Resolve-CodexHome {
    param([string]$Override)
    if ($Override) { return $Override }
    if ($env:CODEX_HOME) { return $env:CODEX_HOME }
    return (Join-Path $HOME ".codex")
}

function Get-GhPath {
    $cmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $common = "C:\Program Files\GitHub CLI\gh.exe"
    if (Test-Path $common) { return $common }
    return ""
}

function Ensure-GitHubCli {
    $gh = Get-GhPath
    if ($gh) { return $gh }
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "GitHub CLI is required for private repositories. Install it from https://cli.github.com/ and rerun this script."
    }
    Write-Host "Installing GitHub CLI..."
    winget install --id GitHub.cli --exact --silent --accept-package-agreements --accept-source-agreements
    $gh = Get-GhPath
    if (-not $gh) { throw "GitHub CLI installation finished, but gh.exe was not found. Restart PowerShell and rerun this script." }
    return $gh
}

function Ensure-GhAuth {
    param([string]$Gh)
    & $Gh auth status *> $null
    if ($LASTEXITCODE -eq 0) { return }
    Write-Host "GitHub login is required. Complete the browser/device authorization that opens next."
    & $Gh auth login --hostname github.com --web --git-protocol https --scopes repo
    if ($LASTEXITCODE -ne 0) { throw "GitHub authentication failed." }
}

function Download-RepoArchive {
    param(
        [string]$Repo,
        [string]$Branch,
        [bool]$Private,
        [string]$OutputZip
    )
    $archiveUrl = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"
    if ($Private) {
        $gh = Ensure-GitHubCli
        Ensure-GhAuth -Gh $gh
        $token = (& $gh auth token).Trim()
        Invoke-WebRequest -Uri $archiveUrl -Headers @{ Authorization = "Bearer $token" } -OutFile $OutputZip
    } else {
        Invoke-WebRequest -Uri $archiveUrl -OutFile $OutputZip
    }
}

function Install-SkillFromArchive {
    param(
        [string]$SkillName,
        [string]$Repo,
        [string]$Branch,
        [string]$SkillPath,
        [bool]$RepoIsPrivate,
        [string]$CodexHome
    )

    $skillsDir = Join-Path $CodexHome "skills"
    $targetDir = Join-Path $skillsDir $SkillName
    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("$SkillName-" + [System.Guid]::NewGuid().ToString("N"))
    $zipPath = Join-Path $tempRoot "repo.zip"

    New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
    New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

    Write-Host "Downloading $SkillName..."
    Download-RepoArchive -Repo $Repo -Branch $Branch -Private $RepoIsPrivate -OutputZip $zipPath

    Expand-Archive -Path $zipPath -DestinationPath $tempRoot -Force
    $repoRoot = Get-ChildItem -Path $tempRoot -Directory | Select-Object -First 1
    if (-not $repoRoot) { throw "Downloaded archive did not contain repository files." }

    if ($SkillPath -eq "." -or $SkillPath -eq "") {
        $sourceDir = $repoRoot.FullName
    } else {
        $sourceDir = Join-Path $repoRoot.FullName $SkillPath
    }
    if (-not (Test-Path (Join-Path $sourceDir "SKILL.md"))) {
        throw "SKILL.md not found in $Repo/$SkillPath"
    }

    if (Test-Path $targetDir) {
        $backupDir = "$targetDir.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Write-Host "Existing $SkillName found. Backup: $backupDir"
        Move-Item -Path $targetDir -Destination $backupDir
    }

    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Copy-Item -Path (Join-Path $sourceDir "*") -Destination $targetDir -Recurse -Force
    Remove-Item -Path $TempRoot -Recurse -Force
    Write-Host "Installed $SkillName -> $targetDir"
}

$null = Initialize-ProxyFromWindows
$resolvedCodexHome = Resolve-CodexHome -Override $CodexHome
Install-SkillFromArchive -SkillName $SkillName -Repo $Repo -Branch $Branch -SkillPath $SkillPath -RepoIsPrivate $RepoIsPrivate -CodexHome $resolvedCodexHome
Write-Host "Done. Restart Codex if the skill does not appear immediately."
