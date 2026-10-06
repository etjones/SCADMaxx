# Convert the approved PNG artwork into platform icon containers; does not build or test SCADMaxx.
[CmdletBinding()]
param([string]$Magick='E:/Dropbox/bin/ImageMagick-7.1.2-23-portable-Q16-HDRI-x64/magick.exe')
$ErrorActionPreference='Stop'
$assets=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../assets/icons'))
$master=Join-Path $assets 'scadmaxx-master.png'
foreach($size in @(16,24,32,48,64,128,256,512,1024)){
  & $Magick $master -resize "${size}x${size}" "$assets/scadmaxx-$size.png"
  if($LASTEXITCODE -ne 0){throw "PNG conversion failed: $size"}
}
Copy-Item "$assets/scadmaxx-512.png" "$assets/scadmaxx.png"
& $Magick "$assets/scadmaxx-256.png" -define icon:auto-resize=256,128,64,48,32,24,16 "$assets/scadmaxx.ico"
if($LASTEXITCODE -ne 0){throw 'ICO conversion failed'}
# ICNS stores PNG representations with big-endian chunk lengths.
$chunks=@(@('icp4',16),@('icp5',32),@('icp6',64),@('ic07',128),@('ic08',256),@('ic09',512),@('ic10',1024))
$payload=[IO.MemoryStream]::new()
function Write-BigEndian($stream,[int]$value){
  $bytes=[BitConverter]::GetBytes($value)
  if([BitConverter]::IsLittleEndian){[Array]::Reverse($bytes)}
  $stream.Write($bytes,0,4)
}
foreach($chunk in $chunks){
  $bytes=[IO.File]::ReadAllBytes("$assets/scadmaxx-$($chunk[1]).png")
  $tag=[Text.Encoding]::ASCII.GetBytes($chunk[0]);$payload.Write($tag,0,4)
  Write-BigEndian $payload ($bytes.Length+8);$payload.Write($bytes,0,$bytes.Length)
}
$output=[IO.File]::Create("$assets/scadmaxx.icns")
try{$tag=[Text.Encoding]::ASCII.GetBytes('icns');$output.Write($tag,0,4);Write-BigEndian $output ($payload.Length+8);$payload.Position=0;$payload.CopyTo($output)}
finally{$output.Dispose();$payload.Dispose()}
