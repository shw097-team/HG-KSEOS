# Unactivated HGK Owner maintenance tool. Never run Enable/Sign as the Maker.
[CmdletBinding()]
param(
  [ValidateSet('Inspect','SelfTest','Enable','Sign','Revoke')][string]$Mode='Inspect',
  [string]$PlanPath,
  [string]$ExpectedPlanSha256,
  [string]$PayloadPath,
  [string]$ExpectedPayloadSha256,
  [string]$CertificateThumbprint,
  [string]$SignatureOutput,
  [string]$ExpectedRegistrySha256,
  [string]$TestRoot
)
$ErrorActionPreference='Stop'
$programData=[Environment]::GetFolderPath('CommonApplicationData')
$registryDir=Join-Path $programData 'HG-KSEOS/native-admission'
$registryPath=Join-Path $registryDir 'registry.json'
$identity=[Security.Principal.WindowsIdentity]::GetCurrent()
$sid=$identity.User.Value
$principal=[Security.Principal.WindowsPrincipal]::new($identity)
$isAdmin=$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if($Mode -eq 'Inspect'){
  [pscustomobject]@{schema='HGK-NATIVE-TRUST-INSPECT/1';os_sid=$sid;elevated_admin=$isAdmin;registry_exists=(Test-Path -LiteralPath $registryPath);private_key_accessed=$false;native_activation=$false}|ConvertTo-Json
  exit 0
}
if($Mode -ne 'SelfTest' -and -not $isAdmin){throw 'ERR_OWNER_ELEVATED_OS_PRINCIPAL_REQUIRED'}
Add-Type @'
using System; using System.Runtime.InteropServices; using Microsoft.Win32.SafeHandles;
public static class HgkOwnerHandles {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)]
 public static extern SafeFileHandle CreateFile(string p,uint access,uint share,IntPtr sa,uint creation,uint flags,IntPtr template);
 [DllImport("kernel32.dll",SetLastError=true)]
 public static extern bool GetFileInformationByHandle(SafeFileHandle h,[Out] byte[] info);
}
'@
$held=[Collections.Generic.List[IDisposable]]::new()
try {
function Lock-Parents([string]$Path){
  $cursor=[IO.Path]::GetFullPath($Path)
  while($cursor){
    $item=Get-Item -LiteralPath $cursor -Force
    if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'ERR_ANCESTOR_REPARSE'}
    $h=[HgkOwnerHandles]::CreateFile($cursor,[uint32]2147483648,3,[IntPtr]::Zero,3,0x02200000,[IntPtr]::Zero)
    if($h.IsInvalid){$h.Dispose();throw 'ERR_OWNER_DIRECTORY_HANDLE'}
    $held.Add($h)
    $parent=Split-Path -Parent $cursor
    if($parent -eq $cursor){break};$cursor=$parent
  }
}
function Assert-Protected([string]$Path){
  $cursor=[IO.Path]::GetFullPath($Path)
  while($cursor){
    $item=Get-Item -LiteralPath $cursor -Force
    if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'ERR_PROTECTED_REPARSE'}
    $acl=Get-Acl -LiteralPath $cursor
    $owner=([Security.Principal.NTAccount]$acl.Owner).Translate([Security.Principal.SecurityIdentifier]).Value
    if($owner -notin @('S-1-5-18','S-1-5-32-544')){throw 'ERR_PROTECTED_OWNER'}
    $mask=if($cursor -eq $programData){0x000D0040}else{0x000D0156}
    foreach($r in $acl.Access){
      $who=$r.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
      if($r.AccessControlType -eq 'Allow' -and ([int]$r.FileSystemRights -band $mask) -ne 0 -and $who -notin @('S-1-5-18','S-1-5-32-544')){throw 'ERR_UNPROTECTED_WRITE_ACE'}
    }
    if($cursor -eq $programData){break};$cursor=Split-Path -Parent $cursor
  }
}
function Read-Pinned([string]$Path,[string]$Expected,[bool]$Hold=$false){
  if(-not [IO.Path]::IsPathRooted($Path)){throw 'ERR_PINNED_PATH_ABSOLUTE'}
  Lock-Parents (Split-Path -Parent $Path)
  $item=Get-Item -LiteralPath $Path -Force
  if($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'ERR_PINNED_REPARSE_OR_DIRECTORY'}
  $stream=[IO.File]::Open($Path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
  try{
    # Compare identity from the opened handle, not a second path lookup.
    $info=New-Object byte[] 52
    if(-not [HgkOwnerHandles]::GetFileInformationByHandle($stream.SafeFileHandle,$info)){throw 'ERR_PINNED_HANDLE'}
    if(([BitConverter]::ToUInt32($info,0) -band 0x410) -ne 0){throw 'ERR_PINNED_REPARSE_OR_DIRECTORY'}
    $m=[IO.MemoryStream]::new();try{$stream.CopyTo($m);$bytes=$m.ToArray()}finally{$m.Dispose()}
    if($Hold){$held.Add($stream);$stream=$null}
  }finally{if($stream){$stream.Dispose()}}
  $hash=[Security.Cryptography.SHA256]::Create()
  try{$actual=([BitConverter]::ToString($hash.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()}finally{$hash.Dispose()}
  if($Expected -and $actual -ne $Expected){throw 'ERR_PINNED_BYTES_SHA'}
  return ,$bytes
}
function Bytes-Hash([byte[]]$Bytes){
  $hash=[Security.Cryptography.SHA256]::Create()
  try{return ([BitConverter]::ToString($hash.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant()}finally{$hash.Dispose()}
}
function Write-NewPinned([string]$Path,[byte[]]$Bytes){
  if(-not [IO.Path]::IsPathRooted($Path)){throw 'ERR_OUTPUT_PATH_ABSOLUTE'}
  Lock-Parents (Split-Path -Parent $Path)
  # CreateNew rejects pre-existing files, links and crash residue. Never truncate.
  $stream=[IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
  try{
    $stream.Write($Bytes,0,$Bytes.Length);$stream.Flush($true);$stream.Position=0
    $m=[IO.MemoryStream]::new();try{$stream.CopyTo($m);$readback=$m.ToArray()}finally{$m.Dispose()}
    if((Bytes-Hash $readback) -ne (Bytes-Hash $Bytes)){throw 'ERR_ATOMIC_READBACK'}
  }finally{$stream.Dispose()}
}
function Set-ProtectedAcl([string]$Path,[bool]$Directory){
  if($Directory){$acl=[Security.AccessControl.DirectorySecurity]::new()}else{$acl=[Security.AccessControl.FileSecurity]::new()}
  $admins=[Security.Principal.SecurityIdentifier]::new('S-1-5-32-544')
  $system=[Security.Principal.SecurityIdentifier]::new('S-1-5-18')
  $users=[Security.Principal.SecurityIdentifier]::new('S-1-5-32-545')
  $acl.SetOwner($admins);$acl.SetAccessRuleProtection($true,$false)
  foreach($who in @($admins,$system)){$acl.AddAccessRule([Security.AccessControl.FileSystemAccessRule]::new($who,'FullControl','Allow'))}
  $acl.AddAccessRule([Security.AccessControl.FileSystemAccessRule]::new($users,'ReadAndExecute','Allow'))
  Set-Acl -LiteralPath $Path -AclObject $acl
}
function Read-Plan {
  if(-not $PlanPath -or $ExpectedPlanSha256 -notmatch '^[0-9a-f]{64}$'){throw 'ERR_EXACT_PLAN_PIN_REQUIRED'}
  $plan=[Text.Encoding]::UTF8.GetString((Read-Pinned $PlanPath $ExpectedPlanSha256))|ConvertFrom-Json
  if($plan.schema -ne 'HGK-OWNER-ENABLE-PLAN/1'){throw 'ERR_PLAN_SCHEMA'}
  if($plan.owner_os_sid -ne $sid -or $plan.owner_os_sid -eq $plan.maker_os_sid -or $plan.checker_os_sid -in @($plan.owner_os_sid,$plan.maker_os_sid)){throw 'ERR_REAL_PRINCIPAL_SEPARATION'}
  if(-not $plan.checker_os_sid -or -not $plan.maker_os_sid){throw 'ERR_PRINCIPAL_BINDING'}
  foreach($identitySid in @($plan.owner_os_sid,$plan.checker_os_sid,$plan.maker_os_sid)){
    $osIdentity=[Security.Principal.SecurityIdentifier]::new($identitySid)
    $null=$osIdentity.Translate([Security.Principal.NTAccount])
  }
  if(-not $plan.approval_source -or $plan.policy_sha256 -notmatch '^[0-9a-f]{64}$' -or $plan.source_manifest_sha256 -notmatch '^[0-9a-f]{64}$'){throw 'ERR_OWNER_SOURCE_BINDING'}
  if($plan.policy_epoch -isnot [long] -and $plan.policy_epoch -isnot [int]){throw 'ERR_POLICY_EPOCH_INTEGER'}
  if($plan.policy_epoch -lt 1 -or $plan.head -notmatch '^[0-9a-f]{40}$' -or $plan.scope.head -ne $plan.head -or -not $plan.scope.root_identity -or -not [IO.Path]::IsPathRooted($plan.root) -or -not [IO.Path]::IsPathRooted($plan.scope.database_path)){throw 'ERR_EXACT_OWNER_SCOPE_REQUIRED'}
  foreach($requestHash in $plan.scope.request_sha256){if($requestHash -notmatch '^[0-9a-f]{64}$'){throw 'ERR_REQUEST_HASH'}}
  return $plan
}
if($Mode -eq 'SelfTest'){
  if(-not $TestRoot -or -not [IO.Path]::IsPathRooted($TestRoot) -or (Test-Path -LiteralPath $TestRoot)){throw 'ERR_SELFTEST_NEW_ABSOLUTE_ROOT_REQUIRED'}
  $parent=Split-Path -Parent $TestRoot
  Lock-Parents $parent
  New-Item -ItemType Directory -Path $TestRoot -ErrorAction Stop|Out-Null
  $a=Join-Path $TestRoot 'bytes.bin'
  $bytes=[byte[]]@(0,13,10,255,65)
  Write-NewPinned $a $bytes
  $read=Read-Pinned $a (Bytes-Hash $bytes)
  if((Bytes-Hash $read) -ne (Bytes-Hash $bytes)){throw 'ERR_SELFTEST_EXACT_BYTES'}
  $refused=$false;try{$null=Read-Pinned $a ('0'*64)}catch{if($_ -notmatch 'ERR_PINNED_BYTES_SHA'){throw};$refused=$true}
  if(-not $refused){throw 'ERR_SELFTEST_HASH_REFUSAL'}
  $refused=$false;try{Write-NewPinned $a ([byte[]]@(88))}catch{$refused=$true}
  if(-not $refused -or (Bytes-Hash (Read-Pinned $a '')) -ne (Bytes-Hash $bytes)){throw 'ERR_SELFTEST_CREATE_NEW'}
  $staged=Join-Path $TestRoot 'staged.bin';$backup=Join-Path $TestRoot 'before.bin'
  Write-NewPinned $staged ([byte[]]@(66))
  # A crash before Replace leaves the original intact and readable.
  if((Bytes-Hash (Read-Pinned $a '')) -ne (Bytes-Hash $bytes)){throw 'ERR_SELFTEST_CRASH_BEFORE_REPLACE'}
  [IO.File]::Replace($staged,$a,$backup)
  if((Bytes-Hash (Read-Pinned $a '')) -ne (Bytes-Hash ([byte[]]@(66))) -or (Bytes-Hash (Read-Pinned $backup '')) -ne (Bytes-Hash $bytes)){throw 'ERR_SELFTEST_REPLACE_READBACK'}
  [pscustomobject]@{schema='HGK-OWNER-TOOL-MAKER-SELFTEST/1';tests=5;passed=5;root=$TestRoot;private_key_accessed=$false;native_activation=$false;independent_acceptance=$false}|ConvertTo-Json
  exit 0
}
if($Mode -eq 'Enable'){
  $plan=Read-Plan
  if(-not $plan.approved_files -or $plan.max_ttl_seconds -le 0 -or $plan.max_ttl_seconds -gt 3600 -or -not $plan.scope.request_sha256 -or -not $plan.scope.database_path){throw 'ERR_EXACT_OWNER_SCOPE_REQUIRED'}
  Lock-Parents $plan.root
  # Exact artifact pins are mandatory. This tool provisions public trust only;
  # it never applies product patches, migrates DB, grants permits or creates WOs.
  foreach($file in $plan.approved_files){
    $path=Join-Path $plan.root $file.path
    $resolved=[IO.Path]::GetFullPath($path)
    if(-not $resolved.StartsWith([IO.Path]::GetFullPath($plan.root).TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'ERR_WRITESET_ESCAPE'}
    Lock-Parents (Split-Path -Parent $resolved)
    $item=Get-Item -LiteralPath $resolved -Force
    if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'ERR_REPARSE'}
    if($file.sha256 -notmatch '^[0-9a-f]{64}$'){throw 'ERR_FILE_SHA_REQUIRED'}
    $null=Read-Pinned $resolved $file.sha256 $true
  }
  $head=(& git -C $plan.root rev-parse HEAD).Trim();if($LASTEXITCODE -ne 0 -or $head -ne $plan.head){throw 'ERR_HEAD'}
  if(Test-Path -LiteralPath $registryPath){throw 'ERR_EXISTING_REGISTRY_USE_REVIEWED_REVISION_NOT_OVERWRITE'}
  $keys=@{}
  foreach($entry in $plan.certificates){
    $cert=Get-Item -LiteralPath ('Cert:/LocalMachine/My/'+$entry.thumbprint)
    if(-not $cert.HasPrivateKey -or $cert.NotBefore.ToUniversalTime() -gt [DateTime]::UtcNow -or $cert.NotAfter.ToUniversalTime() -le [DateTime]::UtcNow){throw 'ERR_EXISTING_CERT_REQUIRED'}
    $key=[Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
    try{
      if($key -isnot [Security.Cryptography.RSACng] -or $key.KeySize -lt 3072 -or $key.Key.ExportPolicy -ne [Security.Cryptography.CngExportPolicies]::None){throw 'ERR_NONEXPORTABLE_MACHINE_CNG_RSA_REQUIRED'}
      if(-not $key.Key.IsMachineKey){throw 'ERR_MACHINE_KEY_REQUIRED'}
      $keyPath=Join-Path $programData ('Microsoft/Crypto/Keys/'+$key.Key.UniqueName)
      $acl=Get-Acl -LiteralPath $keyPath
      $keyOwner=([Security.Principal.NTAccount]$acl.Owner).Translate([Security.Principal.SecurityIdentifier]).Value
      if($keyOwner -notin @('S-1-5-18','S-1-5-32-544',$sid)){throw 'ERR_PROTECTED_KEY_OWNER'}
      foreach($r in $acl.Access){
        $who=$r.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
        if($r.AccessControlType -eq 'Allow' -and $who -notin @('S-1-5-18','S-1-5-32-544',$sid)){throw 'ERR_PROTECTED_KEY_ACL'}
      }
    }finally{if($key){$key.Dispose()}}
    $keys[$entry.thumbprint]=@{algorithm='RS256';purposes=$entry.purposes;revoked=$false;public_certificate_der_b64=[Convert]::ToBase64String($cert.RawData)}
  }
  if($keys.Count -eq 0 -or $plan.task_kinds.psobject.Properties.Count -eq 0){throw 'ERR_REGISTERED_KEYS_AND_KINDS_REQUIRED'}
  # Enabling is an explicit action by this actual OS Owner on a reviewed plan.
  $data=@{schema='HGK-NATIVE-REGISTRY/1';canonical_profile='HGK-B1-ASCII-C14N/1';status='ACTIVE';owner_os_sid=$sid;checker_os_sid=$plan.checker_os_sid;maker_os_sid=$plan.maker_os_sid;mission_id=$plan.mission_id;source_manifest_sha256=$plan.source_manifest_sha256;policy_sha256=$plan.policy_sha256;policy_epoch=$plan.policy_epoch;max_ttl_seconds=$plan.max_ttl_seconds;scope=$plan.scope;root=$plan.root;approved_files=$plan.approved_files;keys=$keys;task_kinds=$plan.task_kinds;revoked_nonces=@();owner_enable_plan_sha256=$ExpectedPlanSha256;approval_source=$plan.approval_source}
  $hgkParent=Split-Path -Parent $registryDir
  Lock-Parents $programData
  if(-not (Test-Path -LiteralPath $hgkParent)){New-Item -ItemType Directory -Path $hgkParent|Out-Null;Set-ProtectedAcl $hgkParent $true}
  Assert-Protected $hgkParent;Lock-Parents $hgkParent
  if(Test-Path -LiteralPath $registryDir){throw 'ERR_EXISTING_TRUST_DIRECTORY_REVIEW_REQUIRED'}
  New-Item -ItemType Directory -Path $registryDir -ErrorAction Stop|Out-Null
  $dir=Get-Item -LiteralPath $registryDir -Force;if($dir.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'ERR_TRUST_DIR_REPARSE'}
  Set-ProtectedAcl $registryDir $true
  Assert-Protected $registryDir;Lock-Parents $registryDir
  # CreateNew prevents replacement/re-enrollment of an existing trust registry.
  $bytes=[Text.UTF8Encoding]::new($false).GetBytes(($data|ConvertTo-Json -Depth 24))
  Write-NewPinned $registryPath $bytes
  Set-ProtectedAcl $registryPath $false
  [pscustomobject]@{state='PUBLIC_TRUST_PROVISIONED_REQUIRES_VERIFIER_READBACK';registry_sha256=(Get-FileHash -LiteralPath $registryPath).Hash.ToLowerInvariant();owner_os_sid=$sid;private_key_exported=$false;permit_issued=$false;product_patch_applied=$false}|ConvertTo-Json
  exit 0
}
Assert-Protected $registryPath;Lock-Parents $registryDir
if($ExpectedRegistrySha256 -notmatch '^[0-9a-f]{64}$'){throw 'ERR_EXACT_REGISTRY_PIN_REQUIRED'}
# One stable file lock serializes all supported maintenance writers. It is
# never deleted/recreated; readers keep the registry pinned until their commit.
$maintenance=[IO.File]::Open((Join-Path $registryDir 'maintenance.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
$held.Add($maintenance)
$registryBytes=Read-Pinned $registryPath $ExpectedRegistrySha256
$data=[Text.Encoding]::UTF8.GetString($registryBytes)|ConvertFrom-Json
if($data.owner_os_sid -ne $sid -or $data.maker_os_sid -eq $sid){throw 'ERR_REGISTERED_OWNER_OS_IDENTITY'}
if($Mode -eq 'Revoke'){
  $data.status='REVOKED'
  $staged=Join-Path $registryDir ([Guid]::NewGuid().ToString()+'.revoke')
  $bytes=[Text.UTF8Encoding]::new($false).GetBytes(($data|ConvertTo-Json -Depth 24))
  Write-NewPinned $staged $bytes
  Set-ProtectedAcl $staged $false
  $null=Read-Pinned $registryPath $ExpectedRegistrySha256
  $backup=$registryPath+'.before-revoke-'+[Guid]::NewGuid().ToString()
  [IO.File]::Replace($staged,$registryPath,$backup)
  $null=Read-Pinned $registryPath (Bytes-Hash $bytes)
  [pscustomobject]@{state='REVOKED';sha256=(Get-FileHash -LiteralPath $registryPath).Hash.ToLowerInvariant()}|ConvertTo-Json
  exit 0
}
if($Mode -eq 'Sign'){
  if($data.status -ne 'ACTIVE'){throw 'ERR_REGISTRY_INACTIVE'}
  if(-not $PayloadPath -or $ExpectedPayloadSha256 -notmatch '^[0-9a-f]{64}$' -or -not $SignatureOutput){throw 'ERR_EXACT_PAYLOAD_PIN_REQUIRED'}
  $output=[IO.Path]::GetFullPath($SignatureOutput)
  if((Split-Path -Parent $output) -ne $registryDir -or (Test-Path -LiteralPath $output)){throw 'ERR_SIGNATURE_OUTPUT_SCOPE_OR_EXISTS'}
  $payloadBytes=Read-Pinned $PayloadPath $ExpectedPayloadSha256
  $registered=$data.keys.psobject.Properties[$CertificateThumbprint]
  if(-not $registered -or $registered.Value.revoked){throw 'ERR_REGISTERED_KEY_REQUIRED'}
  $cert=Get-Item -LiteralPath ('Cert:/LocalMachine/My/'+$CertificateThumbprint)
  if($cert.NotBefore.ToUniversalTime() -gt [DateTime]::UtcNow -or $cert.NotAfter.ToUniversalTime() -le [DateTime]::UtcNow){throw 'ERR_CERT_EXPIRED_OR_FUTURE'}
  if([Convert]::ToBase64String($cert.RawData) -ne $registered.Value.public_certificate_der_b64){throw 'ERR_CERT_PIN'}
  $key=[Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
  try{
    if($key -isnot [Security.Cryptography.RSACng] -or $key.KeySize -lt 3072 -or -not $key.Key.IsMachineKey -or $key.Key.ExportPolicy -ne [Security.Cryptography.CngExportPolicies]::None){throw 'ERR_CNG_NONEXPORTABLE_REQUIRED'}
    $keyPath=Join-Path $programData ('Microsoft/Crypto/Keys/'+$key.Key.UniqueName)
    $keyAcl=Get-Acl -LiteralPath $keyPath
    $keyOwner=([Security.Principal.NTAccount]$keyAcl.Owner).Translate([Security.Principal.SecurityIdentifier]).Value
    if($keyOwner -notin @('S-1-5-18','S-1-5-32-544',$sid)){throw 'ERR_PROTECTED_KEY_OWNER'}
    foreach($rule in $keyAcl.Access){
      $who=$rule.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
      if($rule.AccessControlType -eq 'Allow' -and $who -notin @('S-1-5-18','S-1-5-32-544',$sid)){throw 'ERR_PROTECTED_KEY_ACL'}
    }
    # Sign exact pinned canonical bytes; the native verifier still enforces all
    # purpose/subject/epoch/TTL/nonce/registry semantics before canonical mutation.
    $signature=$key.SignData($payloadBytes,[Security.Cryptography.HashAlgorithmName]::SHA256,[Security.Cryptography.RSASignaturePadding]::Pkcs1)
    # Signatures are public, but elevated writes remain within this protected dir.
    $bytes=[Text.UTF8Encoding]::new($false).GetBytes([Convert]::ToBase64String($signature))
    $null=Read-Pinned $registryPath $ExpectedRegistrySha256
    Write-NewPinned $output $bytes
    Set-ProtectedAcl $output $false
  }finally{if($key){$key.Dispose()}}
  [pscustomobject]@{state='SIGNED_EXACT_BYTES_REQUIRES_NATIVE_VERIFICATION';signature_file_sha256=(Get-FileHash -LiteralPath $SignatureOutput).Hash.ToLowerInvariant();private_key_exported=$false}|ConvertTo-Json
}
} finally {
  for($i=$held.Count-1;$i -ge 0;$i--){$held[$i].Dispose()}
}
