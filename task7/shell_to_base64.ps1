$in_p = (Resolve-Path (Join-Path $PSScriptRoot "\shell.ps1")).Path
$out_p = Join-Path $PSScriptRoot "\shell.ps1.b64"
$content = [IO.File]::ReadAllText($in_p)
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($content)) | Out-File $out_p
