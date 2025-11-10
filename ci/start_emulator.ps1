param([string]$AvdName = "Medium_Phone_API_36.1")
Write-Host "Starting AVD: $AvdName"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
& adb kill-server | Out-Null
Start-Process -FilePath "emulator" -ArgumentList @("-avd",$AvdName,"-no-snapshot","-no-boot-anim","-gpu","auto","-netfast") -WindowStyle Hidden
& adb wait-for-device
# wait for boot complete
$retries=60
for($i=0;$i -lt $retries;$i++){
  $boot=(& adb shell getprop sys.boot_completed).Trim()
  if($boot -eq "1"){break}
  Start-Sleep -Seconds 3
}
# nudge network + unlock
& adb shell svc wifi disable
& adb shell svc data disable
& adb shell svc wifi enable
& adb shell svc data enable
& adb shell input keyevent 82
Write-Host "Emulator is ready."
