# CMPE 272 — Complete Midterm Study Guide

> **Primary sources:** the lecture slides for Sessions 1–7 and the Fall 2026 syllabus. The existing lecture `.md` files were used as searchable transcripts, but the PDFs were treated as authoritative. Slide references use the format **L4:S35** = Lecture 4, slide 35; syllabus references use **Syllabus:p3**.

## Navigation

- [What the instructor said about the midterm](#what-the-instructor-said-about-the-midterm)
- [Highest-priority review](#highest-priority-review)
- [A repeatable method for architecture scenarios](#a-repeatable-method-for-architecture-scenarios)
- [Session 1 — Enterprise architecture and Ansible](#session-1--enterprise-architecture-and-ansible)
- [Session 2A — OS, identity, storage, and configuration management](#session-2a--os-identity-storage-and-configuration-management)
- [Session 2B — Enterprise networking](#session-2b--enterprise-networking)
- [Session 3 — Frameworks, integration, APIs, and service mesh](#session-3--frameworks-integration-apis-and-service-mesh)
- [Session 4 — Microservices, resilience, scaling, and serverless](#session-4--microservices-resilience-scaling-and-serverless)
- [Session 5 — Platform engineering, SDLC, DevOps, and CI/CD](#session-5--platform-engineering-sdlc-devops-and-cicd)
- [Session 6 — ERP, CRM, and enterprise systems](#session-6--erp-crm-and-enterprise-systems)
- [Session 7 — Modeling, BPMN, messaging, and service composition](#session-7--modeling-bpmn-messaging-and-service-composition)
- [Must-know comparison tables](#must-know-comparison-tables)
- [Worked architecture scenarios](#worked-architecture-scenarios)
- [Practice questions](#practice-questions)
- [Answer key](#answer-key)
- [Last-minute checklist](#last-minute-checklist)
- [Source map](#source-map)

---

## What the instructor said about the midterm

### Confirmed directly by the slides

1. **The midterm covers Sessions 1–7.** (L7:S72)
2. **The exam is closed book and combines multiple-choice and short-answer questions.** (Syllabus:p3)
3. **The midterm is worth 10% of the course grade.** Grades are assigned on a curve, and the course offers no extra credit. (Syllabus:p3)
4. **Session 7 is on the exam**, with these topics explicitly named:
   - queue vs. topic;
   - at-least-once delivery and idempotency;
   - the transactional outbox pattern;
   - orchestration vs. choreography;
   - sagas. (L7:S72)
5. The Session 7 decision checklist says that **the midterm asks architecture questions about a scenario**. You should be able to select and defend a design, not merely recite definitions. (L7:S67)
6. The exam is in class after project abstract presentations: Section 49 on October 7 and Section 03 on October 13. The syllabus schedule independently confirms both dates. (L7:S70, S72; Syllabus:p6)

### Practical priority

Use this order if study time is limited:

1. **Session 7 messaging and service composition** — explicitly named by the instructor.
2. **Session 4 microservices and async reliability** — the foundation for the Session 7 scenarios.
3. **Session 3 integration patterns, APIs, and service mesh.**
4. **Sessions 5 and 6** — delivery lifecycle and core enterprise applications.
5. **Sessions 1 and 2** — infrastructure, automation, identity, storage, and networking foundations.

### What the closed-book format means for studying

- Memorize the **distinctions and decision rules**, not vendor trivia: queue/topic, sync/async, orchestration/choreography, SLI/SLO/SLA, ERP/CRM/SFA, block/file/object, and CI/continuous delivery.
- Practice definitions in one or two precise sentences for short-answer questions.
- For scenario questions, always state the choice, the reason, the failure mode it addresses, and the tradeoff it introduces.
- Reproduce the twelve-step architecture method below from memory; it provides a structure for longer short answers.
- Use the comparison tables for multiple-choice preparation, especially where two terms sound similar.

---

## Highest-priority review

You should be able to explain every item below without notes and apply it to a new scenario.

### 1. Queue vs. topic

- A **queue** is point-to-point: each message is processed by one consumer. Multiple workers on one queue compete and share the work.
- A **topic** is publish/subscribe: every subscriber receives the event.
- A common production design combines them: a topic fans out to one durable queue for each consuming service, and each service has a worker pool draining its queue.
- Use a queue when one kind of consumer must eventually do work. Use a topic when multiple independent consumers must learn that something happened. (L7:S50)

### 2. At-least-once means duplicates are normal

- **At most once:** messages may be lost but are not retried.
- **At least once:** the broker redelivers until acknowledgment; duplicates can occur.
- **Exactly once:** an end-to-end application effect is something the system must design, not a magic cross-system switch.
- A consumer must acknowledge **after** its side effect commits. Acknowledging first can lose work if the process crashes before the commit. (L7:S51)

### 3. Idempotency

An operation is idempotent when repeating it has the same final effect as doing it once.

- Give each command/event an idempotency key such as `paymentId`, `orderId + version`, or a producer-generated UUID.
- Store the key in the **same database transaction** as the business effect.
- On redelivery, detect the key and skip the repeated effect.
- Prefer `SET balance = 60` or an upsert over `balance = balance + 20`.
- In HTTP, GET, PUT, and DELETE are defined as idempotent; POST normally is not unless the application adds an idempotency key. (L4:S35, S41; L7:S52, S60)

### 4. Ordering

- Brokers normally guarantee ordering only **within a partition or message group**, not across the entire topic.
- Put messages that must stay ordered on the same key: order ID, account ID, or device ID.
- A poor key may create a hot partition; a single high-volume key cannot be spread across workers without weakening order.
- SQS FIFO uses a message-group ID; SQS Standard gives only best-effort ordering. (L7:S53)

### 5. Retries and dead-letter queues

- Retry transient failures with **exponential backoff and jitter**.
- Do not retry permanent validation failures.
- After a bounded number of attempts, move the message to a **dead-letter queue (DLQ)**.
- Alert on DLQ depth, preserve failure metadata, fix the consumer, and redrive safely.
- Redrive is safe only if the consumer is idempotent. (L4:S36; L7:S54)

### 6. Transactional outbox

The dual-write problem occurs when a service changes its database and publishes an event as two separate actions:

- database commits, publish fails → business state changed but no event;
- publish succeeds, database commit fails → event announces something that never happened.

The **outbox pattern** writes the business change and an outbox row in one local database transaction. A relay later publishes outbox rows, often by polling or change data capture (CDC/Debezium). The relay is still at-least-once, so consumers must remain idempotent. (L4:S37; L7:S55)

### 7. Orchestration vs. choreography

- **Orchestration:** one component owns the workflow and commands each step. The flow is visible and testable in one place, but the orchestrator must be protected and must not become a new monolith.
- **Choreography:** services react to events and emit new events. It is loosely coupled and easy to extend, but the end-to-end flow can become hard to see or debug.
- Use orchestration for a core transaction with an owner, deadline, or human task.
- Use choreography for peripheral side effects such as analytics, notifications, and search indexing.
- A common hybrid orchestrates the core and choreographs the edges. (L4:S22–S26; L7:S62)

### 8. Saga

A saga implements one business transaction as a sequence of local transactions across services.

- There is no global database rollback.
- On failure, run **compensating transactions** for already-committed steps, normally in reverse order.
- Compensation is a new business action, not time travel: refund payment, release inventory, or cancel shipment.
- Put irreversible steps last, or treat one as a pivot after which later steps must be guaranteed to finish.
- Give the saga an ID, timeout, durable state, and observable status. (L7:S63)

### 9. Scenario engine choice

- **Camunda 8:** BPMN-first; good for human tasks, timers, message correlation, and flows business users need to read.
- **Temporal:** code-first durable execution; good for developer-owned machine-to-machine workflows that may run for days or months.
- **AWS Step Functions:** JSON state machine; good for short AWS-native serverless orchestration.
- **No workflow engine:** use a topic and queues for pure fan-out. (L7:S64–S67)

---

## A repeatable method for architecture scenarios

When the exam gives a scenario, answer in this order:

1. **Name the business outcome and owner.** What must complete, who owns the flow, and is a user waiting?
2. **Separate synchronous from asynchronous work.** If the answer is required now, call synchronously. If work only needs to happen eventually, queue it.
3. **Choose queue or topic.** One worker group → queue. Several independent interested services → topic, usually feeding durable queues.
4. **State the delivery assumption.** Default to at-least-once.
5. **Make consumers idempotent.** Specify the key, unique constraint/processed-event record, and same-transaction rule.
6. **Choose an ordering key.** State what must remain sequential and why.
7. **Add reliability controls.** Timeouts, bounded retries, exponential backoff with jitter, DLQ, circuit breaker, concurrency limits, and backpressure.
8. **Solve database + broker consistency.** Use an outbox and relay/CDC.
9. **Choose orchestration or choreography.** Defend it using ownership, visibility, human steps, and coupling.
10. **If multiple services commit state, design a saga.** List each local transaction and its compensation.
11. **Choose the engine only if one is justified.** Camunda, Temporal, Step Functions, or none.
12. **Add observability.** Correlation ID, trace context, consumer lag, retry rate, DLQ depth, latency, and a status view.

That structure directly answers the kind of scenario question mentioned in L7:S67.

---

## Session 1 — Enterprise architecture and Ansible

### Enterprise applications

Enterprise applications commonly require:

- persistent data;
- concurrent access;
- multiple user interfaces/data representations;
- CI/CD;
- reliability, availability, scalability, and disaster recovery;
- integration, telemetry, instrumentation, and manageability;
- information security;
- authentication, authorization, and accounting/auditing (AAA). (L1:S17)

TOGAF defines an **enterprise** broadly as any collection of organizations with common goals: a company, division, department, government agency, or geographically distributed group. Enterprise applications include payroll, patient records, shipment tracking, credit scoring, insurance, supply-chain, accounting, CRM, and trading systems. (L1:S19–S20)

### Why enterprise architecture exists

Enterprise architecture reduces complexity and aligns business, data, applications, and technology. Expected benefits include:

- lower operating, development, support, and maintenance costs;
- greater organizational agility and application portability;
- better information management, security, reliability, and availability;
- easier component upgrades/replacement;
- reuse of current investments and lower risk for future ones.

Important frameworks include the **Zachman Framework** and **TOGAF**, including its Architecture Development Method (ADM), content framework, and capability framework. Frameworks provide domains, layers, views, matrices, and diagrams for documenting architecture. (L1:S21–S22, S70)

### Ansible essentials

**Ansible** automates provisioning, configuration management, application deployment, orchestration, and operational tasks. It connects through SSH, PowerShell, or APIs and is agentless. Its configuration is mostly YAML and should express desired state. (L1:S43–S46)

| Term | Meaning |
|---|---|
| Inventory | Hosts and groups Ansible manages, plus connection variables. |
| Module | Reusable unit of work such as `service`, `copy`, `template`, or `apt`. |
| Ad-hoc command | One module invocation without a playbook. |
| Task | One named unit of work in a play. |
| Play | Maps an ordered set of tasks to hosts. |
| Playbook | YAML file containing one or more plays. |
| Variable | Reusable YAML value referenced with `{{ ... }}`. |
| Fact | Information discovered from a managed host. |
| Handler | A task notified by changes; runs once near the end of the play. |
| Role | Standard reusable directory structure for tasks, handlers, templates, variables, and files. |

Key ideas:

- Modules should be **idempotent** and report whether they changed the target.
- Handlers avoid unnecessary restarts: many tasks may notify `restart apache`, but the handler runs once.
- `become: yes` enables privilege escalation; `become_user` names the target identity.
- Long tasks may run with `async` and `poll` rather than holding a connection indefinitely.
- Important magic variables include `hostvars`, `group_names`, and `groups`.
- Useful validation modes: `--check`, `--diff`, and `--syntax-check`.
- Roles are the main mechanism for modularization and reuse. (L1:S55–S65)

**Exam connection:** Ansible is an early example of infrastructure/configuration as code, declarative desired state, automation, repeatability, and idempotency—ideas that return in platform engineering and event consumers.

---

## Session 2A — OS, identity, storage, and configuration management

### Operating-system foundations

- OS categories include single/multitasking, single/multiuser, distributed, templated (VM/container image), lightweight, embedded, and real-time systems.
- Linux is a monolithic-kernel family; the slides contrast monolithic and microkernel approaches.
- `systemd` is a system/service manager that replaces many procedural init scripts with declarative unit files. It supports modular, asynchronous/concurrent service management and exposes a common interface.
- The **GPL** is a copyleft license: users may run, study, share, and modify software, but distributed derivative works must use the same license terms. MIT/BSD are permissive alternatives. (L2A:S4–S8)

### Load average

Linux load average reports average runnable or uninterruptible work over 1, 5, and 15 minutes. Interpret it relative to CPU capacity: a load near 4 on a four-core machine is very different from a load of 4 on a one-core machine. The slides identify `uptime`, `top`, and `/proc/loadavg` as sources. (L2A:S10)

### Identity and access

| Technology | Primary purpose | Key point |
|---|---|---|
| SAML | Federated authentication/authorization assertions | XML-based exchange between security domains; often enterprise SSO. |
| OAuth 2.x | Delegated authorization | Lets an application access resources without receiving the user's password. |
| OpenID Connect | Authentication on OAuth 2.0 | Adds an identity layer; OAuth alone is not an authentication protocol. |
| Identity provider (IdP) | Authenticates users for other applications | Returns an assertion/token to the relying application. Examples in slides: Okta, Auth0, OneLogin, Duo. |
| Active Directory | Microsoft directory and identity platform | Central users, computers, policy, authentication, authorization, and related services. |

Active Directory roles:

- **AD DS:** users, computers, domains, policies, domain controllers;
- **AD CS:** certificates and identities;
- **AD FS:** federation across boundaries;
- **AD RMS:** information-rights protection;
- **AD LDS:** lightweight directory services. (L2A:S12–S16)

### File systems and caching

- The **Virtual File System (VFS)** gives the kernel a common interface over concrete file systems such as ext4.
- VFS metadata includes the superblock, directory entry (dentry), and inode.
- An **inode** stores a file's metadata and pointers to data, but not its filename; directory contents map names to inodes.
- Storage optimization relies on RAM being faster than disk and sequential I/O being faster than random I/O.
- The **page cache** holds file-backed pages in RAM, prefetches reads, and absorbs writes. Dirty pages are later written back; `fsync()` requests a flush. (L2A:S18–S21)

### Storage choices

| Type   | Interface/model                                                       | Strength                              | Common use                                       |
| ------ | --------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------ |
| Block  | Raw fixed-size blocks; file system added by host; iSCSI/Fibre Channel | Low latency, high I/O, fine control   | Databases, VMs, transactional apps               |
| File   | Hierarchical files/directories; NFS/SMB/CIFS                          | Familiar sharing and file permissions | Shared documents, home directories, repositories |
| Object | Object + metadata + unique ID; HTTP/REST API; flat namespace          | Massive scale and rich metadata       | Cloud storage, backup/archive, media, analytics  |

An HDD uses rotating magnetic media. SSD/flash removes mechanical seek time but has different performance, durability, and cost characteristics. RAID combines physical disks into logical storage to improve redundancy, performance, or both; it is not itself a backup. (L2A:S22–S28)

### Configuration-management tools

- **Puppet:** declarative configuration language with client/server distribution.
- **Chef:** Ruby-based recipes and configuration management.
- **Ansible:** agentless YAML automation over existing transports.
- **Declarative** specifies the desired end state; **imperative** specifies the procedure/commands to reach it. Declarative tools improve repeatability and idempotency. (L2A:S29–S34)

---

## Session 2B — Enterprise networking

### QUIC

QUIC runs over UDP but implements connection management, reliability, ordering, congestion control, and encryption above it. Its important advantage is multiplexed streams without TCP connection-wide head-of-line blocking: loss on one stream does not stop every other stream. (L2B:S3–S4)

### Layer 2: VLANs, switching, and spanning tree

- A **VLAN** is a logical Layer-2 flooding domain spanning selected switch interfaces.
- A **trunk** carries multiple VLANs; each frame is associated with one VLAN.
- IEEE **802.1Q** inserts a four-byte tag containing a 12-bit VLAN ID, priority bits, and CFI. Untagged trunk traffic belongs to the native VLAN.
- A switch learns its MAC/CAM table from **source** MAC addresses and forwards using the **destination** MAC. An unknown destination causes unknown-unicast flooding.
- **STP** creates a loop-free logical tree and blocks redundant links; **RSTP (802.1w)** converges faster after a topology change. (L2B:S5–S12)

### Layer 3 and BGP

- An autonomous system (AS) is one administrative routing domain.
- **IGPs** route within an AS/enterprise: RIP, EIGRP, IS-IS, OSPF.
- **BGP** is the inter-domain EGP that connects autonomous systems.
- **eBGP** learns reachability from other ASes; **iBGP** distributes that reachability inside an AS.
- Enterprise connectivity ranges from single-homed to multihomed designs using different provider edges, customer edges, access technologies, or ISPs. More independence improves fault tolerance but raises routing and operational complexity. (L2B:S14–S22)

### Bandwidth billing

- **Committed Information Rate (CIR):** guaranteed purchased capacity, often hard-capped.
- **95th-percentile (P95) billing:** frequently sample traffic, sort samples, discard the highest 5%, and bill near the remaining peak. It permits occasional bursts without pricing every brief spike as permanent capacity. (L2B:S23–S24)

### Management, control, and data planes

- **Management plane:** configuration, policy, CLI/GUI, and administrative access.
- **Control plane:** routing/signaling logic; exchanges topology and builds routing tables.
- **Data/forwarding plane:** applies the resulting forwarding table to each passing frame/packet.

The control plane decides; the data plane forwards. (L2B:S26)

### Data-center topology

- Traditional designs and STP often select one best path and leave alternatives unused.
- A **Clos/leaf-spine** fabric provides many equal-cost paths and predictable east-west bandwidth.
- Leaf switches connect endpoints and every spine; leaves do not connect to leaves, and spines do not connect to spines in the basic design.
- Cisco ACI decouples endpoint identity from location and uses VXLAN tunnel endpoints plus a distributed mapping database. (L2B:S27–S30)

### NAT

- **Inside local:** inside host address as seen internally.
- **Inside global:** that inside host as represented externally.
- **Outside global:** outside host's actual external address.
- **Outside local:** outside host as represented internally.
- **Static NAT:** one fixed one-to-one mapping.
- **Dynamic NAT:** choose an address from a pool.
- **PAT/overload:** many inside hosts share one outside address by using different ports. (L2B:S31)

Wireshark captures frames through a packet-capture interface and decodes the link, network, transport, and application layers. (L2B:S32)

---

## Session 3 — Frameworks, integration, APIs, and service mesh

### Communication styles and API formats

Legacy/distributed communication examples include IPC/RPC, CORBA, Java RMI, XML-RPC/JSON-RPC, SOAP/WSDL/UDDI, Thrift, REST, and Protocol Buffers/gRPC. The important choice is the interaction contract, coupling, performance, and evolution—not simply which product is newest. (L3:S5–S11)

#### REST

REST constraints:

- client-server separation;
- stateless requests;
- cacheability;
- layered system;
- uniform interface;
- optional code-on-demand.

Desired properties include performance, scalability, simplicity, modifiability, visibility, portability, and reliability. Model resources as nouns and use HTTP semantics consistently. (L3:S7, S9, S94)

#### Protocol Buffers and gRPC

- Protocol Buffers define typed messages in `.proto` files and generate language-specific classes.
- They are compact binary serialization, typically smaller/faster than XML and less ambiguous than ad-hoc formats.
- gRPC uses Protobuf as an IDL/serialization format and HTTP/2 transport.
- It supports unary, server-streaming, client-streaming, and bidirectional-streaming calls.
- HTTP/2 supplies multiplexing and header compression. (L3:S10–S11)

### ESB, message bus, and message queue

An **Enterprise Service Bus (ESB)** mediates communication across heterogeneous applications. It can route, transform, and distribute work while hiding protocol/format differences. Advantages include interoperability and central policy; the architectural danger is moving too much business logic into centralized middleware. (L3:S12–S13, S51)

A **message bus** is shared messaging infrastructure. A **message queue** stores messages so a receiver can process them later, decoupling sender and receiver in time. (L3:S14)

### Enterprise Integration Patterns (EIP)

Know each family and the problem it solves:

| Family         | Important patterns                                                                                                                                                          |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Foundation     | Message, Message Channel, Pipes and Filters, Message Router, Message Translator, Message Endpoint                                                                           |
| Channels       | Point-to-Point, Publish-Subscribe, Dead-Letter Channel, Guaranteed Delivery, Message Bus                                                                                    |
| Construction   | Event Message, Request-Reply, Correlation Identifier, Return Address                                                                                                        |
| Routing        | Content-Based Router, Filter, Dynamic Router, Recipient List, Splitter, Aggregator, Resequencer, Scatter-Gather, Routing Slip, Throttler, Delayer, Load Balancer, Multicast |
| Transformation | Content Enricher, Content Filter, Claim Check, Normalizer, Sort, Validate                                                                                                   |
| Endpoints      | Event-Driven Consumer, Polling Consumer, Competing Consumers, Durable Subscriber, Idempotent Consumer, Transactional Client, Messaging Gateway, Service Activator           |

**Rider Auto Parts example:** FTP and HTTP endpoints feed one incoming-order channel. A content-based router distinguishes CSV from XML, translators convert both to a common POJO, and the normalized order enters the processing channel. This preserves legacy interfaces while standardizing the internal model. (L3:S28–S37)

### Framework concepts

- Java/Jakarta EE supplies APIs and runtimes for scalable, secure, multi-tier enterprise applications. Examples include Tomcat, GlassFish, WebLogic, WebSphere, WildFly, and Jetty.
- **Inversion of Control (IoC):** the framework controls the program flow and calls application-provided hooks.
- **Dependency Injection (DI):** the object's dependencies are provided externally through constructors, setters, or interfaces. DI is a common IoC technique that reduces hard-coded coupling. (L3:S23–S25, S39–S42)

### Event-driven architecture

- A producer detects a state change and publishes an event.
- A consumer subscribes and reacts.
- A broker routes events and decouples producers from consumers.
- Synchronous communication waits for a response; asynchronous communication lets processing happen independently. (L3:S43–S44)

#### Modern platforms

| Platform | Core model                                                                         | Best fit                                                           |
| -------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Kafka    | Partitioned durable append-only event log; topics, offsets, consumer groups        | Very high-throughput streaming, CDC, replay, event-driven services |
| Pulsar   | Brokers separated from BookKeeper storage; several subscription modes              | Multi-tenancy, geo-replication, combined queue/stream workloads    |
| Dapr     | Sidecar runtime with service invocation, pub/sub, state, actors, secrets, bindings | Portable, polyglot microservice building blocks                    |
| Temporal | Durable code-first workflows, activity workers, event-history replay               | Long-running reliable workflows and sagas                          |

Kafka provides per-partition order and replay. Consumer groups divide work; separate consumer groups independently read the same log. Pulsar emphasizes storage/compute separation and flexible subscriptions. Dapr standardizes APIs over pluggable back ends. Temporal persists workflow history and retries activities under policy. (L3:S46–S50)

### Service mesh

A service mesh is an infrastructure layer for managing service-to-service traffic. It externalizes cross-cutting communication behavior from application code.

Capabilities:

- discovery, logical routing, load balancing, traffic splitting, and canary releases;
- timeouts, retries, health checks, circuit breaking, and fault injection;
- mutual TLS, workload identity, and authorization policy;
- uniform metrics, logs, and distributed tracing. (L3:S60–S68)

Evolution described in the slides:

1. shared language-specific libraries (Hystrix/Finagle/Stubby);
2. per-node proxies such as early Linkerd;
3. lightweight sidecars and modern control planes such as Envoy + Istio, Linkerd 2, and newer sidecar-less/ambient models.

The **data plane** proxies carry traffic; the **control plane** distributes configuration and policy. A sidecar puts a proxy beside each workload. (L3:S69–S78)

AWS App Mesh terms: mesh, virtual service, virtual node, virtual router/route, and proxy. (L3:S80–S82)

### Contract-first APIs and OpenAPI

Contract-first means the API description is the product and source of truth; implementation follows it. Benefits include parallel development using mocks, consistent governance, fewer integration surprises, and automated generation/testing.

OpenAPI 3.1 should define paths/operations, JSON schemas, parameters, headers, security, errors, servers, examples, and reusable components.

HTTP/API rules from the slides:

- model nouns, not verbs: `/issues/{number}/comments`;
- creation: `201 Created` plus `Location`;
- update: `200` or `204`;
- client errors: `4xx`;
- paginate consistently and propagate `Link` headers;
- use idempotency keys for POST when required;
- use `ETag`/`If-Match` for safe conditional updates;
- use a consistent Problem Details error schema with a correlation ID;
- evolve additively; deprecate before removal; use compatibility checks in CI.

**OpenAPI is the specification; Swagger is a tooling ecosystem** such as Swagger UI and Swagger Editor. AsyncAPI describes asynchronous/evented interfaces. (L3:S92–S99)

---

## Session 4 — Microservices, resilience, scaling, and serverless

### Microservices: definition and tradeoff

A microservice architecture is a suite of small services, each in its own process, communicating through lightweight APIs. Services are organized around business capabilities and independently deployable with strong automation and minimal centralized management. (L4:S6–S10)

Key characteristics:

- one focused responsibility/high cohesion;
- autonomy and loose coupling;
- independent development, deployment, and scaling;
- technology and data-store heterogeneity;
- decentralized governance and data ownership;
- resilience, observability, and design for failure;
- replaceability and evolutionary design.

Benefits include strong module boundaries, independent deployment, team alignment, and technology diversity. Costs include network latency/failure, eventual consistency, distributed debugging, and operational complexity. The **microservice premium** means a simpler system may be better as a monolith or **modulith**—a modular monolith with strong internal boundaries. (L4:S7, S11–S15)

### SLI, SLO, SLA, and error budget

| Term         | Meaning                                  | Example                                                |
| ------------ | ---------------------------------------- | ------------------------------------------------------ |
| SLI          | Measured service behavior                | latency, error rate, throughput, availability          |
| SLO          | Target/range for an SLI                  | 99.9% availability; p95 latency below 120 ms           |
| SLA          | User-facing agreement with consequences  | service credit if availability falls below target      |
| Error budget | Allowed unreliability implied by the SLO | time/failures available for change and experimentation |

An SLI is evidence, an SLO is the internal target, and an SLA attaches consequences. (L4:S13)

### Synchronous and asynchronous architecture

- Synchronous request/response is simple and suitable when a caller needs fresh information immediately, but every hop adds latency and dependency failure can cascade.
- Asynchronous messaging buffers spikes, lets consumers scale independently, and decouples deployments, but introduces eventual consistency, duplicates, ordering concerns, DLQs, and harder tracing.
- Decentralized synchronous chains are brittle for changing workflows.
- A synchronous orchestrator can execute sequential or parallel calls but becomes a capacity and availability concern.
- Asynchronous choreography scales well for event-driven side effects.
- Asynchronous orchestration makes the flow explicit while still using durable messaging.
- Hybrid systems commonly use orchestration for explicit core steps and events for independent side effects. (L4:S14–S26, S32)

### Service boundaries and governance

Good boundaries have **loose coupling** (changing one service should not require changes to another) and **high cohesion** (behavior that changes together stays together). For each service, identify capability, owned aggregates, APIs/events, datastore, SLOs, team, deployment cadence, and dependencies. (L4:S28–S31)

Governance through code uses approved templates/exemplars to encode logging, monitoring, build, packaging, and deployment defaults. It should guide teams without turning a central architecture group into a ticket bottleneck.

### Three major failure modes

1. **Dependency brownout → timeout → cascading failure**
   - Symptoms: rising p95/p99 latency, timeout spikes, exhausted pools, open breakers.
   - Controls: strict deadlines, bounded retry budgets, exponential backoff/jitter, circuit breakers, graceful fallbacks, caching.
2. **Saturation/backpressure failure**
   - Symptoms: CPU/memory/file descriptors/DB connections exhausted, queue growth, 429/503, GC pauses.
   - Controls: bulkheads, bounded queues, concurrency/rate limits, load shedding, autoscaling on lag/depth, cell/AZ isolation.
3. **Contract/state correctness failure**
   - Symptoms: schema validation errors, silent truncation, post-deploy 4xx bursts, duplicates, ghost records, reordering bugs.
   - Controls: versioned schemas, registry and contract tests, idempotency keys, unique constraints, outbox, sagas, reconciliation. (L4:S30)

### Five-part async safety checklist

1. **Contract:** CloudEvents envelope plus JSON/Protobuf/Avro; versioned compatible schema in a registry.
2. **Delivery:** assume at-least-once; idempotent handlers; use aggregate ordering keys.
3. **Reliability:** bounded retry, exponential backoff with full jitter, DLQ, poison-message handling.
4. **State:** transactional outbox plus poller/CDC relay.
5. **Observability:** trace context, business correlation ID, publish/consume rate, end-to-end latency, lag, retries, DLQ depth, and alarms. (L4:S33–S38)

### Resilience patterns

- **Timeout/deadline:** stop waiting after a bounded time.
- **Circuit breaker:** after a failure threshold, fail fast rather than exhausting resources; later probe and close after recovery.
- **Bulkhead:** isolate pools/quotas so one failure cannot consume everything.
- **Rate limiting/load shedding:** reject excess work before collapse.
- **Retry budget:** retry only transient failures and limit multiplied load.
- **Idempotency:** makes safe retry possible.
- **Chaos testing/fault injection:** deliberately exercise failure paths. (L4:S39–S43)

### Scaling and traffic

- **Vertical scaling:** larger machine.
- **Horizontal scaling:** more instances.
- **Read scaling:** caches and read replicas.
- **Write scaling:** sharding by a key, with replication for durability.
- **CQRS:** separate command/write and query/read models; powerful but operationally complex.
- Caches may be client-side, proxy/CDN, or server-side (Redis/Memcached). (L4:S42, S46–S47)

AWS load-balancer distinctions in the slides:

- **ALB:** Layer 7 HTTP routing by host, path, method, headers, query, source, or port; can target Lambda.
- **NLB:** high-performance network-level traffic through listeners and target groups.
- **GWLB:** Layer-3 insertion/scaling of network appliances such as firewalls and IDS/IPS using GENEVE. (L4:S44–S45)

### Discovery, containers, orchestration, and mesh

Dynamic service discovery solves changing service locations. Registries include Consul, Eureka, and ZooKeeper; Kubernetes keeps DNS current through Services/CoreDNS.

A container is a process isolated by namespaces/cgroups with a filesystem image. An orchestrator such as Kubernetes/ECS places and restarts containers, scales replicas, routes traffic, and performs rollouts/rollbacks. Kubernetes concepts named in the slides: Pod, Deployment, Service, Ingress, ConfigMap, Secret, and Namespace. Controllers reconcile actual state to declared state. (L4:S48–S49)

A service mesh repays its cost when many services/languages need consistent mTLS, retries, traffic policy, and telemetry and a platform team owns it. It is usually excessive for a few services or a modulith. Start with an edge gateway plus resilience libraries and add a mesh when organizational/technical scale justifies it. (L4:S50–S51)

### Organizational costs

- **Conway's Law:** system architecture reflects organizational communication structure.
- **Inverse Conway maneuver:** shape teams to encourage the desired service boundaries.
- **Technical sprawl:** uncontrolled languages, libraries, pipelines, metrics, and deployment practices multiply operational cost. Platform standards should reduce accidental variety. (L4:S55–S56)

### Serverless

Serverless is an event-driven, on-demand execution model for short-running stateless code that scales automatically and bills at fine usage granularity. Events such as HTTP requests, uploads, queue messages, or timers trigger functions.

Good fits: APIs/microservices, mobile back ends, bots, inference, IoT, moderate stream processing, and service integration. Poor fits: long-running stateful computation, heavy simulations, deep-learning training, or workloads whose steady volume makes dedicated infrastructure simpler/cheaper.

The Prime Video example warns that distributed/serverless designs are not automatically optimal; one workload reportedly cut cost substantially by consolidating. Choose based on workload, not fashion. (L4:S58–S66)

---

## Session 5 — Platform engineering, SDLC, DevOps, and CI/CD

### Platform engineering

At enterprise scale, every team building a unique pipeline creates duplication. A platform team builds a **paved road/golden path** as an internal product.

An **Internal Developer Platform (IDP)** may provide a portal, service catalog, templates, environments on demand, and a prewired path from scaffold → repository → CI/CD → deployment → observability. Treat it as a product with users, a roadmap, and service expectations—not a ticket queue. (L5:S5–S6)

### DORA and governance

DORA metrics:

- deployment frequency;
- lead time for changes;
- change-failure rate;
- time to restore service.

Use them as system/team health signals, not individual targets. Goodhart's law warns that a metric stops being useful when it becomes the target. SPACE adds satisfaction, performance, activity, communication, and efficiency. (L5:S7)

Governance through code includes policy-as-code, production-readiness scorecards, security/ownership/observability checks, SBOMs, provenance, and automatically produced audit evidence. (L5:S8, S24)

### SDLC

The SDLC defines distinct phases and acts as a process agreement between stakeholders and IT. It creates common language, repeatability, consistent deliverables, early risk/ROI checks, and formal readiness decisions. (L5:S11–S16)

Core progression:

1. identify and assess;
2. requirements definition;
3. analysis;
4. design;
5. build and test;
6. production rollout;
7. support/adoption review.

Named milestones include Concept Commit, Execute Commit, Design Review, Readiness Review (go/no-go), Post-Project Assessment, and Adoption Review.

Models in the slides: Waterfall, Spiral, iterative/incremental, Agile, rapid prototyping, and synchronize-and-stabilize. Pick based on uncertainty, risk, feedback needs, and delivery constraints—not ritual. (L5:S15–S17)

### DevOps

DevOps combines development and operations responsibility through collaboration and automation across the complete release lifecycle. It breaks functional silos and aims for small, rapid, repeatable, reliable releases.

Principles:

- cohesive cross-functional teams;
- automate repeatable release work;
- strong source control for code, tests, configuration, and infrastructure;
- test early and often;
- continuously improve process, tools, metrics, and security. (L5:S19–S24)

### Scrum vs. Kanban

**Scrum:** prioritized product backlog, self-organizing team, timeboxed sprint, sprint planning/backlog, daily Scrum (15 minutes), and a tested integrated increment. Work overlaps across requirements, design, coding, and testing. (L5:S25–S28)

**Kanban:** visualize the workflow, pull work according to capacity, limit work in progress, and optimize continuous flow. The board is the single source of truth. Values include transparency, balance, collaboration, customer focus, flow, leadership, understanding, agreement, and respect. (L5:S29–S33)

### Jenkins and pipeline as code

Jenkins is an extensible automation server for building, testing, packaging, reporting, and deploying software. Plugins support SCM, build tools, triggers, test reports, static analysis, artifact repositories, notifications, and authorization.

- A **Jenkinsfile** stores the pipeline definition in source control.
- Triggers include manual runs, schedules, SCM polling, upstream jobs, and webhooks.
- Build quality signals include unit/integration tests, coverage, static analysis, warnings, and artifacts.
- Agents provide distributed/remote execution.
- SonarQube continuously inspects code quality and technical debt. (L5:S34–S54)

### CI, continuous delivery, and the deployment pipeline

- **Continuous Integration:** everyone integrates frequently—at least daily—and an automated build/test system gives fast feedback. It is a practice, not merely a tool.
- **Continuous Delivery:** keep software in a state that is always ready to release to production.
- **Continuous deployment** is the stronger automation practice in which validated changes are released without a manual release decision; the slides emphasize delivery readiness and button-driven deployment.
- The **deployment pipeline** is the heart of continuous delivery: automated build, unit/integration/acceptance/performance/security checks, artifact creation, environment promotion, feedback, and controlled approval/deployment. (L5:S56–S73)

Everything needed to reproduce the system belongs under configuration management: code, tests, configuration, build scripts, environment definitions, and documentation. Frequent trunk integration avoids long-lived merge risk; incomplete features can be released gradually or hidden behind a feature toggle. Environments should be reproducible as code. (L5:S64–S67)

GitHub Projects connects issues/PRs with boards, roadmaps, fields, automation, and delivery tracking, serving as a shared planning/execution view. (L5:S75–S77)

---

## Session 6 — ERP, CRM, and enterprise systems

### Enterprise systems and the silo problem

Functional organizations divide into purchasing, operations, warehouse, sales/marketing, R&D, finance/accounting, HR, and IT. The **silo effect** occurs when each department optimizes its own step without understanding the end-to-end process. Enterprise systems integrate processes that cross departments and geographic locations. (L6:S9–S14)

Major process families include procurement, production, fulfillment, product lifecycle, material planning, inventory/warehouse, asset/customer service, HCM, project management, financial accounting, and management accounting.

### Architectural progression

- **Client-server:** presentation, application/business logic, and data layers.
- **SOA:** self-contained black-box services representing business activities; services may compose other services.
- **ERP:** integrated intra-company and cross-functional processes over shared data. (L6:S15–S17)

### ERP

ERP consolidates enterprise planning, manufacturing, sales, marketing, finance, and related work into one integrated management system and shared database. It automates tasks in business processes. (L6:S19–S28)

Common modules/capabilities:

- finance: general ledger, accounts receivable, accounts payable;
- HR: administration, payroll, self-service;
- manufacturing/logistics: production planning, materials management, order processing, warehouse management;
- SCM, CRM, HRM, collaboration, content, BI, and identity capabilities.

Before ERP, departments maintain separate files and manually reconcile orders, inventory, purchasing, and accounting. After ERP, shared data links the process, improves visibility, and creates an audit trail.

#### Benefits and costs

Benefits:

- integrated system and single source of data;
- standardized processes/data and fewer duplicate entries/errors;
- end-to-end visibility, audit trails, better planning and inventory;
- faster fulfillment and financial reporting;
- configurable package modules and embedded practices.

Costs/risks:

- complexity, inflexibility, long implementation, and difficult configuration;
- standard practice may not fit a genuinely differentiating process;
- centralized access/security becomes complex;
- customization creates upgrade debt;
- a best-of-breed product may fit one function better. (L6:S31–S33)

### Clean core and replacement risk

Major platforms include SAP S/4HANA, Salesforce, Microsoft Dynamics 365/Power Platform, Oracle Fusion/NetSuite, and Workday. **Clean core** means keeping vendor internals close to standard and extending through supported APIs, events, and side-by-side platform applications. This avoids custom code welded into the core.

ERP replacement is hard because of data gravity, decades of process assumptions, organizational change, and cutover risk. A phased/strangler approach is often safer than a big-bang rip-and-replace. (L6:S5–S7)

### ERP data

- **Organizational data:** enterprise structure such as client, company code, sales area, or plant.
- **Master data:** durable shared entities such as customer/business partner, vendor, material, and pricing conditions.
- **Transactional data:** records produced while executing a process, such as a sales order, goods receipt, invoice, or payment.
- **Situational data:** what/when/how context such as date, time, and person.

Sales-order processing uses customer, material, and pricing master data plus configuration for routes/shipping points. The system validates entries, assigns identifiers, and links the order through delivery, goods issue, invoice, accounting, and payment. (L6:S37–S45)

### CRM and SFA

CRM manages the customer relationship across sales, marketing, service, interactions, history, preferences, and retention. It is both software and a customer-focused operating philosophy.

Core CRM activities include one-to-one marketing, call-center automation, Sales Force Automation (SFA), campaigns, contact management, and sales activity management.

**SFA** is a subset/component focused on sales execution: contacts, accounts, activities, opportunities, pipelines, and sometimes sales orders/partners. CRM is broader and includes customer profiles, communications, campaigns, commerce, service, and support. (L6:S35, S46–S56)

Customer relationship phases: prospecting → acquiring → servicing → retaining. Marketing automation triggers and measures messages/offers. Double opt-in requires the subscriber to submit and then confirm the subscription, reducing abuse; every message must allow unsubscribe. (L6:S52–S54)

Benefits include better satisfaction/retention, more efficient selling/service, consolidated customer data, targeted marketing, faster responses, and prediction of needs. CRM can route email, auto-reply, connect messages to customers/incidents, and support welcome, thank-you, reactivation, and cross-sell campaigns. (L6:S57–S59)

### Cloud vs. on-premises ERP/CRM

| Dimension | Cloud/SaaS | On-premises |
|---|---|---|
| Hosting | Vendor-managed | Organization's infrastructure |
| Cost | Subscription; lower initial capital | Licenses/hardware/implementation plus maintenance |
| Updates | Provider-managed | Organization-managed |
| Access | Internet-based and remote-friendly | Traditionally internal/controlled |
| Scale | Usually quicker elastic adjustment | Requires capacity planning/investment |
| Control/customization | Less direct control; vendor limits | More control and customization |
| Risk | Internet/vendor dependence, data concerns | Operational burden, slow deployment, upgrade cost |

A hybrid model places functions/data where control, cost, integration, and scalability requirements fit best. (L6:S60–S67)

### ERP implementation sequence

1. Define business objectives and measurable goals.
2. Select the appropriate ERP through fit assessment and pilots.
3. Form a cross-functional implementation team and empowered project leader.
4. Create timeline, milestones, resources, budget, and contingency plans.
5. Clean, map, and migrate data.
6. Configure/customize with key users while protecting the clean core.
7. Train users and manage organizational change.
8. Pilot test and incorporate feedback.
9. Deploy with integration, data, and transition support.
10. Monitor, support, and optimize.
11. Evaluate outcomes and refine over time. (L6:S68–S71)

The BlueFin exercise connects these ideas to order-to-cash, procure-to-pay, master-data quality, risks/controls, role access, and segregation of duties. (L6:S73–S74)

---

## Session 7 — Modeling, BPMN, messaging, and service composition

### UML essentials

UML is a standardized visual language for specifying, documenting, and communicating software design.

#### Multiplicity

- `0..1`: optional, at most one;
- `1`: exactly one;
- `0..*` or `*`: zero or more;
- `1..*`: one or more;
- `m..n`: at least m and at most n.

#### Relationships

- **Association:** general connection between objects/classes.
- **Aggregation:** weak whole-part; parts can exist independently of the whole.
- **Composition:** strong whole-part; a part's lifecycle depends on the whole.

#### Diagram types

- **Class diagram:** classes, attributes, operations, and relationships.
- **Use-case diagram:** actors and the system capabilities they need; good early scope discussion.
- **Activity diagram:** business or component workflow.
- **Sequence diagram:** time-ordered interactions among objects for one scenario. Frames use `opt` for optional paths, `alt` for alternatives, and `loop` for repetition.

Sequence diagrams remain useful because they are language-independent, collaborative, readable by non-coders, and omit implementation noise while showing many participants at once. (L7:S8–S19)

### ER diagrams

An Entity Relationship diagram documents data structure and becomes a basis for data-model implementation.

- **Cardinality:** maximum number of related instances.
- **Participation:** minimum number of related instances.
- **Primary key:** stable unique identifier for a row/entity.
- **Foreign key:** child-table attribute referencing the parent key.
- Crow's-foot notation represents one/many and optional/required relationships. (L7:S20–S24)

### BPM and BPMN

Business process modeling represents an enterprise process so it can be analyzed, simulated, improved, and automated. BPMN is the OMG/ISO standardized notation for Business Process Diagrams. (L7:S25–S29)

Key elements:

- **Pool:** boundary of one process/participant. A white-box pool shows the internal process; a black-box pool hides it.
- **Lane:** subdivision of a pool, usually a role, team, system, or phase.
- **Task:** atomic activity at the chosen modeling level.
- **Subprocess:** activity intentionally decomposed into lower-level elements.
- **Loop marker:** repeats the same activity while a condition holds.
- **Multi-instance marker:** creates several instances for different data/items, sequentially or in parallel.
- **Events:** start, intermediate, or end occurrences such as message, timer, error, or completion.
- **Exclusive gateway:** exactly one conditional path.
- **Inclusive gateway:** one or more conditional paths.
- **Parallel gateway:** all paths proceed concurrently; no condition selection.
- **Event-based gateway:** path is chosen by which event occurs.

Camunda 8 turns BPMN into executable orchestration using Zeebe. Operate shows running instances, Tasklist handles human work, Optimize provides analytics, Modeler builds diagrams, and connectors/workers integrate services. Workers subscribe to task types and complete jobs through gRPC/REST. (L7:S30–S46)

### Messaging — complete exam model

#### Why messaging

A synchronous call chain fails together and its latency is bounded by the slowest dependency. A queue decouples services in time, buffers bursts, and lets a temporarily unavailable consumer catch up. The tradeoff is that the caller receives no immediate business result.

Rule: **if the caller needs the answer to continue, call; if it only needs the work done eventually, queue.** (L7:S49)

#### Queue, topic, and durable fan-out

- Queue: one message → one consumer from a worker group.
- Topic: one event → every subscription.
- Durable fan-out: topic → separate queue for each service → competing workers within each service.
- Ask: how many kinds of consumer need the message, and must an offline consumer receive it later? (L7:S50)

#### Delivery, acknowledgment, and idempotency

Design for at-least-once. Commit business effect and processed key atomically, then acknowledge. Record the key and correlation ID in logs. A replay of yesterday's events against a database copy should not change final state; if it does, the handler is not idempotent. (L7:S51–S52, S60)

#### Retry/DLQ

Use bounded exponential backoff plus jitter, classify transient vs. permanent errors, move poison messages to a DLQ, alert, preserve metadata, repair, and redrive. Watch consumer lag and DLQ depth. (L7:S54, S60)

#### Outbox

Write business data and outbox event in one local transaction. A relay publishes later through polling or CDC. Use the aggregate ID as broker key when its events require stable ordering. Consumers still deduplicate. (L7:S55)

#### Kafka mental model

- Topic = set of partitions.
- Partition = ordered append-only disk log.
- Message = record with an offset.
- Consumer group = one logical subscriber whose members split partitions.
- Different groups read the same topic independently.
- Consumption does not delete messages; retention is time/size based.
- Compaction keeps the latest value per key.
- Replay begins again at an earlier offset. (L7:S56)

#### AWS messaging choices

| Service | Model | Use |
|---|---|---|
| SQS Standard | Queue; at-least-once; best-effort order; high throughput | Buffer work for one consumer type |
| SQS FIFO | Queue with message groups, ordering, deduplication within service boundaries | Ordered work per key/group |
| SNS | Pub/sub topic and fan-out | Deliver one event to multiple queues/Lambdas/endpoints |
| EventBridge | Content-routed event bus with rules, schemas, archive/replay | Cross-team/account/SaaS routing by event content |

Use references for large documents rather than placing very large payloads in messages. (L7:S57)

#### Event schemas and evolution

Treat a message schema like an API. Use Avro, Protobuf, or JSON Schema and register versions.

- backward compatible: new readers can read old messages;
- forward compatible: old readers can read new messages;
- full compatible: both.

Safest evolution is additive: optional fields, no semantic repurposing, no field renaming/retyping, and no reuse of serialized field numbers. Put event type and version in the envelope. (L7:S58)

#### Commands, events, CDC, and event sourcing

- A **command** asks a specific recipient to act and may be refused: `ReserveStock`. It normally goes to a queue.
- An **event** states an immutable past fact: `StockReserved`. It normally goes to a topic.
- **Event notification** carries minimal data and requires consumers to call back.
- **Event-carried state transfer** includes the data consumers need, improving autonomy at the cost of replicated/eventually consistent copies.
- **CDC** converts database commit-log changes into events; Debezium is a common tool.
- **Event sourcing** makes the event log itself the system of record. It is powerful but a major architectural commitment. (L7:S59)

### Service composition

#### Orchestration and choreography

Use orchestration for explicit owned workflows, deadlines, audit/status requirements, human tasks, and compensation. Use choreography for independent reactions that should not block the core. Avoid an orchestrator containing every business rule and avoid choreography with no traceable process state. (L7:S61–S62, S66)

#### Saga design recipe

1. List each service's local transaction.
2. List the compensation for every committed step.
3. Identify irreversible actions and place them last or after the pivot.
4. Persist saga state and ID.
5. Define timeouts and retry policy.
6. Make every command and compensation idempotent.
7. Expose current state for support and users. (L7:S63)

#### Workflow engine map

| Engine | Model | Strength | Limitation |
|---|---|---|---|
| Camunda 8 | BPMN + workers | Human tasks, analyst-readable flows, timers/messages/DMN | Requires BPMN/process-platform operations |
| Temporal | Workflow code + activity workers | Durable developer-owned flows, history/replay, long duration | No business-readable diagram as the source |
| Step Functions | JSON state machine | AWS-native serverless integrations and managed operations | AWS coupling; weaker outside AWS |

All provide durable state between steps, retry policy, and visibility into workflow instances. (L7:S64–S65)

#### Composition pitfalls

- **Distributed monolith:** synchronous services sharing a database; distributed cost without independence.
- **Stacked retries:** three layers × three retries can create 27 bottom-level attempts. Retry at one appropriate layer and set a top-level deadline.
- **Chatty flow:** many network calls to render one request; compose at the edge or carry needed state.
- **No correlation ID:** makes incident reconstruction nearly impossible.
- **God orchestrator:** central flow accumulates domain logic.
- **Invisible choreography:** nobody can answer “where is order 123?”
- **Raw CDC coupling:** consumers depend on producer-internal table structures. Publish a stable public event schema instead. (L7:S66)

---

## Must-know comparison tables

### REST vs. gRPC vs. asynchronous events

| Dimension | REST/HTTP | gRPC | Events/messages |
|---|---|---|---|
| Interaction | Request/response | Typed RPC and streaming | Asynchronous publish/consume |
| Typical format | JSON | Protobuf | JSON/Avro/Protobuf |
| Coupling | Caller knows endpoint/resource | Caller knows service contract | Producer need not know consumers |
| Best for | Public/business APIs, CRUD/resource models | Low-latency internal service calls | Decoupling, fan-out, buffering, audit/replay |
| Main risk | Chatty calls, weak contracts | Stronger platform/tool coupling | Eventual consistency, duplicates, order, operations |

### Queue vs. topic vs. event bus

| Need | Choose | Reason |
|---|---|---|
| One worker group must do a job | Queue | One message is consumed once logically by the group |
| Several services need the same fact | Topic | Fan-out to every subscription |
| Content-based routing across many teams/accounts | Event bus | Rules route different event shapes to destinations |
| Each interested service must survive downtime | Topic + durable queue per service | Fan-out plus independent retention/backpressure |

### Orchestration vs. choreography

| Question | Orchestration | Choreography |
|---|---|---|
| Where is the process? | Explicit in orchestrator/workflow | Distributed across event reactions |
| Visibility | Strong central status | Requires tracing/process view |
| Coupling | Services coupled to flow commands | Producers decoupled from subscribers |
| Extension | Change workflow | Add subscriber without changing producer |
| Risk | God orchestrator/single critical component | Untraceable emergent process |
| Best fit | Core transaction, human tasks, deadlines, saga | Notifications, analytics, indexing, optional reactions |

### Monolith, modulith, microservices, serverless

| Style | Advantage | Cost | Use when |
|---|---|---|---|
| Monolith | Simple deployment/debugging | Boundaries may erode; scale as one unit | Small/simple system or team |
| Modulith | Monolith simplicity with enforced modules | Requires disciplined internal design | Strong boundaries but distributed cost is unjustified |
| Microservices | Independent teams/deployments/scaling | Network failure, consistency, operations | Complexity/team scale repays the premium |
| Serverless | No server management, automatic event scaling, fine-grained billing | Limits, cold starts/platform coupling, poor long-stateful fit | Spiky short event-driven work |

### Scrum vs. Kanban

| Scrum | Kanban |
|---|---|
| Timeboxed sprints | Continuous flow |
| Sprint backlog and planned commitment | Pull work based on capacity |
| Defined ceremonies/roles | Visual board and explicit workflow |
| Increment at sprint end | Continuous delivery of completed items |
| Good for cadence and planning | Good for flow, support, and changing priority |

### ERP vs. CRM vs. SFA

| System | Focus |
|---|---|
| ERP | Integrated enterprise resources and cross-functional processes such as finance, production, purchasing, inventory, and HR |
| CRM | Full customer lifecycle across marketing, sales, service, interactions, and retention |
| SFA | Sales-execution subset: leads, accounts, contacts, activities, opportunities, pipelines |

---

## Worked architecture scenarios

### Scenario 1: Order, inventory, payment, and notifications

**Requirement:** Create an order, reserve inventory, charge payment, then send email and analytics. Inventory may be temporarily unavailable.

**Strong answer:**

1. Use an orchestrated saga for the core order → inventory → payment flow because it has one business outcome and needs explicit status/compensation.
2. Use idempotent commands keyed by order ID/payment ID.
3. Each service commits local state and an outbox row atomically; CDC/relay publishes results.
4. If payment fails after inventory reservation, compensate by releasing inventory. If a charge succeeded and a later reversible step fails, refund with a new idempotent transaction.
5. Publish `OrderCompleted` to a topic. Give email and analytics separate durable queues; these are choreographed edges and do not block the order.
6. Use bounded retry/backoff, DLQs, correlation/saga IDs, and a customer-visible status.

### Scenario 2: Three remote services; one is often down

**Requirement:** A project calls three systems and must keep working when one is unavailable.

**Strong answer:**

- If all three answers are needed immediately, use parallel synchronous calls with per-hop deadlines, circuit breakers, bulkheads, a top-level deadline, and a defined degraded response/cache.
- If some work only needs eventual completion, put that work on a queue. A consumer retries with backoff and DLQ while the main request continues.
- Do not stack retries in the client, gateway, mesh, and service.
- Measure dependency latency/timeouts, breaker state, backlog, lag, and DLQ depth.

### Scenario 3: Customer-created event has many consumers

**Requirement:** Loyalty, postal welcome pack, email, analytics, and search must react.

**Strong answer:** Publish a versioned `CustomerCreated` event to a topic. Give every consuming service its own durable queue and worker group. Write customer and outbox records atomically. Make every consumer idempotent and use customer ID as correlation/partition key where customer-local order matters. Use orchestration instead only if the customer is not considered created until mandatory steps complete.

### Scenario 4: Expense approval involving a manager

**Requirement:** A request waits up to five days for a manager, escalates, then calls finance.

**Strong answer:** Use Camunda/BPMN because a person acts inside a long-lived process and business stakeholders need a readable flow. Model user task, timer boundary/escalation, exclusive approval gateway, service task, errors, and end states. Persist a business key/correlation ID; make finance calls idempotent.

### Scenario 5: Duplicate payment request

**Requirement:** A network timeout causes the client to retry POST `/payments`.

**Strong answer:** Require an idempotency key. Store it under a unique constraint in the same transaction as the payment effect and saved response. Repeated calls return the original result rather than charging again. A timeout alone does not prove the original operation failed.

---

## Practice questions

The syllabus says the closed-book exam combines multiple-choice and short-answer questions. Try these without looking at the answers.

### Multiple choice

**MC1.** Three independent services must each receive `OrderCreated`, including after temporary downtime. Which topology best fits?

A. One shared queue with all three services competing  
B. A topic with one durable queue/subscription per service  
C. Three synchronous HTTP calls with unlimited retries  
D. One database table read directly by every service

**MC2.** A consumer commits a payment, crashes before acknowledging, and then receives the message again. Which property prevents a second charge?

A. Statelessness  
B. Horizontal scaling  
C. Idempotency  
D. Forward compatibility

**MC3.** Which ordering is safest for an at-least-once consumer?

A. Acknowledge, then commit the side effect  
B. Commit the side effect and processed key atomically, then acknowledge  
C. Acknowledge and commit in unrelated systems simultaneously  
D. Publish a new event before validating the message

**MC4.** What problem does a transactional outbox directly address?

A. Choosing between REST and gRPC  
B. Keeping a database change and its event record consistent  
C. Preventing every possible duplicate  
D. Encrypting messages in transit

**MC5.** Which design best fits email, analytics, and search indexing after an order completes?

A. Put them inside the critical synchronous transaction  
B. Choreograph them as independent reactions to an event  
C. Give them direct write access to the order database  
D. Use a distributed lock across all services

**MC6.** Which term is a target value for a measured service characteristic?

A. SLI  
B. SLO  
C. SLA  
D. Error log

**MC7.** Which statement best describes dependency injection?

A. The object constructs every dependency internally  
B. Dependencies are provided to the object from outside  
C. The network retries every failed call  
D. A broker copies an event to every subscriber

**MC8.** A switch receives a frame whose destination MAC is absent from its CAM table. What normally happens?

A. The frame is routed with BGP  
B. The switch performs unknown-unicast flooding within the VLAN  
C. The frame is translated with PAT  
D. STP creates a new VLAN

**MC9.** Which ERP data is a durable shared entity reused across transactions?

A. Situational data  
B. Master data  
C. A consumer offset  
D. A deployment artifact

**MC10.** Which BPMN gateway starts all outgoing paths without evaluating conditions?

A. Exclusive gateway  
B. Inclusive gateway  
C. Parallel gateway  
D. Event-based exclusive gateway

**MC11.** When is a service mesh most likely to repay its operational cost?

A. One small modulith maintained by one team  
B. Many polyglot services needing uniform mTLS, traffic policy, and telemetry, with a platform owner  
C. A static website with no service-to-service calls  
D. A single batch script run once per month

**MC12.** Which delivery guarantee should an application normally assume when consuming from SQS Standard or a typical broker subscription?

A. At most once  
B. At least once  
C. Global total ordering  
D. No duplicates under any failure

### Core recall

1. What exact session range does the midterm cover, and which Session 7 concepts did the instructor name?
2. Why is at-least-once delivery incompatible with a non-idempotent consumer?
3. Why must acknowledgment happen after the side effect commits?
4. What two inconsistent outcomes make up the dual-write problem?
5. How does the transactional outbox solve those outcomes, and what problem does it not eliminate?
6. When should you choose a queue, a topic, or a topic plus queues?
7. Why is exactly-once best described as an application effect across system boundaries?
8. How do partition keys provide order, and how can they reduce scalability?
9. Contrast orchestration and choreography using visibility, coupling, and failure handling.
10. What is a saga, and why is compensation not the same as rollback?
11. When would Camunda, Temporal, Step Functions, or no engine be most appropriate?
12. Define SLI, SLO, SLA, and error budget.
13. What are the three microservice failure-mode categories in Lecture 4?
14. What is the difference between a service mesh control plane and data plane?
15. Why can a modulith be better than microservices?
16. State the REST constraints listed in the slides.
17. Contrast REST, gRPC, and asynchronous event integration.
18. What is the difference between IoC and DI?
19. Name at least four Enterprise Integration Patterns and their purposes.
20. What is the difference between OpenAPI and Swagger?
21. What do an inode and a directory entry each contribute to file lookup?
22. Compare block, file, and object storage.
23. Distinguish SAML, OAuth, OIDC, and an IdP.
24. How does a switch learn its table, and what happens for an unknown destination MAC?
25. Contrast an IGP with BGP and eBGP with iBGP.
26. Contrast control and data planes.
27. Why is leaf-spine useful in a data center?
28. Contrast static NAT, dynamic NAT, and PAT.
29. What makes an Ansible handler different from an ordinary always-run task?
30. What is the difference between a variable, fact, and magic variable in Ansible?
31. What four DORA metrics are named in the slides?
32. Contrast CI and continuous delivery.
33. Contrast Scrum and Kanban.
34. Why should code, tests, configuration, environments, and documentation all be under configuration management?
35. Explain the silo effect and how ERP responds to it.
36. Contrast master, organizational, transactional, and situational ERP data.
37. Contrast ERP, CRM, and SFA.
38. Give two benefits and two risks of SaaS ERP compared with on-premises ERP.
39. Contrast UML association, aggregation, and composition.
40. Contrast BPMN pool, lane, task, subprocess, exclusive gateway, and parallel gateway.

### Scenario prompts

41. A metrics pipeline can tolerate losing an occasional sample but must be fast. Which delivery guarantee is reasonable?
42. A payment processor receives the same message twice. Describe the database transaction the consumer should execute.
43. Three subscribers need `OrderCreated`, but one is offline for two hours. Design the messaging topology.
44. A workflow calls three services, and each library plus the gateway retries three times. What failure pattern is likely, and how would you change it?
45. An ERP implementation has 20 years of inconsistent vendor records and many custom core modifications. Name the two major risks and a strategy for each.
46. A five-service system in one language is considering a service mesh. What questions determine whether the mesh is worth it?
47. A producer renames a required event field. What breaks, and what schema-evolution change is safer?
48. An order reserves inventory, charges a card, and books shipping. Shipping fails. Design the saga compensations and identify any potentially irreversible step.

---

## Answer key

### Multiple-choice answers

| Question | Answer | Why |
|---|---:|---|
| MC1 | B | A topic fans out; independent durable queues preserve each service's messages and backpressure. |
| MC2 | C | Redelivery is normal; the idempotency key makes the second execution have no additional effect. |
| MC3 | B | Atomic effect + dedup record followed by acknowledgment prevents both lost work and repeated effects. |
| MC4 | B | The business row and outbox event are committed in one local transaction. |
| MC5 | B | These are noncritical side effects that should not block the core order flow. |
| MC6 | B | The SLI is measured; the SLO is its target; an SLA attaches consequences. |
| MC7 | B | DI supplies dependencies externally and is a common implementation of IoC. |
| MC8 | B | Layer-2 switches learn sources and flood destinations they have not learned. |
| MC9 | B | Customers, vendors, materials, and pricing are long-lived master data. |
| MC10 | C | A parallel gateway creates simultaneous paths without conditional selection. |
| MC11 | B | Consistent cross-language policy at scale can justify a mesh when someone owns it. |
| MC12 | B | At-least-once means retries and possible duplicates; consumers must be idempotent. |

1. Sessions 1–7; queue vs. topic, at-least-once/idempotency, outbox, orchestration vs. choreography, and sagas.
2. Redelivery repeats the side effect—double charge, duplicate email, repeated increment, etc.
3. An ack before commit can lose work after a crash; ack after commit permits safe redelivery.
4. Commit succeeds/publish fails; publish succeeds/commit fails.
5. One local transaction records business state and event. A relay publishes later. It does not remove duplicates, so idempotent consumers remain necessary.
6. Queue for one worker group, topic for fan-out, topic plus durable queue per subscriber for fan-out with independent retention/backpressure.
7. Broker-level guarantees stop at boundaries; databases, external APIs, crashes, and retries still require deduplication/transactions.
8. Same key maps to one partition and preserves local order; a hot key bottlenecks one partition.
9. Orchestration centralizes visible flow but can centralize too much; choreography decouples subscribers but makes global state harder to observe.
10. Sequence of local transactions plus compensations; compensation is a new business action such as a refund, not reversal of history.
11. Camunda for BPMN/humans; Temporal for developer-owned durable code workflows; Step Functions for AWS glue; no engine for simple fan-out.
12. Measured signal; target; agreement with consequence; allowed unreliability.
13. Dependency/cascading failure; saturation/backpressure; contract/state correctness.
14. Data plane proxies carry/enforce traffic behavior; control plane distributes configuration/policy.
15. It keeps deployment/debugging simple while preserving modules; microservice complexity may not be repaid.
16. Client-server, stateless, cacheable, layered, uniform interface, optional code-on-demand.
17. REST: resource-oriented HTTP; gRPC: typed high-performance RPC/streams; events: asynchronous decoupled integration.
18. IoC means the framework owns flow; DI externally supplies an object's dependencies and is one way to implement IoC.
19. Examples: router selects destination, translator changes format, splitter divides, aggregator combines, resequencer restores order, idempotent consumer handles duplicates.
20. OpenAPI is the API description specification; Swagger is tooling around it.
21. Inode stores metadata/data pointers; directory entry maps a name to an inode.
22. Block: raw low-latency volumes; file: hierarchical shared files; object: API-addressed objects plus metadata at massive scale.
23. SAML exchanges XML identity assertions; OAuth delegates authorization; OIDC adds authentication to OAuth; an IdP performs authentication and issues assertions/tokens.
24. Learn source MAC/port; use destination MAC to forward; flood an unknown destination within the VLAN.
25. IGP routes within an AS; BGP between ASes. eBGP exchanges with external ASes; iBGP propagates BGP reachability internally.
26. Control plane builds routing state; data plane forwards each packet using it.
27. Many equal-cost paths, predictable scale, resilient east-west connectivity, better utilization than one STP-selected path.
28. Fixed one-to-one; mapping from pool; many-to-one using ports.
29. It runs only when notified by a changed task and normally once after the play's tasks.
30. Variable is supplied data; fact is discovered host data; magic variable is Ansible-reserved metadata such as `hostvars`/`groups`.
31. Deployment frequency, lead time, change-failure rate, time to restore.
32. CI frequently integrates and validates changes; continuous delivery keeps every validated change release-ready.
33. Scrum uses timeboxed sprints/ceremonies; Kanban uses pull, WIP limits, and continuous flow.
34. The system and pipeline must be reproducible, auditable, testable, and recoverable.
35. Departments optimize isolated work and lose the end-to-end view; ERP integrates cross-functional processes and shared data.
36. Org structure; durable entities; process records; event context.
37. ERP runs enterprise resources/processes; CRM covers full customer relationship; SFA is sales-execution functionality.
38. Benefits: lower initial cost, rapid deployment, accessibility, vendor updates, scale. Risks: recurring cost, vendor/Internet dependence, data/security concerns, limited customization.
39. General link; weak whole-part with independent lifecycle; strong whole-part with dependent lifecycle.
40. Process boundary; role/partition; atomic activity; decomposable activity; one conditional path; concurrent paths.
41. At most once may be acceptable for disposable samples.
42. Begin transaction; insert idempotency key under unique constraint; if new, apply payment and save result; commit; then ack. If duplicate, return/skip original result and ack.
43. Topic with one durable queue/subscription per subscriber; each queue has its own consumers and retention.
44. Retry amplification/storm (potentially 27 attempts at the bottom); retry at one layer with a budget/backoff and enforce an overall deadline.
45. Dirty master data → cleanse/deduplicate/map before migration. Customization debt → clean core and supported side-by-side/API/event extensions; phased strangler migration.
46. Number/languages of services, mTLS/audit need, inconsistent retry/timeout policy, progressive delivery, observability need, and whether a platform team owns the mesh versus its CPU/control-plane/debug cost.
47. Old consumers fail schema parsing/logic. Add an optional field, preserve old semantics, version/deprecate, and enforce compatibility in a registry/CI.
48. Release inventory and refund payment if shipping fails. A settled payment or external shipment can be difficult/irreversible; place irreversible work last or define a clear pivot and business resolution.

---

## Last-minute checklist

Before the exam, verify that you can do all of this from memory:

- [ ] Remember the official format: closed book, multiple choice plus short answer, worth 10%.
- [ ] State the confirmed Sessions 1–7 scope and the five explicitly named Session 7 topics.
- [ ] Draw queue, topic, and topic → per-service queue topologies.
- [ ] Explain at-least-once → duplicate → idempotency → ack-after-commit.
- [ ] Draw dual-write failure and the outbox solution.
- [ ] Design ordering keys, retry/backoff, and DLQ handling.
- [ ] Defend orchestration vs. choreography in a scenario.
- [ ] List a saga's steps and compensations.
- [ ] Choose Camunda vs. Temporal vs. Step Functions vs. no engine.
- [ ] Explain microservice benefits, premium, and three major failure modes.
- [ ] Distinguish REST, gRPC, event messaging, ESB, API gateway, and service mesh.
- [ ] Define SLI/SLO/SLA/error budget and core resilience patterns.
- [ ] Explain CI/CD, DORA, Scrum/Kanban, IDP/golden path, and pipeline as code.
- [ ] Explain ERP/CRM/SFA, ERP data types, cloud/on-prem tradeoffs, and clean core.
- [ ] Read basic UML/ER/BPMN notation.
- [ ] Review Ansible, identity, storage, VLAN/BGP/NAT, and control/data plane fundamentals.

---

## Source map

All sources are in this `Lectures` folder.

| Source | Authoritative PDF | Searchable transcript |
|---|---|---|
| Syllabus | `CMPE-272-03+49_FA26_syllabus_bond.pdf` | None |
| 1 | `Lecture-01_CMPE-272_Bond_FA26.pdf` | `Lecture-01_CMPE-272_Bond_FA26.md` |
| 2A | `Lecture-02a-SESSION_CMPE-272-Bond_FA26.pdf` | `Lecture-02a-SESSION_CMPE-272-Bond_FA26.md` |
| 2B | `Lecture-02b-SESSION_CMPE-272-Bond_FA26.pdf` | `Lecture-02b-SESSION_CMPE-272-Bond_FA26.md` |
| 3 | `Lecture-03_CMPE-272-Bond_FA26.pdf` | `Lecture-03_CMPE-272-Bond_FA26.md` |
| 4 | `Lecture-04_CMPE-272-Bond_FA26.pdf` | `Lecture-04_CMPE-272-Bond_FA26.md` |
| 5 | `Lecture-05_CMPE-272-Bond_FA26.pdf` | `Lecture-05_CMPE-272-Bond_FA26.md` |
| 6 | `Lecture-06_CMPE-272-Bond_FA26.pdf` | `Lecture-06_CMPE-272-Bond_FA26.md` |
| 7 | `Lecture-07_CMPE-272-Bond_FA26.pdf` | No Session 7 transcript was present; the PDF was read directly. |

### Slide locations for the instructor's midterm guidance

- Syllabus:p3 — closed-book multiple-choice and short-answer format; 10% weight; curved grading; no extra credit.
- Syllabus:p6 — Session 8 schedule: project abstract presentations plus in-class midterm on October 7/13 by section.
- L7:S67 — scenario-oriented decision checklist and statement that the midterm asks these questions about a scenario.
- L7:S70 — section dates for presentations and midterm.
- L7:S72 — Sessions 1–7 scope and explicitly emphasized Session 7 topics.
