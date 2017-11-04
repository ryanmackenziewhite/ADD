#! /bin/bash
#
# provision.sh
# Copyright (C) 2017 Ryan Mackenzie White <ryan.white@cern.ch>
#
# Distributed under terms of the  license.
# 
# Inspired from https://github.com/jream/provision-bash.git
# Each part can be moved to separate scripts, e.g. logger to logger.sh 

##################################################
# Environment variables
#source bin/variables.sh
export __DEBUG=false
export __FINALIZE=false
#export __LOGGER_FILEPATH="junk"
#export __LOGGER_FILENAME="junk.log"
export __SHARE_FILEPATH="/media/sf_vmshare/"
export __HOSTS_FILENAME="hosts.txt"
export __KEYS_FILENAME="keys.txt"
export __HADOOP_VERSION="hadoop-2.7.4"
export __HADOOP_PATH="/opt/hadoop"
export __MEDIA="dvd"
export __OS="Ubuntu"
export __PKGMGR="apt-get"
export __SETKEYS=false
##################################################

##################################################
# Help
# For double brackets explanation, see ch 7.1 in Advanced Bash-Scripting
if [[ $1 == 'help' || $1 == '-h' || $1 == '--help' ]] 
then
    echo "Usage:"
    echo "./provision.sh <nodename> <ipaddress>"
    echo "Options"
    echo "--debug Prints all commands, does not execute"
    exit 1
fi

# Version
if [[ $1 == 'V' || $1 == 'v' || $1 == '--version' ]] 
then
    echo "Version 0.0"
    exit 1
fi
##################################################

# Debug
if [[ $1 == '--debug' ]] 
then
   __DEBUG=true
fi
##################################################

if [[ $1 == '-k' || $1 == '--keys' ]]
then
    __SETKEYS=true
fi

##################################################
# Colors
# colors for interactive
red='\e[0;31m'
green='\e[0;32m'
yellow='\e[1;33m'
cyan='\e[0;36m'
nc='\e[0m'

reset=${nc}
debug="${yellow} DEBUG: ${reset}" 
warn="${yellow} WARNING: ${reset}" 
success="${green} SUCCESS: ${reset}"
error="${red} ERROR: ${reset}"
question="${cyan} Question: ${reset}"
info="${cyan} INFO: ${reset}"
##################################################


##################################################
# Utilities
# Logger
# source bin/logger.sh
# Path and name for log
if [[ ! $__LOGGER_FILEPATH ]] 
then
    echo 'Set Logger Path'
	__LOGGER_FILEPATH="/tmp"
fi
if [[ ! $__LOGGER_FILENAME ]]; then
    __LOGGER_FILENAME="provision.log"
fi

# Append text to log file
# Echo content to stdout
# $ param   str Content 
logger() {
    # Strip colors from log
    echo -e "$(date) $1" | perl -pe 's/\e\[?.*?[\@-~]//g' >> $__LOGGER_FILEPATH/$__LOGGER_FILENAME
    echo -e "$(date) $1"
}

logger_clear() {
    echo -e "${info} Clear the log"
    echo "" > $__LOGGER_FILEPATH/$__LOGGER_FILENAME
}

logger_clear
if [[ $__DEBUG == true ]]; then
    logger "${DEBUG} DEBUG: ${__DEBUG}"
    logger "Print all commands, do not execute"
fi

#################################################

##################################################
# Configuration
# Users
# hadoop must be first, creates group for remaining hadoop 
users=(
    "hadoop"   
    "hadoopuser"
    "hdfs"
    "yarn"
    "mapred"
)

# Packages
declare -A packages
packages=(
    ["ssh"]=install_ssh
    ["vim"]=install_vim
)

declare -A languages
languages=(
    ["jdk"]=install_jdk
    ["python"]=install_python
)

# network
# Debug
if [[ $1 == '--debug' || $1 == '-k' || $1 == '--keys' ]] 
then
    if [[ "$#" -ne 3 ]]
    then
        logger "${error} Provide Nodename IP address"
        exit 1
    fi
    nodename=$2
    ipaddr=$3

else
    if [[ "$#" -ne 2 ]]
    then
        logger "${error} Provide Nodename IP address"
        exit 1
    fi
    nodename=$1
    ipaddr=$2
fi
    
networkcfg=(
    ${nodename}
    ${ipaddr}
    "192.168.56.1"
    "255.255.255.0"
)

if [[ -f "/etc/os-release" ]]
then
    . /etc/os-release
    __OS=$NAME
    if [[ ${__OS} == "CentOS Linux" ]]
    then
        __PKGMGR="yum"
    fi
fi

logger "${info} OS Version: $__OS"
logger "${info} Install via ${__PKGMGR}"


logger "${info} Configure Node: ${networkcfg[0]} ${networkcfg[1]} ${networkcfg[2]} ${networkcfg[3]}"

logger "${info} Packages to Install:"
for key in "${!packages[@]}"
do
    logger "${info} Install ${key}"
done

logger "${info} Languages to Install:"
for key in "${!languages[@]}"
do
    logger "${info} Install ${key}"
done

logger "${info} Users to configure:"
for user in ${users}
do
    logger "${info} ${user}"
done
################################################

# Pass sudo command
# $ param str Command
executor() {
    COMMAND="$@"
    if [[ $__DEBUG == true ]]; then
        logger "${debug} $@"
    else
        echo -e "Executing command"
        logger $@
        ${COMMAND[@]} 
    fi
}

################################################
# Installers
install_ssh() {
    executor "sudo ${__PKGMGR} install ssh"
}

install_vim() {
    executor "sudo ${__PKGMGR} install vim"
}

install_jdk() {
    if [[ ${__OS} == "CentOS Linux" ]]
    then
        executor "sudo ${__PKGMGR} install --disablerepo=extras,updates java-sdk"
    else
        executor "sudo ${__PKGMGR} install default-jdk"
    fi
}

install_python() {
    executor "sudo ${__PKGMGR} install python3"
}

##################################################
# Start Provision Process
logger "${info} Begin provisioning"

##################################################
if [[ ! -d ${__SHARE_FILEPATH} ]]
then 
    if [[ ! -d "/media/cdrom" ]]
    then
            
            executor 'sudo mkdir /media/cdrom' 
            executor 'sudo mount /dev/cdrom /media/cdrom'
    fi
    if [[ -f "/media/cdrom/VBoxLinuxAdditions.run" ]]
    then
            executor 'sudo /media/cdrom/VBoxLinuxAdditions.run'
    else
            logger "${error} VBoxLinuxAdditions.run not found!"
    fi
else
    # Use the vmshare to indicate VM has restarted
    # Better way is to store script state
    # run from init.d
    # Complete installation with users
    __FINALIZE=true
fi
##################################################

##################################################

if [[ $__SETKEYS == true ]]
then
    logger "${info} ============================================ " 
    logger "${info} set hosts"
    sudo cat $__SHARE_FILEPATH/$__HOSTS_FILENAME | sudo tee -a /etc/hosts
    
    logger "${info} copy keys to slaves"
    for user in ${users[@]}
    do
         sudo -u ${user} cat $__SHARE_FILEPATH/$__KEYS_FILENAME | tee -a /home/${user}/.ssh/authorized_keys
    done
    exit 0
fi 
    

###################################################
#################################################
# User Accounts
#################################################
# Create the hadoopgroup

if [[ ${__FINALIZE} == true ]]
then
    ###################################################
    # Repository from local share drive
    tmppath=$(echo $__SHARE_FILEPATH | perl -pe 's/\//\\\//g')
    sudo perl -i -pe "s/\#baseurl=http:\/\/mirror.centos.org\/centos\/\$releasever/baseurl=file:$tmppath\/CentOS\//g" /etc/yum.repos.d/CentOS-Base.repo 
    # Packages 
    logger "${info} Install Packages"
    for i in "${packages[@]}"
    do
        logger "${info} Installing ${i}"
        ${i}
    done

    ##################################################

    #################################################
    # Languages
    logger "${info} Install Languages"
    for i in "${languages[@]}"
    do
        logger "${info} Installing ${i}"
        ${i}
    done

    #################################################
    # SSH KEYS
    echo -e "${networkcfg[1]}  ${networkcfg[0]}" | sudo tee -a $__SHARE_FILEPATH/$__HOSTS_FILENAME  
    echo -e "${networkcfg[0]}" | sudo tee -a $__SHARE_FILEPATH/slaves   

    for user in ${users[@]}
    do
        logger "${info} Create keys for user ${user}" 
            if [[ $__DEBUG == false ]]
            then
            sudo -u ${user} ssh-keygen -t rsa -P '' -f /home/${user}/.ssh/id_rsa
            sudo -u ${user} cat /home/${user}/.ssh/id_rsa.pub | sudo -u ${user} tee -a /home/${user}/.ssh/authorized_keys
            sudo -u ${user} chmod 0600 /home/${user}/.ssh/authorized_keys
            sudo -u ${user} cat /home/${user}/.ssh/authorized_keys | tee -a $__SHARE_FILEPATH/$__KEYS_FILENAME
        fi
    done
    #################################################

    #################################################
    # Hadoop 
    if [[ ! -d $__HADOOP_PATH ]]
    then
            executor "sudo mkdir $__HADOOP_PATH"
    fi	

    executor "sudo tar -xzf $__SHARE_FILEPATH/$__HADOOP_VERSION.tar.gz --directory $__HADOOP_PATH"
    executor "sudo chown -R hadoop:hadoop $__HADOOP_PATH/$__HADOOP_VERSION"
    ##################################################
    # Create /etc/profile.d/hadoop.sh
    sudo touch /etc/profile.d/hadoop_setup.sh
    sudo echo -e "HADOOP_PREFIX=$__HADOOP_PATH/$__HADOOP_VERSION" | sudo tee -a /etc/profile.d/hadoop_setup.sh
    sudo echo -e "export HADOOP_PREFIX" | sudo tee -a /etc/profile.d/hadoop_setup.sh
    sudo echo -e "JAVA_HOME=/usr" | sudo tee -a /etc/profile.d/hadoop_setup.sh
    sudo echo -e "export JAVA_HOME" | sudo tee -a /etc/profile.d/hadoop_setup.sh

    echo -e "export PATH=$PATH:$__HADOOP_PATH/$__HADOOP_VERSION/$__HADOOP_PATH/bin:$__HADOOP_PATH/$__HADOOP_VERSION/sbin" | sudo tee -a /etc/environment
    
    # Create the storage directories
    # Do we need to create 1...n for datanode and add these directories?
    if [[ ${nodename} == "master" ]]
    then
        sudo mkdir -p /data/dfs/nn
        sudo chown -R hdfs:hdfs /data/dfs/nn
    else
        sudo mkdir -p /data/dfs/dn
        sudo chown -R hdfs:hdfs /data/dfs/dn
    fi

    # Create the storage directories for hdfs, logs, etc...
    logger "${info} Completed Provisioning Process"

    exit 0
fi


#################################################
# Networking
THISHOST=$(hostname)
logger "Hostname is: ${THISHOST}"
echo -ne "\n${question} Set the node name: "
#read nodename

logger "Nodename is: ${nodename}"

echo -ne "\n${question} Set the IP address for ${nodename}: "
#read ipaddr
logger "IP address for ${nodename} is ${ipaddr}"

logger "${info} Update hosts information for ${nodename} on host ${THISHOST}"
logger "${info} ${ipaddr}  ${nodename}  ${THISHOST}" 

if [[ $__DEBUG == false ]]
then
    if [[ ${__OS} == "CentOS Linux" ]]
    then
        logger "${info} CentOS Linux network"
        sudo perl -i -pe "s/BOOTPROTO=dhcp/BOOTPROTO=static/g" /etc/sysconfig/network-scripts/ifcfg-enp0s8
        sudo perl -i -pe "s/ONBOOT=no/ONBOOT=yes/g" /etc/sysconfig/network-scripts/ifcfg-enp0s8
        echo -e "IPADDR=${ipaddr}" | sudo tee -a "/etc/sysconfig/network-scripts/ifcfg-enp0s8"
        echo -e "NETMASK=${networkcfg[3]}" | sudo tee -a "/etc/sysconfig/network-scripts/ifcfg-enp0s8"
        echo -e "NETWORKING=yes" | sudo tee -a "/etc/sysconfig/network"
        echo -e "HOSTNAME=${THISHOST}" | sudo tee -a "/etc/sysconfig/network"
        echo -e "GATEWAY=${networkcfg[2]}" | sudo tee -a "/etc/sysconfig/network"
	
	echo -e "${ipaddr}  ${nodename}  ${THISHOST}" | sudo tee -a "/etc/hosts"
	executor "sudo /etc/init.d/network restart"
    elif [[ ${__OS} == "Ubuntu" ]]
    then
        echo -e " " | sudo tee -a "/etc/network/interfaces"
        echo -e "auto enp0s8" | sudo tee -a "/etc/network/interfaces"
        echo -e "iface enp0s8 inet static" | sudo tee -a "/etc/network/interfaces"
        echo -e "address ${ipaddr}" | sudo tee -a "/etc/network/interfaces"
        echo -e "network ${networkcfg[2]}" | sudo tee -a "/etc/network/interfaces"  
        echo -e "netmask ${networkcfg[3]}" | sudo tee -a "/etc/network/interfaces"
	echo -e "${ipaddr}  ${nodename}  ${THISHOST}" | sudo tee -a "/etc/hosts"
	executor "sudo /etc/init.d/networking restart"
    else 
        logger "${error} Cannot configure network"
    fi
else
    logger "${DEBUG} Configure the node: ${networkcfg[0]} ${networkcfg[1]}"
fi

logger "${info} Setup users"

for user in ${users[@]}
do
    logger "${info} Create user account: ${user}"
    exists=$(grep -c "^${user}:" /etc/passwd)
    if [[ ${exists} == 0 ]]
    then
        logger "${info} Create ${user}"
        if [[ ${user} == "hadoop" ]]
        then
            executor "sudo useradd -m -G vboxsf ${user}"
        else
	    executor "sudo useradd -m -G hadoop,vboxsf ${user}"
        fi
    else
        logger "${info} Modify groups for ${user}"
        executor "sudo usermod -aG vboxsf ${user}"
        executor "sudo usermod -aG hadoop ${user}"
    fi
done

################################################
logger "${info} Completed initial provisioning, restarting"
executor "sudo reboot"
exit 0
