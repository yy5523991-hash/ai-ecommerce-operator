$ErrorActionPreference = "Stop"

$SkillName = "ai-ecommerce-operator"
$Repo = "yy5523991-hash/ai-ecommerce-operator"
$Branch = "main"

if ($env:CODEX_HOME) {
    $CodexHome = $env:CODEX_HOME
} else {
    $CodexHome = Join-Path $HOME ".codex"
}

$SkillsDir = Join-Path $CodexHome "skills"
$TargetDir = Join-Path $SkillsDir $SkillName
$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("$SkillName-" + [System.Guid]::NewGuid().ToString("N"))
$ZipPath = Join-Path $TempRoot "skill.zip"
$ArchiveUrl = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"

New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

Write-Host "Downloading $SkillName from GitHub..."
Invoke-WebRequest -Uri $ArchiveUrl -OutFile $ZipPath

Write-Host "Extracting..."
Expand-Archive -Path $ZipPath -DestinationPath $TempRoot -Force
$SourceDir = Get-ChildItem -Path $TempRoot -Directory | Select-Object -First 1
if (-not $SourceDir) {
    throw "Downloaded archive did not contain a skill folder."
}

foreach ($Required in @("SKILL.md", "agents", "references", "scripts")) {
    if (-not (Test-Path (Join-Path $SourceDir.FullName $Required))) {
        throw "Missing required skill item: $Required"
    }
}

if (Test-Path $TargetDir) {
    $BackupDir = "$TargetDir.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "Existing skill found. Moving it to $BackupDir"
    Move-Item -Path $TargetDir -Destination $BackupDir
}

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
Copy-Item -Path (Join-Path $SourceDir.FullName "SKILL.md") -Destination $TargetDir -Force
Copy-Item -Path (Join-Path $SourceDir.FullName "agents") -Destination $TargetDir -Recurse -Force
Copy-Item -Path (Join-Path $SourceDir.FullName "references") -Destination $TargetDir -Recurse -Force
Copy-Item -Path (Join-Path $SourceDir.FullName "scripts") -Destination $TargetDir -Recurse -Force

Remove-Item -Path $TempRoot -Recurse -Force

Write-Host "Installed: $TargetDir"
Write-Host "Restart Codex if the skill does not appear immediately."
