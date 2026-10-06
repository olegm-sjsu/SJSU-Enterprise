# Lecture-02b-SESSION CMPE-272-Bond FA26

Source: `Lecture-02b-SESSION_CMPE-272-Bond_FA26.pdf` (33 slides)

## Slide 1: CMPE-272

Enterprise Software Platforms

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: SAN · JOSE · STATE · UNIVERSITY · SJSU  

---

## Slide 2: - OSI Model & IP Data Networks

- 7 Layers of OSI Model
- Basic Purpose and functions of various network devices such as routers, switches, bridges and hubs
- Common services and network functions

- Network Utilities (ping, telnet, ssh, ifconfig, ip – and how to use them)
- IP Addressing (v4)
- Classes, Subnet, Mask, Multicast, VLSM, Notation Reference Sheets: IPv4 IPv6

Basic Networking Concepts
What you should already know

> **Text from slide image (OCR, may contain errors):**
>
> Subnets Decimal to Binary  
> CIDR Subnet Mask Addresses Wildcard Subnet Mask Wildcard  
> /10 255.192.0.0 4,194,304 0.63.255.255 Classful Ranges  
> 240.0.0.0 268,435,456 Reserved Ranges  
> 224.0.0.0 536,870,912 31.255.255.255 RFC 1918 10.0.0.0 10.255.255.255  
> 192.0.0.0 1,073,741,824 63.255.255.255 Localhost 127.0.0.0 127.255.255.255  
> 128.0.0.0 2,147,483,648 127.255.255.255 RFC 1918 172.16.0.0 172.31.255.255  
> 4,294,967,296 255.255.255.255 RFC 1918 192.168.0.0 192.168.255.255  

> **Text from slide image (OCR, may contain errors):**
>
> HTTP, FTP,  
> Application Application POP,SMTP,  
> DNS, RIP  
> Token Ring  

> **Text from slide image (OCR, may contain errors):**
>
> CH BI) Subnet ID Bits  
> Class Default  
> Left-Most  
> Binary Subnet  
> Mask Converted  

---

## Slide 3: QUIC (Quick UDP Internet

Connections)
Key Characteristics of QUIC
- QUIC is designed to address several limitations in TCP and provide better support for the modern web, where low-latency connections and secure communication are essential. The major characteristics of QUIC include:

- UDP-Based Transport
- Unlike TCP, which operates at the transport layer of the OSI model and is widely used for reliable transmission of data, QUIC operates over UDP (User Datagram Protocol).
- UDP is a lightweight, connectionless protocol. However, UDP lacks features like connection management, reliability, and congestion control. QUIC builds these features on top of UDP, effectively adding reliability, ordering, and encryption to a connectionless transport layer.
- The use of UDP allows QUIC to bypass many of the limitations of TCP, especially those related to latency and slow connection setup, while preserving the advantages of reliability.

---

## Slide 4: Multiplexing Without Head-of-Line

Blocking
- One of the significant problems with HTTP/2 over TCP is head-of-line blocking. If one packet is lost in TCP, all subsequent packets must wait for that lost packet to be retransmitted, causing delays across all streams using the same TCP connection.
- QUIC solves this by multiplexing multiple streams over a single connection and handling packet loss on a perstream basis. This means that if a packet is lost for one stream, other streams can continue without delay, significantly improving performance in environments with packet loss.

---

## Slide 5: What is Switching?

- A “switch” is a hard-wired connection between 2 wires
- A switch in a network device is a nailed-down connection between input and output
- A packet is switched if the forwarding decision is pre-determined, i.e. trivial per-packet processing necessary
- Switching in packet world implies label switching
- Label switching (ATM) was an early h/w forwarding implementation
- Switching therefore came to mean forwarding in h/w, as opposed to s/w
- Switching has morphed into a marketing term

---

## Slide 6: What is a VLAN?

- Virtual LAN (VLAN) – a group of interfaces on one or more LANs that are configured to communicate as if they were attached to the same wire, when in fact they are located on a number of different LAN segments:
- VLANs are logical partitions of flooding domains
- Many different ways to partition VLANs. Some examples are:
- MAC address
- Port
- Protocol

---

## Slide 7: VLAN Trunk

- A port which carries the traffic of multiple VLANs through the use of encapsulation or other explicit technique. Examples are ISL, IEEE802.1q, LANE
- Normally used as a link between forwarding devices such as switches and routers
- Each frame transmitted on a trunk link is "tagged" as belonging to one and only one VLAN

---

## Slide 8: IEEE 802.1q

- AKA, “dot1q”
- 4 byte “Tag” inserted after the regular Ethernet SA and before EtherType/Length field
- First 2 bytes shows a value of 0x8100; serves as a 802.1q EtherType
- Next 16 bits encapsulate:
- 12-bit VLAN ID
- 3 bits of priority
- 1bit of Canonical Format Identifier (CFI) - compatibility between Token Ring type and Ethernet type networks

> **Text from slide image (OCR, may contain errors):**
>
> Inter Frame Ga  
> Inter Frame Gap  

---

## Slide 9: IEEE 802.1q cont’d

- Both tagged and untagged frames are allowed on dot1q
- Untagged frames transmitted and received on dot1q are associated with the Native VLAN
- Null VLAN id with priority tagged frames are considered as untagged frames

---

## Slide 10: Layer2 Forwarding

- Unlike IGPs (Interior Gateway Layer3 Routing Protocols), Layer2 switching does not have a protocol to setup forwarding tables
- Layer2 Forwarding table (CAM table/MAC table) is build by watching source MAC address in data packets
- Layer2 Forwarding happens based on destination MAC, if entry not present in CAM then Unknown Unicast flooding is used

---

## Slide 11: Spanning Tree

- The Spanning Tree Protocol (STP) is a network protocol that builds a logical loop-free topology for Ethernet networks. The basic function of STP is to prevent bridge loops and the broadcast radiation that results from them. Spanning tree also allows a network design to include backup links to provide fault tolerance if an active link fails.
- As the name suggests, STP creates a spanning tree within a network of connected layer-2 bridges, and disables those links that are not part of the spanning tree, leaving a single active path between any two network nodes. STP is based on an algorithm that was invented by Radia Perlman while she was working for Digital Equipment Corporation.[1][2]
- In 2001, the IEEE introduced Rapid Spanning Tree Protocol (RSTP) as 802.1w. RSTP provides significantly faster spanning tree convergence after a topology change, introducing new convergence behaviors and bridge port roles to do this. RSTP was designed to be backwardscompatible with standard STP.

---

## Slide 12: Algoryhme by Radia Perlman

I think that I shall never see
A graph more lovely than a tree.
A tree whose crucial property
Is loop-free connectivity.
A tree that must be sure to span
So packets can reach every LAN.
First, the root must be selected.
By ID, it is elected.
Least-cost paths from root are traced.
In the tree, these paths are placed.
A mesh is made by folks like me,
Then bridges find a spanning tree.

Just don't call her the mother of the internet

---

## Slide 13: LAYER 3: IP ROUTING

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 14: IGP vs. EGP

- 
- 
- 
- 
- 

An AS (Autonomous System) is a single SP’s network
The IGP protocols in use today are: RIP/RIPNG, IGRP, EIGRP, IS-IS, OSPF
There is only 1 EGP: BGP
IGP’s route with an AS or enterprise
EGP’s route between AS’s

---

## Slide 15: Internet inter-AS routing: BGP

- BGP (Border Gateway Protocol): the de facto inter-domain routing protocol
- “glue that holds the Internet together”

- allows subnet to advertise its existence, and the destinations it can reach, to rest of Internet: “I am here, here is who I can reach, and how”
- BGP provides each AS a means to:
- 
- 

eBGP: obtain subnet reachability information from neighboring ASes iBGP: propagate reachability information to all AS-internal routers.

- determine “good” routes to other networks based on reachability information and policy

Network Layer: 5-15

---

## Slide 16: BGP For Enterprise Networks

> **Text from slide image (OCR, may contain errors):**
>
> Global Global Global  
> ISP ISP ISP ISP  

---

## Slide 17: Single-homed network

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: ISP · Single-Homed · Branch  

---

## Slide 18: Multi-Homing

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 19: Scenario 1 – Same PE / CE

> **Text from slide image (OCR, may contain errors):**
>
> Global Global  
> Internet Internet  
> ISP ISP  
> T1 DSL LTE  
> HA using common HA using different  
> access technology access technologies  

---

## Slide 20: Scenario 2 – Different PEs / Single CE

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: ISP · Presented · as · Two · distinct · single · L3 · node · nodes  

---

## Slide 21: Scenario 3 – Different PEs and CEs

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: ISP · wy · Presented · as · single · L3 · node  

---

## Slide 22: Scenario 4 – Multiple ISPs

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Global · Internet · ISP  

---

## Slide 23: Datacenter Billing

- Committed Information Rate (CIR)
- CIR is a guarantee that the port will always have the bandwidth you’re paying for available to it
- Traditional TDM circuits such as Frame Relay use this method for provisioning so a customer always knows they are going to get
- Has a hard cap without any allowance for bursting
- This allows the ISP to tightly control the amount of bandwidth entering and leaving their network, which is required on large broadband networks where a given segment is likely oversubscribed rather than overprovisioned
- Often Asymmetric B/W (Up/Down)

---

## Slide 24: P95: 95th Percentile Metering

- P95 is a bandwidth usage metering scheme that allows a customer to burst beyond their committed base rate, and still provides the carrier with the ability to scale their billing with the cost of the infrastructure and transit commits (if any)
- Carriers sample the amount of data transferred on a customer’s port(s) every 5 minutes and use that value to derive a data rate (typically in megabits per second or Mbps) for that 5 minute interval

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Original · Data · Samples · Date  

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: 10 · Sorted · Data · Samples · 95th · Percentile · ~6Mbps · 16 · 21 · 26 · 32 · 37 · 63 · 79 · 95  

---

## Slide 25: Modern Datacenter Networks

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 26: Management, Control Plane & Data Plane

Control Plane
-  Makes decisions about where traffic is sent
-  Control plane packets are destined to or locally originated by the router itself
-  The control plane functions include the system configuration, management, and exchange of routing table information
-  The route controller exchanges the topology information with other routers and constructs a routing table based on a routing protocol, for example, RIP, OSPF or BGP
-  Control plane packets are processed by the router to update the routing table information.
-  It is the Signalling of the network
-  Since the control functions are not performed on each arriving individual packet, they do not have a strict speed constraint and are less time-critical

Data Plane
-  Also known as Forwarding Plane
-  Forwards traffic to the next hop along the path to the selected destination network according to control plane logic
-  Data plane packets go through the router
-  The routers/switches use what the control plane built to dispose of incoming and outgoing frames and packets

http://sdntutorials.com/difference-between-control-plane-and-data-plane/

> **Text from slide image (OCR, may contain errors):**
>
> Management, Control and Data Planes  
> Adjacent router Adjacent router  
> Management Policy plane  
> Configuration CLI GUI  
> 4d Routing Control plane Control plane  
> Neighbor Link state IP routing  
> table database table  
> Forwarding table  

---

## Slide 27: Clos networks

- 

- 

- 
- 
- 

- 

First researched in the mid-1950s as a method to switch telephone calls. Clos networks evolved into crossbar topologies and eventually into chassis-based Ethernet switches using a crossbar switching fabric. Now Clos networks are being used in modern data center networking architectures to achieve high performance and resiliency
Charles Clos was a researcher at Bell Laboratories in the
1950s. He published a paper titled "A Study of Non-blocking
Switching Networks" in the Bell System Technical Journal in
1953
Clos networks evolved into crossbar topologies and eventually into chassis-based Ethernet switches using a crossbar switching fabric
Now Clos networks are being used in modern data center networking architectures to achieve high performance and resiliency
Crossbar fabrics fell out of favor because they were subject to Head Of Line (HOL) blocking due to input queue limitations. Over time, Ethernet switches were developed that had input and output queues on all the interfaces
Modern Ethernet switches have more advanced fabric technologies, output queuing and priority-based flow control so they can now achieve non-blocking performance https://www.networkworld.com/article/2226122/cisco-subnet/clos-networks--what-s-old-is-new-again.html

---

## Slide 28: Traditional Data Center Architecture

- 

- 

Modern Ethernet switches have more advanced fabric technologies, output queuing and priority-based flow control so they can now achieve non-blocking performance. With these technical enhancements, switches can now support guaranteed bandwidth connectivity for protocols like Fiber Channel over Ethernet
(FCoE) using 10 Gigabit Ethernet linksues on all the interfaces the "fat tree" model

The problem with traditional networks built using the spanning-tree protocol or layer-3 routed core networks is that a single "best path" is chosen from a set of alternative paths. All data traffic takes that "best path" until the point that it gets congested then packets are dropped. The alternative paths are not utilized because they topology algorithm deemed them to be less desirable or removed to prevent loops from forming.

---

## Slide 29: Leaf/Spine Clos Architecture

- 
- 
- 
- 
- 

Clos networks have now made their second reappearance in modern data center switching topologies
Rather than being a fabric within a single device, the Clos network now manifests itself in the way that the switches are interconnected
Data center networks now comprised of top of rack (ToR) switches are the leaf switches attached to the core switches which represent the spine
Leaf switches are not connected to each other and spine switches only connect to the leaf switches (or an upstream core device)
In this Spine-Leaf architecture, the number of uplinks from the leaf switch equals the number of spine switches. Similarly, the number of downlinks from the spike equal the number of leaf switches.

---

## Slide 30: Example: Cisco ACI

- 

- 
- 

- 

ACI fabric decouples the tenant endpoint address, its identifier, from the location of the endpoint that is defined by its locator or VXLAN tunnel endpoint (VTEP) address
Forwarding within the fabric is between VTEPs
Mapping of the internal tenant MAC or IP address to a location is performed by the VTEP using a distributed mapping database
With this model, we can have a full mesh, loop-free topology without the need to use the spanning-tree protocol to prevent loops

---

## Slide 31: Network Access Translation (NAT)

NAT Concepts
- 

Inside and Outside Addresses
- 
- 

- 
- 

- 

inside local address: This is the inside address as it is seen and used within the organizational network. inside global address: This is the inside address as it is seen and used on the outside of the organizational network. outside local address: This is the outside address as it seen and used within the organizational network. outside global address: This is the outside address as it is seen and used on the outside of the organizational network.

NAT Types
- 
- 
- 

Static address translation (Static NAT): This type of NAT is used when a single inside address needs to be translated to a single outside address or vice versa.
Dynamic address translation (Dynamic NAT): This type of NAT is used when an inside address (or addresses) need to be translated to an outside pool of addresses or vice versa.
Overloading (Port Address Translation (PAT)): This type of NAT is a variation on dynamic NAT. With dynamic NAT, there is always a one to one relationship between inside and outside addresses; if the outside address pool is ever exhausted, traffic from the next addresses requesting translation will be dropped.
With overloading, instead of a one to one relationship, traffic is translated and given a specific outside port number to communicate with; in this situation, many internal hosts can be using the same outside address while utilizing different port numbers.

> **Text from slide image (OCR, may contain errors):**
>
> Inside Cloud  
> 172.16.10.8/24 Outside Cloud  
> web server listenting to  
> TCP port 8080  
> Inside NAT  
> devices Router  
> In the above topology, devices on the  
> outside are sending web traffic to TCP  
> port 80 but the webserver on the inside  
> is only listening on TCP port 8080  

---

## Slide 32: Wireshark application

(www browser, email client)

packet analyzer

application
OS

packet capture
(pcap)

copy of all
Ethernet frames sent/received

Transport (TCP/UDP)
Network (IP)
Link (Ethernet)
Physical

---

## Slide 33: Readings and Project

I. Review/Study this slide deck and links/references
II. Read: Fowler (ch. 2), Newman (ch. 3), and: http://martinfowler.com/articles/microservices.html

---
