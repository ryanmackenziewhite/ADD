Provisioning scripts for hadoop VM
Requires VirtualBox
Assumes CentOS repo is cloned to a local shared drive
Instructions here setup a pseudo cluster for sandboxing. 
In principle, this will work for provisioning a physical cluster as well.

For windows, use VMCreate.ps1
VMCreate.ps1 <VMName> <Port 22 Port Forward> <mode> <namenode> <storage>
`VMCreate.ps1 LinuxHadoop 2222 create 0 4096`

Run the linux installer, ensure primary network device is enabled.
Create user hadoopuser
After install, finalize VM

`VMCreate.ps1 LinuxHadoop 2222 finalize 0 4096`

`pscp.exe -P 2222 provision.tar.gz hadoopuser@localhost:/home/hadoopuser
ssh -p 2222 hadoopuser@localhost
tar -xzf provision.tar.gz
cd provision
./provision master 192.168.56.10`

after reboot continue

`./provision master 192.168.56.10`

hadoop is now available, with the various accounts.
Run the configuration file generator for pseudo mode.
Note that currently we disable dfs permissions. 
Ideally, we run with permissions. The issue is the history,
mapred user tries to write to / to create /user/history.

`python python/configFileGenerator.py -i config/configPseudo.ini
cp *xml /media/sf_vmshare/config`

`sudo -u hadoop cp /media/sf_vmshare/config/*xml /opt/hadoop/hadoop-2.7.4/etc/hadoop`

`sudo -u hdfs bash -i`

`hdfs namenode -format`

`start-dfs.sh`
`hadoop fs -mkdir /user/hadoopuser`
`hadoop fs -chown hadoopuser:hadoopuser /user/hadoopuser`
`hadoop fs -mkdir /user/history`
`hadoop fs -chown mapred:hadoop /user/history`
`ctrl-D`
`sudo -u yarn bash -i`
`start-yarn.sh`
`ctrl-D`
`sudo -u mapred bash -i`
`mr-jobhistory-daemon.sh start historyserver`

