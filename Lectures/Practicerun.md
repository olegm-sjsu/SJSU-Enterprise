## Session 1

What makes software an enterprise application, and why enterprise architecture is needed.
(Lecture-01, slides 20 and 21)

An enterprise software application is usually a piece of software used by a huge set of teams.
An enterprise software is very complex, usually has different roles like admin, customer, employee, Usually distributed to handle a lot of traffic and multiple locations. Has an authorization and authentication flow. 

reduced complexity and shows the one source of thruth. for buisnessed. combines multiple depenedcies and services into one dashboard. 


• The two enterprise architecture frameworks named in class, Zachman and TOGAF, and what
TOGAF consists of. (Lecture-01, slides 22 and 70)

TOGAF has 4 components, 
buisness architecture: Defines buisness strategy, governance
data architecture: descibes how the enterprise stores and manages data
application architecture  outlines desing and deployment of software
techonolgy architeectrue defines what kind of hardware, software and infastructure is needed for the buisness. 

Zachman is a way of oreneizing the info for an enteprise, it is a matrix of roles x questions. Only if all are filled it we will know a buisness


• What Ansible automates, how it reaches hosts, and why it needs no agent. (Lecture-01, slides 43
and 44)
Ansible is a way to deploy applications to servers and manage many servers, it connects to servers via ssh or other remote apis. Ansible is python and yaml based so it doesnt require any more software to run. Its agentless becasue it runs on existing ssh 


• Ansible's components: inventory, modules, plugins, playbooks. (Lecture-01, slide 45)
inventory: defines the target system that ansible will manage
modules:are the actual code that ansible runs to get to the final state
plugins: extensions of ansible, plugins are installed on the main node and extend fuctionality. 
Playbook: a yaml file that defines the end state of a server. it is idempotent 

• Ad-hoc commands against playbooks; playbook sections, variables, facts, privilege escalation,
tasks and handlers, roles. (Lecture-01, slides 53 to 65)

An adhoc comment is a in terminal comment that you can run instead of writing a playbook

playbok sections:
Users/hosts : where the server is and how to access. 
Tasks: defines the modules that are executed
Play: defines which hosts get which tasks executed
modules: the code executed. 
variables: values that can be used in plays
registered varibles: allow you to caputre output from a run and assign to variable
facts: information discovered from the host. 
Privalage:
become can transform you into another user. can use methos like sudo to become a user. set in become_method, there is also just become:yes that allows you to switch and become_user is the desired role you want to become. 
Roles: breaking a playbook into multiple files for reuse and modularization

Modules are idempotent and report when they change something.
A task can notify a handler.
A handler is a named task that runs only if notified. It runs once, at the end of the play, however many tasks notified it. The slide's example is restarting Apache once after several config changes.


## Session 2
### part1
Types of operating systems, and the OS services an enterprise runs. (Lecture-02a, slides 16 and
48)

Operation systmes: Unix/Linux and Windows are the main ones

•  Load averages and the tools that show them. (Lecture-02a, slide 49)
load avarge: avarage system load over a certain amount of time, Shown by utilities like uptime, top and ‘cat /proc/loadavg’

•  Identity: SAML, OAuth and OpenID Connect, identity providers, Active Directory roles.
(Lecture-02a, slides 55 to 59; 66)
SAML is a markup language exchange authentications and authorizations between domains
OAuth is a way to grant access without giving ayone password.

OAuth: Authorization, gives roles to users and defines what they can do
Identity providers: Duo, Okta. 


AD Domain Services: Authenticates users and holds all users, plicies and computers. basically auth
AD Certificate Services: makes certificates to identify services, clients servers and users. basically giving identity
AD Federation Services: Lets people access multiple services and resources from one. 
AD Rights managment services: controls who can open and edit content
AD Lightweight direcotry services: created directory without a full new domain

•  File systems: the virtual file system, the inode, why file systems prefer RAM and sequential I/O,
the page cache. (Lecture-02a, slides 81 to 89)

VFS is an interface between kernel and actual file system. it is meant to handle many file system with the same calls. 

INode: hold info about a file exept its name. liek owner, access rigths, mode, size pointers. 
files namees are in the directory file, list that maps name and inode. 
exam point: 2 names can point to one inode. 

RAM is much faster then any disk. Seqential IO is much faster then random io becuase it deosnt have to look. Files systmes use ram to reduce disk io and write thoutgh buffers. related data sits together on disk. 

Page cache: stores data in a buffer in pages and reduced the io to disk. It first saves to ram and then writes to disk later. may small writes become one big write. dirty pages indicate whether data has changed. 

•  Disks and RAID. (Lecture-02a, slides 98 and 106)

HDD is a storage that writes onto an acutal disk. it is mechanical and has to seek to look for data. random io is slow but sequential is fast.

SSD:
no moving parts
SLC: one bit per cell
MLS: 2 bits per cell, slower but cheaper
eMLC: aimed for enterprise
PCie High Speed Server bus
NVRAM: keeps data when powered off. 

RAID: Redundant Array of Independent, originally Inexpensive, Disks
combines multiple phisical disks  into one or more logical units to redundancy and performances.
protects agains disk failures

Building blocks:
Striping splits data across disks for speed.
Mirroring copies data to another disk for fault tolerance.
Parity is extra computed data that lets you rebuild a lost disk.

•  Block, file and object storage: how each is accessed, what each is good for. (Lecture-02a, slides
109 to 112)
Block:
Data is sotred in fixed blocks. iSCSI or Fibre Channel protocols
used for perforamce and low latency, and control over data placement and caching
Like a disk

Fils: 
Hierachrical like an acual file system with direcotries with protocols NFS, SMB, or CIFS
used for shared access and permissions for files and direcotries.
strucutres liek a traditional file system.

Object storage: 
stores data in objects with metadata attached. 
access with rest apis
scales and distributed, supports search and retrieval. big data. 

•  Puppet, Chef and Ansible; declarative against imperative configuration. (Lecture-02a, slide 124)

Puppet: server automation. Declarative, client server model so it uses an agent 

Chef: in ruby its a configuration management tool. 

ansible: agentless server automation and deployment

all keep many servers in a known state


Declarative: describe desired end state wihtout sayign how to get there
inparative: write exact steps


### part 2

The OSI model and IP addressing you are expected to know already. (Lecture-02b, slide 5)


•  QUIC: what it adds on top of its transport, and how it avoids head-of-line blocking. (Lecture-02b,
slides 7 and 8)

It builds on top of UDP and adds reliability, connection management and congestion control
it deosnt need a handshake like TCP and can jsut send messages. it is low latency

If one packet is lost it will nto wait like TCP it will instead have other packets finish.
IT knows abotu streams and only a certain stram will halt


•  Switching, VLANs, trunks and 802.1Q tagging, including the native VLAN. (Lecture-02b, slides 39
to 45)

A switch is a connection between 2 wires. Network switching is connection input and output.

VLan: Multiple lan networks acting as if they are communicatin on the same Lan

Trunk: port that carries traffic to many vlans over one link. 

802.1Q Tagging
its a tagging standart. inserts a 4 byte tag into ehternet frame. tag contains mark, 12 bit vlan id allows for 4000 vlans, 3 bit priority, 1 compatability bit.

native VLAN: both tagged and untagged frames allowed. untagged is assigned to native vlan.

•  How a switch builds its forwarding (CAM) table, and what it does with an unknown destination.
(Lecture-02b, slide 53)

CAM table lists with mac adresses is reachable out of which port. 
watches source MAC Adress, of every frame. writes, this mac adress is this port. 
it learns liek that

forwards:  looks at destination mac adress of the frame, if its in cam it sends one port.
if none it does unicast flooding and sends to all ports except to the one it came
when device answers it will learn the port.

•  Spanning Tree. (Lecture-02b, slide 54)
It builds a tree out of the conneteted switches which guarantees no loops


•  Routing: IGP against EGP, BGP, eBGP and iBGP, multi-homing to one or more providers.
(Lecture-02b, slides 65, 79 and 88)

an Autonoumous system is a network
an IGP is a protocl for route inside the AS
and EGP is the route between AS

BGP is standart protocol for routing between networks, its hwo the internet works

eBGP is  BGP between different AS. gets info from neighbors
iBGP is routing inside the same AS and shres routes inside.


•  Data center billing: committed information rate against 95th-percentile metering. (Lecture-02b,slides 104 and 105)
CIR lets you gurantee that the port will alwasy have the bandwidth that you are paying for. Its a hard cap

p95 lets you burts above base rate as long as its short. 
Throws away the top5% highest so you are only billed for the 95% lowest.  only sustained usage is going on the bill
•  Control plane against data plane. (Lecture-02b, slide 109)
control plane: makes desicions about where traffic is sent.
handels config and exchange of info
builds routing tabel

Data Plane: forwards traffic to the next hop. 
packets go thought the router. 
has to be fast.

•  Data center designs: Clos networks, the traditional design, leaf/spine, Cisco ACI. (Lecture-02b,
slides 110 to 114)
Trad: built with spanning tree, builds the best path then all traffic uses it. 

Leaf/spine:
swtiches interconnected 
Leafs are swtiches thayt servers connect to. 
spines are connecting leaves
connects everyr leaf to ever spne but not eachother. 

CiscoACI:
example of leaf spine, 

•  NAT: inside and outside addresses; static NAT, dynamic NAT and overloading (PAT).
(Lecture-02b, slide 136)
 Nat takes your private adress and converts into a public one on teh way out then back in in converts it bak to private. 
 Static: one to one
Dynamic: one priv to many pub
overloading: many priv to one pub with ports

## Session 3

•Legacy and modern inter-process communication: RPC, CORBA, SOAP, WSDL, REST, Thrift.
(Lecture-03, slide 6)
RPC: remote procedure calls

•  REST: the properties it aims for and its architectural constraints. (Lecture-03, slides 7 to 9)
Performance:  
Scalability
Simplicity
Modifiability
Visibility
Portability
Reliability

Rest is stateless cashable and idopotent

•  Protocol Buffers and gRPC: serialization, transport, the four call types. (Lecture-03, slides 10 and
11)
Turn data into compact bytes
like json but faster
.proto file defines message types
compile befroe sent and decompile when recieve

gRPC
calling funcitons on a server as if they are local
protobuf is the IDL, HTTP is transport
unary:
request 1 responce 1
server streaming, request 1 responce many
client streaming, request many responce 1
bidirectional, many to many


•  The enterprise service bus, message buses and message queues. (Lecture-03, slides 12 to 14)

many techonologeis and services need to talk to eachother
ESB
uniform way on moving messages, 
like a post office, everythign arrives there and gets distributed
one way to send messages
apps dont connect directly so a broken piece doesnt break everything

•  Enterprise Integration Patterns: channels, message construction, routing, transformation,
endpoints, and the Rider Auto Parts example. (Lecture-03, slides 17 and 18; 28 to 37)


•  Java EE application servers and the Spring framework. (Lecture-03, slides 24 and 25; 39)

JavaEE provides an API and runtime env for runnning software for enterprise. 

Application servers is the runtime that hosts your Java EE

Spring framework is a framework an inversion of control container allows for depenacy injection

•  Inversion of control and dependency injection. (Lecture-03, slides 41 and 42)
IoC is a thing where a system can call code instead of code calling somethinig. so basically subscribign code to a change

DI: An object deosnt create the things it depends on they are brought it form teh outside. 
Constructor injection: dependencies come in through the constructor.
Setter injection: dependencies come in through setter methods.
Interface injection: dependencies are injected through methods defined in an interface.

•  Event-driven architecture: events, brokers. (Lecture-03, slides 43 and 44)
Discrete events: one time like submit

Continuous events: reapting even like a stream
Prducers detect cahnges and trigger events
consumers respond to events
event brokers route these events to the right consumers


•  Kafka, Pulsar, Dapr and Temporal. (Lecture-03, slides 46 to 50)
Kafka: topis split into partitions live on brokers
consumers are in consumer groups
storage is append only commmit log
massive thoughtput and horizontal scale
exactly once processing with idopotence + transactions

Pulsar : message streaming with compute and storage seperation
apache bookkeeper for durable segment based storage

Dapr: Runnign as a sidecar that provides building blocks
service invocation, pub/sub, state, actors, secrets, config, observabiliy

Temporal:
workflow orchestration for huge workflows
automatic retreis, backoff and timeouts,


•  DevOps and the "wall of confusion"; what makes an architecture microservices. (Lecture-03,
slides 53 to 59)
Dev ops conncets developrs who want things fast and Ops who want things stable. 


•  Service mesh: what it is, the pattern, per-node against sidecar, the three generations, AWS App
Mesh. (Lecture-03, slides 64 to 73; 80)

Service mesh is infastructuer to manage many microservices 
monitor, discover microservices
load balances and routes traffic
adds reliabioyt with health checks, timeouts

•  Contract-first API design, OpenAPI 3.1, versioning, design to mock to generate to test.
(Lecture-03, slides 92 to 96
Write the api rule before code.
code follows spec exact;y
contract is a source of thruth

OpenAPI is a standart for describing APIS, 
full json scema, 
clears paths and operations
servers with webhooks and callbacks

Prefer additive changes
depreciate in the schema, publish change log
use CI

write the contract, fake the server from it so others can start work, generate code from it, then test that the real thing matches it.


## Session 4

What microservices are, their key characteristics, their benefits and their costs. (Lecture-04,
slides 6 to 12)
Mocroservices are internal wservices that run  on a different process and are invoked by RPC's
It decentralizes compute and abstracts a lot of complexity for developers by breaking problem into small parts.
Each is independant
is stateless idealy

• SLI, SLO, SLA and the error budget. (Lecture-04, slide 13)

SLI: things that you measure about a service like latncey, error rate. 
SLO: the target for the number
SLA: promise to a customer for breakign that number
error budget: the amout of failure allowed.


• Synchronous against asynchronous communication, the modulith style, and the orchestrated and
choreographed variants with their trade-oﬀs. (Lecture-04, slides 14 to 25; 26)

synronous has halts everything until the responce is recieved. 
DE-cent: intercepts flow at entry point. 
Orchestraded sequenctial: n ochrestrator calls each service and holds all active requests. 
single point of failure
Orchestraded parallel: faster and shorter responce times
worklfow is more complex


asych does not can continue execution wuhtout the responce. 
Choreographed async event: each component listends to a central message bus and waits for event
context is part of event
owns triggered downstream events
scales well
Orchestrated, async, sequential 
each service is a producer and a onsumer on the bus. the orchestrator routes messages to services. each responce gets consumed and then next step is routed. 
Hybrid : orchestration is excellent for explicit flow, choreography handles implicit execution. The workflow can emit events at certain steps, so tasks like notifications and indexing run independently while the orchestration drives the main flow. It gives "the best of both worlds."
Async trade-offs):
Flows are hard to follow through the system.
Async systems are significantly more complex than sync ones.
Natural fit for write-heavy, but it needs mediation for synchronous reads/queries.
A sync wrapper over an async system is an entry point that invokes async flows downstream. It is a stateful component.


• Integration concerns: contract, delivery, reliability, state, observability. (Lecture-04, slides 34 to 38)

contract: agree on what the message looks like, like json, protobuf, versioning
delivery: assume message can arrive out of order and multiple times so we need to handel that
reliability: retry if it might work later and include human in the loop if needed
state: save state only after everyhting is successful, gurantees no lost events
observability: be able to follow a message from sender to reciever and track if something is wrong
• Safety measures: the circuit breaker and idempotency. (Lecture-04, slides 40 and 41)
Indempotency, make sure that if messsage comes in twice, it is the same outcome as once.
circuit breaker, monitor failures and if enought failures happend stop trying.


• Scaling: load balancer types, scaling databases, caching, service discovery. (Lecture-04, slides
42 to 48)
vertical: bigger machines
horizontal: more machines
you can scale with replication where you have multile instantces and requests can be routed to differnt intances. use a loadbalancer for that. 
classic: routes on port
NLB: we have target groups that route to intances containers or IP. 
ALB: Rich routing rules: host name, path, query string, HTTP method, headers, source IP, port.

Scalign databases:
caching and read only replicas
can scale writes by sharding (spready data over nodes)




• Containers, orchestration and the service mesh in a cloud-native platform. (Lecture-04, slides 49
to 51)
Nodes are different containers that can run on any machine, they have all instructions to run
orchestrator: a manager software that decides whihc machine to run everyhting on like kubernetes
declare desired state. 

service mesh: Tracks and help network traffic by handeling retries. 
• Conway's Law, the Inverse Conway's Law, technical sprawl. (Lecture-04, slides 55 and 56)
"That the architecture of a system will be determined by the communication and organizational structures of the company"
"That the organizational structure of any company using microservice architecture will be made up of a large number of very small, isolated, and independent teams"

techincal spreal, when you have many small teams they can choose many different paths to build stuff so you end up with a lot of differnt things

• Serverless: what it means, what triggers code, where the savings come from, and the Prime
Video case. (Lecture-04, slides 57 to 62; 66)

A serverless is a function in the cloud that boots up on demand and shuts down automatically so it doesnt spend idel time and you dotn pay for it. A call triggeres the code. 
 scales up and down instantly and automatically.

## Session 5

• Internal developer platforms and the golden path. (Lecture-05, slide 6)
A website and tools where developers can get what they need to build software. its an internal product.
scafhold -> repo -> CI/CD -> deploy -> observe
• The four DORA metrics, and how to use them. (Lecture-05, slide 7)
Deployment freqency - how frequently you update software
lead time for changes - how long deos it take for an update
change-failure rate - out of how many attempts where those failures
time to restore - how long deos it take to recover from a failure
• Governance and compliance as code. (Lecture-05, slides 8 and 25)
Rules are enforeced thought CI
score on security observability and ownership
complience review. 
• The SDLC: what it is, its stages and milestones, the popular models. (Lecture-05, slides 11 to 17)
a team follows certain phases of implementaion to make software. uits shared actoss the whole team so they all work the same way.
to make projects consistant
to make proccess repeatable
make sure everyone is on the same page

Concept Commit: stakeholders give the go ahead
Execute Commit: decide on a delivery date
Design Review: The designers have inilizd the design of software, E2E, infastrucutre
Readiness Review: everyinew reviews the design and gives the go
Post project Assessment: Stakeholders verified software
Adoption Review: After project checkin

Waterfall
Sequential non interative design,
Agile
requirements and solutions cna shift and change as the project moves



• DevOps: principles and technologies. (Lecture-05, slides 22 and 23)

Cohesive teams: Sotring collaboration between buisness dev and testers
automate everything: Process must be repetable thouhgt automations
Strong source control: A storng version control for source code, infastrucutre, and everything. 
Task Early and frequent: Test everythign from the start
Improve Continously: Evaulate check in and improve

Agile approach, CI, C Testing, CD, collaborate to solve issues. 
automated delivery

• Scrum and Kanban: roles, events, boards, Kanban values. (Lecture-05, slides 26 to 34)
Agile, delivered highest buisness valude in the shortest amount of time. 
Prject is broken down into sprints and they are no more then a month
sprints are made up of tasks usually in the backlog
teams have a daily scrum meeting to check in and communicate 15 min. 

kanban values:
transparency: sharing info clearly
balance: different aspects, viewpoints must be balanced
collaboration: improve the way people work together
Customer Focus:alwasy improve things for the customer
Flow:work is continous
Leadership:leadership from all levels
Understanding:Well understanting of the product and the work
Agreement: everyone is on the same page
Respect: show considaration towards people

Kanban boads are to do, in progress, review, done
• Jenkins: pipelines, pipeline as code, plugins, build triggers, static analysis, test reports,SonarQube. (Lecture-05, slides 36 to 55)

Jenkins is an automation. CICD
automates testing and deployment after commit
notifications for porject
code analasys, reporting.

pipeline: 
Commit-> build-> test-> Stage-> Deploy

build trigger:
Manual build, periodic, build when SNAPSHOT, buidl after other projects, get notis
get a report for tests, covarage, compiler, style
Sonar cube is for inspecting code
• Continuous integration, continuous delivery, branching, environments, the deployment pipeline.
(Lecture-05, slides 58 to 72)
Deliver as freqently as possibel to get constant feedback from customers,find bugs earlier, get product out become comp. 
able to react more.
must have multiple enviroments 
follow CI

• GitHub Projects. (Lecture-05, slide 76)
Githubs project management
kanban style boards,
PR, Tasks, Issues. Used in agile devops and enterprise. single source of truth
has timelines. 