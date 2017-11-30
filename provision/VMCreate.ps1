Param(
    [string]$VM = "LinuxHadoop",
    [int]$PF = 2222, 
    [string]$MODE="create", 
    [boolean]$namenode = $false,
    [int]$storage = 32768  
)

$cwd = Get-Location | Select-Object -exp Path
Set-Variable -Name "VBPath" -Value "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
$NetAdapter = Get-WmiObject -Class Win32_NetworkAdapter -filter "AdapterType like 'Ethernet 802.3'" | Select-Object -exp Name -first 1
$NetAdapter = "82540EM"

if($namenode)
{
    $ram = 8192
}
else {
    $ram = 2048
}


Write-Host "VM: $VM"
Write-Host "SSH Port Forward: $PF"
Write-Host "Mode: $MODE"

if($MODE.equals("create"))
{
    Set-Variable -Name "VM" -Value $VM
    New-Item -ItemType "Directory" -Force -Path "C:\Users\$env:USERNAME\VirtualBox VMs\$VM"
    Set-Location -Path "C:\Users\$env:USERNAME\VirtualBox VMs\$VM"
    
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" createhd --filename "$VM.vdi" --size $storage

    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" createvm --name $VM --ostype "Linux_64" --register

    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storagectl $VM --name "SATA Controller" --add sata --controller IntelAHCI
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storageattach $VM --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$VM.vdi"

    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storagectl $VM --name "IDE Controller" --add ide
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storageattach $VM --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium C:\Users\$env:USERNAME\Downloads\CentOS-7-x86_64-Everything-1708.iso

    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --ioapic on
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --boot1 dvd --boot2 disk --boot3 none --boot4 none
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --memory $ram --vram 128
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --nic1 nat --nictype1 $NetAdapter
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --cableconnected1 on
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --natpf1 "guestssh,tcp,,$PF,,22"
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --nic2 hostonly --nictype2 $NetAdapter --hostonlyadapter2 "VirtualBox Host-Only Ethernet Adapter"
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --cableconnected2 on
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" sharedfolder add $VM --name vmshare --hostpath "C:\Users\ryanwhi\vmshare" --automount
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm $VM
}
elseif($MODE.equals("finalize")){
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm $VM poweroff
    Start-Sleep -s 10
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm $VM --boot1 disk --boot2 dvd --boot3 none --boot4 none
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" storageattach $VM --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium "additions"
    & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm $VM
}
else{
    Write-Host "Incorrect Mode"
}

Set-Location $cwd