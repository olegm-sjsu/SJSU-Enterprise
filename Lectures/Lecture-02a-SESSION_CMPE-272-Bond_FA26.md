# Lecture-02a-SESSION CMPE-272-Bond FA26

Source: `Lecture-02a-SESSION_CMPE-272-Bond_FA26.pdf` (37 slides)

## Slide 1: CMPE 272

Enterprise Software Platforms

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: SAN · JOSE · STATE · UNIVERSITY · SJSU  

---

## Slide 2: IT News

- 

Microsoft's Charles Lamanna predicts traditional business apps will become obsolete by 2030, replaced by AI agents that dynamically adapt to user needs.
- “business agents”: AI-powered entities featuring generative AI (GenAI) user interfaces that dynamically adapt to user needs, goal-oriented agents that find optimal paths rather than following predetermined workflows and vector databases designed for AI-native operations.

- 

Linux Turns 34 – This week, 34 years ago, an unknown computer science student from Finland announced that a new free operating system project was "starting to get ready." Linus Benedict
Torvalds elaborated by explaining that the OS was
"just a hobby, [it] won't be big and professional like
GNU." Of course, this was the first public outing for the colossal collaborative project that is now known as Linux.

---

## Slide 3: - 

- 
- 
- 
- 
- 

Operating System History
Compute Platforms
Modern Enterprise Operating Systems
Identity Management
Filesystems & Storage Networking
Enterprise Management (Puppet/Chef/Ansible/Nagios)

UNIT 1 · ENTERPRISE INFRASTRUCTURE

---

## Slide 4: Types of OS’s

- Single- and multi-tasking
- Single- and multi-user
- Distributed (clustered/networked/infiniband)
- Templated (VM/container template/image)
- Lightweight (minimal e.g. CoreOS)
- Embedded (IoT) / Real-time (event driven)

---

## Slide 5: Linux

- Linux began in 1991 as a personal project by Finnish student Linus Torvalds: to create a new free operating system kernel. The resulting Linux kernel has been marked by constant growth throughout its history.
- How Linux was born, as told by Linus Torvalds himself
- Slackware, Redhat/CentOS, Debian/Ubuntu, SUSE
- Tanenbaum–Torvalds debate

"LINUX is obsolete"
…writing a monolithic kernel in 1991 is
"a giant step back into the 1970s".

> **Text from slide image (OCR, may contain errors):**
>
> Application  
> user  
> mode  
> VFS  
> IPC, Fle System  
> Application UNIX Device File  
> IPC Server Driver Server  
> Scheduler, Virtual Memory er  
> Device Drivers, Dispatcher, Basic IPC, Virtual Memory, Scheduling  
> Hardware Hardware  

> **Text from slide image (OCR, may contain errors):**
>
> Monolithic Kernel Microkernel  
> based Operating System based Operating System  
> System Call  
> user  
> mode  
> mode  

---

## Slide 6: The end of CentOS 

- CentOS Linux 8 will end in 2021 and shifts focus to CentOS Stream
- While RHEL costs money, CentOS offered as a free communitysupported enterprise Linux distro
- Developers and companies who are good at Linux and don’t want to pay RHEL support fees always selected CentOS to save money and get enterprise-class software
- The free ride is over
- Red Hat announced that CentOS Linux 8, as a rebuild of RHEL 8, will end at 2021
- CentOS Stream continues after that date, serving as the upstream (development) branch of Red Hat Enterprise Linux

---

## Slide 7: systemd is a software suite that provides an array of system components for Linux operating systems, unifying service configuration and behavior across Linux distributions systemd's primary component is a "system and service manager"—an init system used to bootstrap user space and manage user processes

systemd also provides replacements for various daemons and utilities, including device management, login management, network connection management, and event logging
Replace init.d scripts with declarative config files
⚫
Expose newer kernel APIs to userspace via a simple interface
⚫
Control behavior of applications via unit files rather than with code changes
Benefits
⚫
Modulararity
⚫
Asynchronous and concurrent;
⚫
Described by declarative sets of properties;
⚫
Bundled with analysis tools and tests;
⚫
Features a fully language-agnostic API.
⚫

---

## Slide 8: GPL

- The GNU General Public License (GNU GPL or GPL) is a widely-used free software license, which guarantees end users the freedom to run, study, share and modify the software
- The GPL is a copyleft license, which means that derivative work can only be distributed under the same license terms. This is in distinction to permissive free software licenses, of which the BSD licenses and the MIT License are widely-used examples. GPL was the first copyleft license for general use.

> **Text from slide image (OCR, may contain errors):**
>
> Free asin Freedom  

---

## Slide 9: Example OS Services (High Level)

- 
- 
- 
- 
- 
- 
- 
- 
- 

Directory Services (LDAP, AD, DNS)
OS Firewall
VPN/Encryption
Antivirus / AntiSpam / antimalware/spyware/ransomeware
Print Clients
Patching / Updating / Upgrading
Remote management (SNMP/Telegraf)
Web Services (Web Server / REST API)
License Server

---

## Slide 10: Load Averages and Performance

Monitoring
- System load/CPU Load – is a measurement of CPU over or underutilization in a Linux system; the number of processes which are being executed by the CPU or in waiting state
- Load average – is the average system load calculated over a given period of time of 1, 5 and 15 minutes
- In Linux, the load-average is technically believed to be a running average of processes in it’s (kernel) execution queue tagged as running or uninterruptible
- Shown by utilities such as uptime, top and ‘cat /proc/loadavg’ $ uptime 07:13:53 up 8 days, 19 min, 2.21

1 user,

load average: 1.98, 2.15,

---

## Slide 11: IDENTITY MANAGEMENT

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 12: What is SAML?

- What is SAML?
- Security Assertion and Markup Language is an XMLbased standard for exchanging authentication and authorization between security domains.

- Why is it Important?
- SAML abstracts the security away from platform architectures and vendor implementations.

---

## Slide 13: OAuth

- 

- 

- 

- 

OAuth is an open standard for access delegation, commonly used as a way for
Internet users to grant websites or applications access to their information on other websites but without giving them the passwords
This mechanism is used by companies such as
Amazon,[2] Google, Facebook, Microsoft and
Twitter to permit the users to share information about their accounts with third party applications or websites
OAuth is a service that is complementary to and distinct from OpenID. OAuth is unrelated to OATH, which is a reference architecture for authentication, not a standard for authorization. However, OAuth is directly related to OpenID Connect (OIDC), since OIDC is an authentication layer built on top of OAuth
2.0 https://tools.ietf.org/html/rfc6749 The OAuth
2.0 Authorization Framework

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Authentication · Who · YOU · Please · referral · notarized · letter · stating · is · the · ertificate · name: · notary: · Pseudo-Authentication · using · OAuth · me · alet · unt · Plea · issue · mea · that · tne · key* · for · core · ner · of · th  

---

## Slide 14: Identity Provider

- An Identity Provider is a trusted system that authenticates users for the benefit of other, unaffiliated websites or digital resources
- By properly utilizing multi-factor and context-based authentication, as well as strong encryption, even securitynaive enterprises can build secure software platforms

- 
- 
- 
- 

OneLogin
Okta
Auth0
Duo

> **Text from slide image (OCR, may contain errors):**
>
> amazon\VorkSpaces  
> Salesforce  
> Office 365  
> User is redirected  
> to IdP for  
> Authentication IdP returns an  
> accept/reject response  
> in SAML assertion or  
> cloud app  
> security token  
> Username  
> Known Device  
> SAML Assertion  
> by IdP  

---

## Slide 15: What is Active Directory

- 

Active Directory (AD) is Microsoft's proprietary directory service.

- 

AD runs on Windows Server and allows administrators to manage permissions and access to network resources.

- 

It consists of a collection of services
(Server Roles and Features) used to manage identity and access for and to resources on a network

- 

A server running Active Directory Domain
Service (AD DS) role is called a domain controller. It authenticates and authorizes all users and computers in a Windows domain type network—assigning and enforcing security policies for all computers and installing or updating software

Domain
Services

- 

Federation
Services
- 

- 
- 

Network
Access for
External
Resources

Internal
Accounts
Authorization
Authentication

Certificate
Services
- Identity
- NonRepudiation

Active Directory

Rights
Management
Services
- 

Content
Security and
Control

- 
- 
- 

Identity
Access
Centralized
Management

Lightweight
Directory
Services
- 

Application
Templates

---

## Slide 16: Active Directory Roles

- AD Domain Services (AD DS)
- Users, Computers, Policies

- AD Certificate Services (AD CS)
- Service, Client, Server and User identification

- AD Federation Services (AD FS)
- Resource access across traditional boundaries

- AD Rights Management Services (AD RMS)
- Maintain security of data

- AD Lightweight Directory Services (AD LDS)

---

## Slide 17: BREAK

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 18: Virtual File System (VFS)

- VFS is the essential concept in UNIX-like FS
- Specify an interface between the kernel and a concrete file system
- Introduced by SUN in 1985

- Pass system calls to the underlying file systems
- E.g. pass sys_write() to Ext4 (i.e. ext4_write())

- Three major metadata in VFS
- Metadata: the data about data (wikipedia)
- Super block, dentry and inode
- OO design
- Each component defines a set of data members and the functions to access them

---

## Slide 19: Inode

- “Index-node” in Unix-style file system
- All information about one file (or directory)
- Except its name
- In UNIX-like system, file names are stored in the directory file: the content of it is an “array” of file names

- E.g. owner, access rights, mode, size, time and etc.
- Pointers to data

---

## Slide 20: General Optimizations

- Based on two principles:
- RAM access is much faster than the access on disk
- Sequential IOs is much faster than random IOs on disk

- So we design file systems that
- Largely utilizes CPU/RAM to reduce IO to disks (various caches/write buffers)
- Prefers sequential IOs
- Computes disk layout to arrange related data sequentially located on disks

---

## Slide 21: Page Cache

- …a “transparent” buffer for disk-backed pages kept in RAM for fast access… [wikipedia]
- A write-back cache
- Main purpose: reducing the # of IOs to disks
- Access based on page (usually 4KB).
- Page cache is per-file based.
- A Redix-tree in inode object.
- Prefetch pages to serve future read
- Absorb writes to reduce # of IOs

- The dirty pages (modified) are flushed to disks for : 1) each 30s or 5s, or 2) OS wants to reclaim RAMs
- Also can be forced to flush by calling “fsync()” system call

---

## Slide 22: Hard Disk Drive (HDD)

- Stores data on one or more rotating disks, coated with magnetic material
- Introduce by IBM in 1956
- Use magnetic head to read data

---

## Slide 23: SSD

> **Text from slide image (OCR, may contain errors):**
>
> Solid-state storage terms  
> TERM DESCRIPTION  
> Solid-state drive (SSD) SSD is typically used to refer to solid-sate storage that is packaged in hard disk form factor.  
> This is type of flash that stores single bit in each chip cell. It is the fastest, most reliable,  
> Sing (SLC) longest lasting and most expensive type of NAND flash.  
> This is NAND flash chip that stores two bits per cell. It is slower and doesn't last as long  
> Colt CALC) as SLC, but is much cheaper  
> Enterprise multi-level eMLC is “souped up” version of MLC flash with controller and software that remedies some  
> cell (eMLC) of the shortcomings of MLC. It is becoming more popular in enterprise solid-state products.  
> PCI Ex (PCle) PCle is high-speed server bus technology that is used by number of serer-based solid-state  
> storage products  
> Non-volatile random This is high-speed memory that is extremely fast like DRAM, but can retain data when  
> access memory (VMRAM) the power is turned off. It is used as cache in some flash solid-state storage systems.  
> FeckFarget  

---

## Slide 24: RAID, Redundant Array of Inexpensive Disks, or Redundant Array of Independent Disks, is a data storage virtualization technology that combines multiple physical disk drive components into one or more logical units for the purposes of data redundancy, performance improvement, or both

> **Text from slide image (OCR, may contain errors):**
>
> BREAKDOWN OF COMMON RAID LEVELS  
> Hewlett Packard  
> Enterprise SD  
> CER  
> MINIMUM COMMON  
> RAID LEVEL METHOD SOFTWARE OF DISKS USAGE  
> COST- NO  
> JBOD  
> BENEFITS  
> HIGH  
> HEAVY READ DATA IS LOST IF  
> LAG FOR WRITE  
> STANDARD TOLERANCE  
> MIRRORING APP SERVERS HIGH READ (BY  
> LAG FOR WRITE  
> STRIPING SPEED+FAULT OPS, REDUCED  
> PARITY TOLERANCE STORAGE  
> LOW WRITE  
> STRIPING LARGE FILE PERFORMANCE,  
> DOUBLE STORAGE APP REDUCED  
> SERVERS STORAGE  
> PARITY PERFORMANCE (BY 215)  
> WRITE REDUCED  
> STRIPING PERFORMANCE STORAGE  
> MIRRORING STRONG FAULT LIMITED  
> TOLERANCE SCALABILITY  
> What Happened to and  
> The RAID levels described above are the most common levels used in enterprise scenarios.  
> The levels in between are highly specialized and only make sense in very specific scenarios.  

---

## Slide 25: Block Storage

- Structure & Access:
- Stores data in fixed-size blocks.
- Presents raw storage volumes that must be formatted with a file system.
- Accessed via protocols like iSCSI or Fibre Channel (common in SANs).

- Characteristics:
- Provides high performance and low latency.
- Offers fine-grained control over data placement and caching.

- Common Use Cases:
- Databases, virtual machine storage, transactional applications where speed and efficiency are critical.

---

## Slide 26: File Storage

- Structure & Access:
- Organizes data into files and directories using hierarchical file systems.
- Accessed over network protocols such as NFS, SMB, or CIFS (typical of NAS systems).

- Characteristics:
- Familiar to users with traditional folder/file organization.
- Ideal for collaborative environments with shared access and file-level permissions.

- Common Use Cases:
- Document management, user home directories, content repositories, and collaborative file sharing.

---

## Slide 27: Object Storage

- Structure & Access:
- Stores data as discrete objects that include the data itself, metadata, and a unique identifier.
- Uses RESTful APIs (HTTP/HTTPS) for access, rather than traditional file system protocols.

- Characteristics:
- Highly scalable and distributed, making it well-suited for large volumes of unstructured data.
- The embedded metadata enables sophisticated data management, search, and retrieval.

- Common Use Cases:
- Cloud storage services, backup and archival systems, media storage, and big data analytics where scalability and cost-effectiveness are key.

---

## Slide 28: Comparative Summary

- Performance:
- Block Storage: Excels in performance and low latency, ideal for high-demand applications.
- File Storage: Provides ease of use and collaborative sharing, with moderate performance.
- Object Storage: Offers scalability and metadata-rich storage, often with higher latency than block storage.

- Scalability & Management:
- Object Storage: Designed to scale out massively with a flat namespace and efficient metadata handling.
- Block & File Storage: May require more planning to scale and often need additional management tools for large environments.

- Choosing the Right Storage:
- Block Storage: Best for applications requiring high I/O performance and direct disk access.
- File Storage: Suitable for environments where ease of file sharing and hierarchical data organization are essential.
- Object Storage: Ideal for unstructured data at scale, especially when cost and longterm data management are priorities.

---

## Slide 29: Enterprise Management

PUPPET/CHEF/ANSIBLE

---

## Slide 30: What are Puppet and Chef?

- 

Puppet is a next-generation server automation tool. It is composed of a declarative language for expressing system configuration, a client and server for distributing it, and a library for realizing the configuration.

- 

Chef is a configuration management tool written in Ruby and Erlang. It uses a pureRuby, domain-specific language (DSL) for writing system configuration "recipes".
Chef is used to streamline the task of configuring & maintaining a company's servers, and can integrate with cloud-based platforms such as Rackspace and
Amazon EC2 to automatically provision and configure new machines.

---

## Slide 31: What is Ansible?

- 

- 

Ansible is an IT automation engine that automates cloud provisioning, configuration management, application deployment, intraservice orchestration, and many other IT needs.
It uses no agents and no additional custom security infrastructure, it uses a very simple language (YAML, in the form of Ansible
Playbooks) that allow you to describe your automation jobs in a way that approaches plain English.

Sample Playbook
- -layer3ip:
- { interface: vlan10, ip: 10.1.10.3, mask: 24 }
- { interface: vlan20, ip: 10.1.20.3, mask: 24 } vpc: domain: 100 systempri: 2000 rolepri: 2000 pkl: src: 10.1.20.3 dest: 10.1.20.2 vrf: keepalive hsrp_priority: 100

https://github.com/jedelman8/nxos-ansible

---

## Slide 32: Declarative vs Imperative

Puppet (declarative)

Shell script (imperative)

user { ‘cgascoig’ : ensure => present, gid => ‘admin’,
}

#!/bin/bash

group { ‘admin’ : ensure => present,
}

if ! getent group sysadmin >/dev/null then echo "Group sysadmin does not exist, creating" groupadd sysadmin fi if ! getent passwd chris >/dev/null then echo "User chris does not exist, creating" useradd --gid sysadmin chris fi
USERGROUPID=`getent passwd chris | awk -F: '{print $4}'`
USERGROUPNAME=`getent group $USERGROUPID | awk -F: '{print
$1}'` if [ "$USERGROUPNAME" != "sysadmin" ] then echo "Primary group of user chris is not sysadmin, updating" usermod --gid sysadmin chris fi

---

## Slide 33: Why Ansible

- 
- 
- 
- 
- 
- 
- 
- 
- 

It is a free open source application
Agent-less – No need for agent installation and management
Python/YAML based
Highly flexible and configuration management of systems.
Large number of ready to use modules for system management
Custom modules can be added if needed
Configuration roll-back in case of error
Simple and human readable
Self documenting

---

## Slide 34: Components

Intranet/internet cloud
Aws,
Azure csr1000v

Ad-hoc / playbook commands
Hosts inventory

Playbooks

Connection plugins

Ansible
Core
Modules

127.0.0.1

Plugins
For email, stdout callback(s etc )

---

## Slide 35: IN-CLASS EXERCISE

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 36: In-Class: Programming with LLMs

Use a language model to help your team write a program that does the following:
1.
2.
- 
- 
- 
- 
- 
- 
- 

Takes a text string as input
Outputs a message about the sentiment of the text string, whether it’s “Positive”, “Negative” or “Neutral”. See also Sentiment
Analysis
Include tests showing all the sentiments and submit a word document with screenshots of the program operations and tests.
Include a link to your source code on github, etc..
Use any programming language you prefer
This is a group assignment
Include the entire related LLM (ChatGPT) session history in your submission for this assignment, including all the prompts you used.
Try Testing it on a sentiment dataset, e.g., https://www.kaggle.com/datasets/abhi8923shriv/sentiment-analysis-dataset
Hint: TextBlob

Extra Credit:

- 

II Use a language model to help your team solve HackerRank coding problems, in the language of your choice:
- 
- 
- 
- 

- 

https://www.hackerrank.com/domains/java https://www.hackerrank.com/domains/c https://www.hackerrank.com/domains/python https://www.hackerrank.com/domains/cpp

1.One each of: Easy, Medium, Hard
First, use a simplistic prompt, and show the initial score from HackerRank
Second, use Prompt Engineering techniques to refine your answer, and show the HackerRank score for the improved answer

---

## Slide 37: Homework

- Reading:
- Newman (ch. 2)
- Understanding IP Addressing: https://www.cisco.com/c/en/us/support/docs/ip/r outing-information-protocol-rip/13788-3.pdf

- HW 1 Ansible Assignment

---
