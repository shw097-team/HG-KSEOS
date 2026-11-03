<#
OWNER PROMPT — the primary passphrase UI for HGK/PIPD owner operations.

One masked prompt (dots), no echo, no history, no file. It posts the secret to the waiting
Python process over loopback (127.0.0.1) and then exits; the secret never touches the disk.

Parameters
  -Purpose   text shown in the window title/body
  -Port      loopback port of the waiting owner_prompt / owner_window process
  -Token     one-time token that authorises the post
  -MinLen    minimum accepted length (default 12)
  -Generate  "1" -> ENTER on an empty entry generates a passphrase and shows it once
#>
param(
    [Parameter(Mandatory = $true)][string]$Purpose,
    [Parameter(Mandatory = $true)][int]$Port,
    [Parameter(Mandatory = $true)][string]$Token,
    [int]$MinLen = 12,
    [string]$Generate = "0"
)

$ErrorActionPreference = "Stop"
function Get-Plain([System.Security.SecureString]$s) {
    $b = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($b) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($b) }
}
function Post-Secret([string]$secret) {
    $body = @{ token = $Token; passphrase = $secret } | ConvertTo-Json -Compress
    try {
        Invoke-RestMethod -Method Post -Uri ("http://127.0.0.1:{0}/submit" -f $Port) `
            -ContentType "application/json" -Body $body -TimeoutSec 20 | Out-Null
        return @{ ok = $true }
    } catch {
        $msg = $_.Exception.Message
        try { $r = $_.ErrorDetails.Message | ConvertFrom-Json; if ($r.error) { $msg = $r.error } } catch {}
        return @{ ok = $false; message = $msg }
    }
}

Write-Host ""
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ("  " + $Purpose) -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "  * masked input: nothing is echoed, stored or written to disk"
if ($Generate -eq "1") {
    Write-Host "  * press ENTER on an empty entry to GENERATE one for you"
}
Write-Host ""

$sent = $false
for ($i = 1; $i -le 3; $i++) {
    $s = Read-Host -AsSecureString ("  passphrase ({0}+ chars):" -f $MinLen)
    $p = Get-Plain $s
    if ([string]::IsNullOrEmpty($p)) {
        if ($Generate -eq "1") {
            $chars = (48..57) + (65..90) + (97..122)
            $p = -join (1..28 | ForEach-Object { [char]($chars | Get-Random) })
            Write-Host ""
            Write-Host "  GENERATED (save it now, shown once):" -ForegroundColor Green
            Write-Host ("      " + $p) -ForegroundColor White
            Write-Host ""
        } else {
            Write-Host "  -> empty; try again" -ForegroundColor Red
            continue
        }
    }
    if ($p.Length -lt $MinLen) {
        Write-Host ("  -> only {0} chars, need {1}" -f $p.Length, $MinLen) -ForegroundColor Red
        $p = $null
        continue
    }
    $res = Post-Secret $p
    $p = $null
    if ($res.ok) { $sent = $true; break }
    Write-Host ("  -> rejected: " + $res.message) -ForegroundColor Red
}
if ($sent) {
    Write-Host "  accepted. You can close this window." -ForegroundColor Green
} else {
    Write-Host "  not accepted after 3 attempts - close this window and check the console." -ForegroundColor Red
}
Start-Sleep -Milliseconds 800
