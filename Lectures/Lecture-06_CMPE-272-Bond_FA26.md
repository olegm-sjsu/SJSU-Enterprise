# Lecture-06 CMPE-272-Bond FA26

Source: `Lecture-06_CMPE-272-Bond_FA26.pdf` (77 slides)

## Slide 1: CMPE-272

Enterprise Software Platforms

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: SAN · JOSE · STATE · UNIVERSITY · SJSU  

---

## Slide 2: Enterprise Software Platforms

Instructor: Andrew Bond

---

## Slide 3: IT News

- Dreamforce 2026, San Francisco, September 15 to 17. Salesforce presented the CRM as a place where AI agents do the work, not only a record of customers.
- AIforce: a layer that lets outside AI agents act inside Salesforce, through an API, MCP or a CLI, under Salesforce's own permissions.
- MCP security: integrations are scanned when an agent registers them and rated for prompt injection and tool poisoning.

- SAP, September 2: HARTING moves to the cloud with RISE with SAP. Mainstream maintenance for SAP ECC ends in 2027, so migrations like this one fill SAP's news this year.
- SAP, September 15: TabPFN-3.5 Plus, a prediction model for tabular data, is now available in SAP AI Core, so predictions run next to the ERP data.
- Tonight's question: when the ERP or CRM vendor ships the AI agent, who owns the business process, your team or the vendor?

---

## Slide 4: UNIT 5 · ENTERPRISE APPLICATIONS:

ERP, SCM AND CRM (WEEK 6)

---

## Slide 5: The Big Three Today

- SAP S/4HANA: in-memory ERP; RISE with SAP; ECC end-ofmaintenance (2027) is forcing migrations now
- Salesforce: CRM grown into a platform — Data Cloud, Agentforce, the AppExchange ecosystem
- Microsoft Dynamics 365 + Power Platform: ERP/CRM woven into M365 and Azure
- Also running the world: Oracle Fusion / NetSuite, Workday for HR and finance

---

## Slide 6: Extending Without Forking: the

Clean Core
- Customization debt is why ERP upgrades take years — modifications welded into the core
- Clean core: keep the vendor core vanilla; extend via platform layers (SAP BTP, Salesforce Platform, Power Platform)
- Extension points are the patterns you already know: events, APIs, side-by-side apps (Units 2 and 6)

---

## Slide 7: Why Replacing an ERP Is So Hard

- Data gravity: decades of transactions, master data, and process assumptions
- The processes ARE the org chart: Change the system and you change how people work
- Big-bang vs phased cutover: Hershey and Lidl as canonical failure case studies
- Realistic posture: strangler-fig around the edges; ripand-replace is rarely the answer

---

## Slide 8: INTRODUCTION TO ENTERPRISE

SYSTEMS

---

## Slide 9: Functional Structure

- 
- 

- 
- 

The most common enterprise structure you are likely to encounter is the Functional
Structure
Organizations that utilize a functional structure are divided into functions, or departments, each of which is responsible for a set of closely related activities
E.g., the accounting department sends and receives payments, and the warehouse receives and ships materials.
Typical functions or departments found in a modern organization include
- 
- 
- 
- 
- 
- 
- 
- 

Purchasing
Operations
Warehouse
Sales and marketing research and development finance and accounting human resources information systems

---

## Slide 10: Silo Effect

- People in the different functional areas came to perform their steps in the process in isolation, without fully understanding which steps happen before and which steps happen next
- They essentially complete their part of the process, hand it off to the next person, and then proceed to the next task
- By focusing so narrowly on their specific tasks, they lose sight of the “big picture” of the larger process, be it procurement, fulfillment, or any number of other common business processes
- This tendency is commonly referred to as the silo effect because workers complete their tasks in their functional “silos” without regard to the consequences for the other components in the process
- It becomes a major challenge for enterprises to coordinate activities among the different functional areas

---

## Slide 11: Enterprise Systems

- Business processes span different parts of an organization
- Various process steps are increasingly executed by groups in multiple locations throughout the world
- E.g., a bicycle manufacturer may purchase components from Italy, produce bicycles in Germany, and sell those bicycles in the United States
- Steps in business processes are performed in locations that are geographically dispersed, making it impossible to manage such processes effectively without the use of modern information systems
- Systems that support end-to-end processes are called Enterprise Systems (ES), and they are essential to the efficient and effective execution and management of business process

---

## Slide 12: Augmenting Human Intellect

(Groupware)
- By "augmenting human intellect" we mean increasing the capability of a man to approach a complex problem situation, to gain comprehension to suit his particular needs, and to derive solutions to problems.
- Application software designed to help people involved in a common task to achieve their goals http://www.dougengelbart.org/pubs/augment-3906.html http://nexus.awakentech.com:8080/at/awaken1.nsf/UNIDs/CFB70C1957A686E988256540 00699E1B?OpenDocument

---

## Slide 13: The Original Groupware

- IBM Notes (formerly Lotus Notes; see branding, below) and IBM Domino (formerly Lotus Domino[1]) are the client and server, respectively, of a collaborative client-server software platform marketed by IBM.

- Lotus Notes 8 Demo

---

## Slide 14: ENTERPRISE SYSTEMS

- Business Processes
- Procurement process (buy)
- Production process (make)
- Fulfillment process (sell)
- Lifecycle data management process (design)
- Material planning process (plan)
- Inventory and warehouse management (IWM) process (store)
- Asset management and customer service processes (service)
- Human capital management (HCM) processes (people)
- Project management processes (projects)
- Financial accounting (FI) processes (track–external )
- Management accounting or controlling (CO) processes (track– internal )

> **Text from slide image (OCR, may contain errors):**
>
> Functional Functional Functional  
> area area area  
> Step Step Step omy  

---

## Slide 15: Architectures: Client-Server

Layers:
- (1) how you interact with the application (Presentation)
- (2) what the application allows you to do (Application);
- (3) where the application stores your work (Data)

> **Text from slide image (OCR, may contain errors):**
>
> FOC  
> Client Client Client Client Client Client Client Client Client  
> Application eS  
> Application server Application server Application server  
> Data layer  
> Database server  

---

## Slide 16: Architectures: Service-Oriented

Architecture (SOA)
- Extension of Client-Server Architecture
- Integrate multiple client-server applications and create enterprise mash-ups, or composite applications Four properties of a Service 1. 2. 3. 4.

It logically represents a business activity with a specified outcome.
It is self-contained.
It is a black box for its consumers.
It may consist of other underlying services.[3]

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Monito · ij · Process · Orchestration  

---

## Slide 17: Architectures: ERP

- ERP systems focus primarily on intra-company processes—that is, the operations that are performed within an organization—and they integrate functional and cross-functional business processes

> **Text from slide image (OCR, may contain errors):**
>
> Finance Sales Materials Manufacturing Human Capital  
> Forecasting, Budgeting and Planning  
> IFRS Seni’ For’  
> Mobility Analytics Cloud Collaboration Workflow Reporting  

> **Text from slide image (OCR, may contain errors):**
>
> Tab/Mobile Dashboard Driven’ Private Cloud Interfacing with User Defined Parameterized  
> Device Access Analytics Hosting Facebook, Workflows Flexible Reporting  
> LinkedIn Twitter  

---

## Slide 18: ENTERPRISE RESOURCE PLANNING -ERP

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 19: What is ERP?

- The practice of consolidating an enterprise’s planning, manufacturing, sales and marketing efforts into one management system.1
- Combines all databases across departments into a single database that can be accessed by all employees.2
- ERP automates the tasks involved in performing a business process.1 Sources: 1. http://www.cio.com/summaries/enterprise/erp/index.html 2. CIO Enterprise Magazine, May 15, 1999.

---

## Slide 20: https://www.oracle.com/il-en/erp/gartnerproduct-centric-magic-quadrant/ https://www.elevatiq.com/post/top-erp-systems/

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Top · 10 · ERP · Systems · in · 2025 · Oracle · ud · Ms · Dynamics · 365 · NetSuite · infor · CloudSuite · LN/M3 · BC · Acumatica · Odoo · MARKET · PENETRATION · ©2025 · Inc. · All · rights · reserved. · ElevatlQ  

---

## Slide 21: How Do ERP Systems Work?

https://www.researchgate.net/figure/Functional-Architecture-of-an-ERP-product_fig1_220757076

> **Text from slide image (OCR, may contain errors):**
>
> Bussiness Planning Product Innovation  
> BusinessPlan Product Information  
> Sales  
> Master Planning  
> Master Plan Sales Order Ready  
> po/ Material Plan for Assembly Customer  
> Requirements Planning  
> Inquiries Assem-  
> Pur- Sales Invoiced  
> Subcontracting Material Plan bly Sales  
> chase Boon Order  
> Progress roduction  
> FAS Order Packing and  
> Production Orders/ schedules shipping order  
> Warehousing  
> Received Picking Picking Shipment  
> Goods List List order  
> Receipt Component Packing  
> Goods Manufact. Assembly Shipping  

---

## Slide 22: ERP Components

- 

Finance: modules for bookkeeping and making sure the bills are paid on time.
Examples:
- General ledger
- Accounts receivable
- Accounts payable

- 

HR: software for handling personnelrelated tasks for corporate managers and individual employees. Examples:
- HR administration
- Payroll
- Self-service HR

- 

Manufacturing and Logistics: A group of applications for planning production, taking orders and delivering products to the customer.
Examples:
- 
- 
- 
- 

Production planning
Materials management
Order entry and processing
Warehouse management

Source: http://www.computerworld.com/printthis/1998/0,4814,43432,00.html

---

## Slide 23: Modules of ERP systems

- Enterprise Resource Planning (ERP) Systems:

- Software packages that can be used for the core systems necessary to support enterprise systems.
- SCM
- CRM
- HRM
- Collaboration
- Content Management
- Business Intelligence
- Identity Management

---

## Slide 24: ENTERPRISE RESOURCE PLANNING

> **Text from slide image (OCR, may contain errors):**
>
> Sales and Marketing Operations and Logistics  

---

## Slide 25: An ERP Example: Before ERP

Orders
Parts

Sends report

Sales Dept.

Customer
Demographic
Files

Customers

Checks for Parts
Calls back “Not in stock”
“We ordered the parts”

Accounting
Files

Accounting
Sends report

Sends report

Invoices accounting

Ships parts

Vendor
Order is placed with Vendor
Purchasing
Files

Purchasing

Warehouse

“We Need parts #XX”

“We ordered the parts”

Inventory
Files

http://www.umsl.edu/~lacitym/eveerpf2.ppt

---

## Slide 26: An ERP Example: After ERP

Orders
Parts

Sales Dept.

Customers

Inventory Data
If no parts, order is placed through DB

Accounting
Financial Data exchange;
Books invoice against PO

Order is submitted to Purchasing.
Purchasing record order in DB

Database

Books inventory against PO

Order is placed with Vendor

Warehouse

Vendor

Purchasing
Ships parts
And invoices accounting

http://www.umsl.edu/~lacitym/eveerpf2.ppt

---

## Slide 27: ERP

- Attempts to integrate everything
- CRM drives what SCM will produce
- Everyone works together in e-collaboration
- The entire organization knows the entire organization

- Think about your school
- Can you register for class with a bill outstanding?
- Can you register for a class for which you haven’t completed the prerequisite?

---

## Slide 28: ERP Integrates Everything

> **Text from slide image (OCR, may contain errors):**
>
> Finance  
> Sales  
> Manufacturing  
> Customers en Suppliers  
> Enterprise System  
> Inventory  
> Human Resources  

---

## Slide 29: SD Audit Trail for Completion of Steps in the SAP Sales Process

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Document · Quotation · 0020000019 · Completed · Standard · Order · 0000012071 · Delivery · 0080015185 · (Schedule · delivery) · WMS · transfer · order · 0000001511 · (Picking · ticket) · 9/22/2007 · GD · goods · 4900035532 · (Shipment) · complete · Invoice · (F2) · Accounting · dacument · 1400000000 · Cleared  

---

## Slide 30: Audit Trail for Completion of Steps in the SAP Purchase Process

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Standard · PO · Yendor · GPSRUS-999 · Doc. · date · Header · (Purchase · order) · Overview · GPS · Guidance · System-999 · Material · Data · Delivery · Schedule · Invoice · Conditions · Purchase · Order · History · Texts · Amountin · cost · quantity) · WWE · 5000011991 · 15 · 40,500.00 · Goods · receipt · EA · USD · RE-L · (Goods · receipt) · (Vendor · invoice)  

---

## Slide 31: Pros of Enterprise Systems

> **Text from slide image (OCR, may contain errors):**
>
> Single database  
> Integrated system capability to determine ATP)  
> Process orientation (versus function orientation)  
> Standardization of business processes and data, easier to understand across the organization  
> Faster business processes customer fulfillment, product development)  
> Timely information  
> Better financial management (partly due to integration)  
> One face to the customer  
> Optimal inventory levels  
> Improved cash management  
> Productivity improvements, reduced personnel expense  
> financial disclosures  
> Improved budgeting, forecasting, and decision support  
> Seamless integration and accessibility of information across the organization  
> Catalyst for reengineering old, inefficient business processes  

---

## Slide 32: Pros of ERP Packages

> **Text from slide image (OCR, may contain errors):**
>
> One package across many functions (if one ERP)  
> “Best practices”  
> Modular structure (buy what you need)  
> No development needed (unless modifications are required)  
> Configurable  
> Reduced errors business rules, enter data once)  

---

## Slide 33: Cons of Enterprise Systems and ERP

Packages

> **Text from slide image (OCR, may contain errors):**
>
> Centralized control versus decentralized empowerment  
> Inability to support traditional business processes that may be best practices for that organization  
> Loss of flexibility in rapidly adapting to desired new business processes in the post-implementation period  
> Increased complexity of maintaining security, control, and access permissions for specific information embedded  
> in central database  
> The rigidity of “standardization” can impede creative thinking related to ongoing business process improvements  
> Cons of ERP Packages  
> Complex and inflexible  
> Best practices are shared by all who buy  
> Difficult to configure  
> Long implementation  
> Best of breed might be better (than single ERP package)  
> Can't meet all needs developed for many user types)  

---

## Slide 34: CRM

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 35: Customer Relationship Management

(CRM) Systems
- Customer relationship management (CRM) systems, sometimes called e-CRM systems, use technology to help an e-business manage its customer base
- CRM allows an e-business to match customer needs with product plans and offerings, remind customers of service requirements, and determine what products a customer has purchased

---

## Slide 36: CRM and Marketing Management

 Marketing resource and marketing management

- Manage and optimize the use of marketing resources including budgets, people, time, and assets.
- Align all activities and resources around strategic marketing goals.
- Gain visibility and control into your marketing processes.
- Accurately manage the marketing budgets and costs.
- Increase brand awareness with proper usage and consistency across enterprise and third-party agencies.
- Facilitate collaboration among team members and coordinate marketing activities across the enterprise.

---

## Slide 37: Data Elements in SAP ERP

Today we will discuss
- How data is managed in SAP ERP?
- Understanding the components of creating a sales order in ERP.
- Understanding the steps involved in creating the standard order in SAP ERP.
- The overall order management process in ERP.
- Importance of CRM in ERP Systems.

---

## Slide 38: Definitions

- 

SAP S/4HANA — “SAP Business Suite 4 SAP HANA,” SAP’s current ERP built on the in-memory
HANA database (High-Performance Analytic Appliance)
BP — Business Partner (the unified master record for customers/vendors)
MM — Materials Management
PP — Production Planning
SD — Sales and Distribution
FI — Financial Accounting
AR — Accounts Receivable (often written FI/AR when referring to FI’s A/R subledger)
AP — Accounts Payable
WM — Warehouse Management
EWM — Extended Warehouse Management
MRP — Material Requirements Planning
SKU — Stock Keeping Unit (a product identifier)
UoM — Unit of Measure
GR/IR — Goods Receipt/Invoice Receipt (clearing account that reconciles received goods with supplier invoices)
VAT — Value-Added Tax
MDG — Master Data Governance (workflow/governance for master data)
Price control “S/V” — S = Standard price; V = Moving-average price

---

## Slide 39: Master Data

Long-term data represent entities associated with various processes
- Customer
- Vendor
- Material

Centrally stored and is processed to eliminate data redundancy.
Typically includes
- General Data (across company’s code)
- Financial Data
- Area-Specific Data

---

## Slide 40: Transactional Data

Data generated during execution of a process is termed as transactional data.
It requires
- Organizational Data
- Master Data
- Situational Data (What, when and how is it happening?)

Example: Sales Order Creation
- Organizational elements:
- 
- 
- 

Client,
Company Code
Sales Area

- Master Data
- 
- 

Customer
Material

- Situational Data (What, when and how is it happening?)
- 
- 
- 

Date
Time
Person

---

## Slide 41: Example of SAP ERP Data

> **Text from slide image (OCR, may contain errors):**
>
> Customer  
> Material  
> Client Who  
> Company code «When  
> Plant Where  

---

## Slide 42: Creating Order in ERP

The three types of master data critical to sales order processing
1. Customer – Shared with Financial Module
2. Material – Shared with Material Management and
Production Planning
3. Pricing

> **Text from slide image (OCR, may contain errors):**
>
> Sold-to party 2540-00  
> Item Material Quantity  
> Material Master 1400-100-00 20  

---

## Slide 43: Creating Order in ERP

When sales order is created
1. Customer Master
2. Material Master
3. Condition records for Pricing
4. Tables in Configuration for shipping point and route
Data can also be manipulated from an inquiry or quote.

---

## Slide 44: Standard Order in SAP ERP

Task is completed by
1.Order entry screen in SAP ERP’s Enterprise
System
2.A unique number is assigned by the company to each customer
3.For most data entry fields, SAP ERP determines whether an entry is valid

---

## Slide 45: Order Management Process

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Contact · Inquiry · Scheduling · Contract · Quotation · agreement · Goods · issue · ransfer · Order · Shipment · aterial · Stock · nts · Receivab · Account  

---

## Slide 46: What is CRM?

- CRM stands for Customer Relationship Management.
- It is a software system that is used to effectively manage the
- sales process,
- track customer interactions,
- store information about customers (including purchase history, revenue generated, up-selling and cross-selling opportunities, etc.), and
- ultimately strengthen relations with customers.

- CRM, however, is not just about software systems. It is a philosophy for interacting with your clients to make sure that they are happy and that they keep coming back to use your products and services.

---

## Slide 47: CRM Sales Management Functionality

A CRM system supports your sales team at every stage of the sales cycle, from leads to customer management.
Below are a few use cases:
- View and manage account activity and communications
- Use reports to forecast sales, measure business activity, identify trends
- Qualify leads and track prospective customers
- Centralize customer data
- Access, update, and share information across teams and departments.

---

## Slide 48: Core Activities of CRM

The core activities of CRM system may include:
- One-to-One Marketing
- Call Center Automation
- Sales Force Automation (SFA)
- Sales Campaign Management
- Contact Management Tool
- Sales Activity Manager

---

## Slide 49: Key components of a successful CRM

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 50: SAP CRM System

- SAP’s Business Warehouse: It is a system for reporting and analyzing transactional data relationship with the customer.
- Advanced Planner and Optimizer (APO): It is a system that supports efficient planning of the supply chain SAP’s view of CRM to provide a set of tools to manage the three basic task areas: 1. Marketing, 2. Sales, and 3. Service.

---

## Slide 51: SAP CRM System

_(Slide is title-only or image-only with no readable text.)_

---

## Slide 52: Marketing Automation

- Marketing Automation It can be described as event-based trigger marketing that is used to launch messaging and offer presentations to customers at particular points in time. CRM helps not only trigger the communications, but also measure the results.

---

## Slide 53: Double Opt-in

The double opt-in process implies that a subscriber fills out your signup form first and then confirms subscription to your list. In other words, the double opt-in works as follows:
1. A prospect signs up to receive emails via your website, at a tradeshow etc.
2. You send a confirmation email to him/her asking them to click on a link that confirms that they have opted to subscribe to your messages.
3. You get the double opt-in permission from prospects.
- This eliminates the chance of abuse where somebody submits somebody else’s email address without their knowledge or against their will.
- Note that every communication you send must have the option for the contact to unsubscribe at any time.

---

## Slide 54: SAP CRM System

Four phases of the cultivation of the customer relationship:
1. Prospecting,
2. Acquiring,
3. Servicing,
4. Retaining

> **Text from slide image (OCR, may contain errors):**
>
> Marketing and campaign Target group creation  
> planning Modeling  
> py Segment creation  
> Selection  
> Monitoring  
> Campaign analysis  
> Phone Web Mobile Email Success  
> measurement  
> Campaign execution Third-party data  
> activity management Profiles  

---

## Slide 55: Key Differences between CRM and SFA

- From a software perspective, SFA (Sales Force Automation) often refers to a primary component of CRM.
- SFA is typically used by sales people and managers and covers functions such as
- contact management,
- account management,
- activity management and
- opportunity management.

- Sometimes SFA systems also include capabilities such as
- sales order processing,
- Partner Relationship Management (PRM), etc.

---

## Slide 56: Key Differences between CRM and

SFA

> **Text from slide image (OCR, may contain errors):**
>
> Providing actionable goals and Customer profiling including  
> targets for each sales team purchasing history, behavior  
> member data, demographics and more.  
> Recording cold calls and lead Customer communications  
> generation activities tracking  
> Storing contact information Storing account data and  
> commerce transactions.  
> Scheduling and tracking  
> appointments Tracking responses to sales and  
> marketing campaigns  
> Managing pipelines,  
> opportunities, and workflows Monitoring service and support  
> interactions  

---

## Slide 57: Benefits of CRM System

- A CRM system can help you
- recognize prospective customers,
- learn more about current customers,
- understand their preferences,
- frequently anticipate their needs and respond to their requests quickly and effectively.

- In other words, with a CRM system, you can track, organize, and consolidate your interactions with clients. Note: When should I start tracking my customers' activities? This is best to start doing before they actually become your customers. This will help you maximize the ROI and retain each customer.

---

## Slide 58: Benefits of CRM for Businesses

With a CRM system, your organization will be able to improve productivity, reach out to more prospects and close more sales. CRM can help you:
- Raise customer satisfaction
- Increase customer retention
- Reduce marketing expenses
- Anticipate customer needs and preferences
- Increase operating efficiencies
- Improve targeted marketing efforts of customers and prospects
- Provide quicker service to customers. Note: Is CRM required for small business with limited customers? CRM software can benefit small businesses by consolidating customer data into a single system. As your business grows, keeping a record of all transactions can become very challenging. CRM will allow you to manage customer interactions more efficiently, so you have more time to focus on your service or product.

---

## Slide 59: E-mail Management through CRM

- 

CRM software may provide workflow-enabled email processing capabilities.
- 
- 
- 
- 
- 

- 

It can retrieve emails sent from your customers, automatically route them to appropriate users based on workflow rules, send auto replies back to your customers, automatically associate emails with incidents and customers, manage multiple attachments in emails, etc.

Examples of Automated Messages:

- Automated welcome messages to new customers, personalized with their most recent transactions
- Thank-you messages to recognize your customers' activities
- Lapsed messages with an irresistible offer to re-activate former highly valuable customers
- Cross-sell messages based on previous purchases
- Run marketing campaigns that rely on repeated contact or several 'touches' with potential customers (ideal for high-value products with a long sales cycle).

---

## Slide 60: Difference between on-premise and cloud-based CRM solutions

- 

What is “cloud”?
The 'cloud' is a popular word for using the Internet to access data, stored on remote servers, i.e. like somewhere in the cloud. The cloud makes it convenient to get at information and services from anywhere.

- 

Difference between on-premise and cloud-based CRM solutions.

- As the name suggests, on-premise CRM software is run on computers within the premises of an organization.
- In this case all the data and information is stored inside the premises of the company, too.
- In recent years there has been a steady growth in the popularity of web-based solutions.
- Cloud-based software implies that the software and all relevant data, is accessible through the Internet and is displayed in a web browser.
- According to Gartner, 35% of all CRM implementations today use SaaS, growing to over 50% by 2020.

---

## Slide 61: Cloud Based CRM

Salesforce Demo: https://www.youtube.com/watch?v=A7AEc-B2PKQ (3 mins)

---

## Slide 62: Major CRM

Vendors

> **Text from slide image (OCR, may contain errors):**
>
> Figure Magic Quadrant for the CRM Customer Engagement Center  
> CHALLENGERS LEADERS  
> Salesforce  
> Microsoft Pegasystems  
> ServiceNow.  
> Zendesk  
> Oracle  
> Verint Freshworks  
> Appian  
> Creatio  
> Zoho  
> SugarCRM eGain  
> Cherwell CRMNEXT  
> NICHE PLAYERS VISIONARIES  
> COMPLETENESS OF VISION As of May 2021 Gartner, Inc  
> Source: Gartner (June 2021)  

---

## Slide 63: Cloud Based ERP Solutions

- Choosing between cloud-based (SaaS) and onpremises ERP solutions is a critical decision for organizations.
- Each approach has its own set of advantages and disadvantages.
- Additionally, some organizations opt for hybrid solutions that combine elements of both.

---

## Slide 64: Cloud-Based (SaaS) ERP:

- Deployment: Cloud ERP is hosted and maintained by a third-party provider, and users access it through the internet.
- Cost Structure: Typically, cloud ERP is subscription-based, with ongoing monthly or annual fees.
- Accessibility: Users can access the system from anywhere with an internet connection, facilitating remote work and collaboration.
- Updates and Maintenance: The provider is responsible for updates, maintenance, and security patches.
- Scalability: Cloud ERP solutions are often more scalable, allowing organizations to adjust resources as needed.

---

## Slide 65: vs. On-Premises ERP:

- Deployment: On-premises ERP is installed and maintained on an organization's own servers and infrastructure.
- Cost Structure: Initial costs include software licenses, hardware, and implementation. Ongoing costs involve maintenance and support.
- Control: Organizations have full control over their ERP environment, which may be essential for compliance and customization.
- Accessibility: Access is typically limited to the organization's premises, which can hinder remote work.
- Updates and Maintenance: Organizations are responsible for managing updates, maintenance, and security measures.
- Scalability: Scalability may be more complex and require additional investments in hardware and resources.

---

## Slide 66: Pros and Cons

Cloud-Based (SaaS) ERP:
- Pros: Lower initial costs, accessible, rapid deployment, scalability, automatic updates – think of the flexibility of Amazon Prime Video.
- Cons: Ongoing costs, potential security concerns, limited customization, internet reliance – similar to the limitations of streaming services. On-Premises ERP:
- Pros: Complete control, high customization, more control over data security, predictable costs – akin to owning a vast library of DVDs.
- Cons: High initial costs, slower deployment, maintenance responsibility, limited remote access – like the challenges of managing a physical media collection.

---

## Slide 67: Hybrid Solutions

- Flexibility: Choose where data resides, similar to how Amazon combines online and physical retail strategies.
- Cost-Effectiveness: Utilize cloud resources for specific functions.
- Integration: Blend on-premises and cloud systems.
- Scalability: Adapt to changing needs.

---

## Slide 68: How to implement ERP

1. Define Objectives and Goals:
- Conduct a thorough needs analysis to understand the specific challenges and opportunities within your organization.
- Establish clear, measurable goals for the ERP implementation, aligning with overall business objectives. 2. Choose the Right ERP System:
- Perform a comprehensive assessment of various ERP solutions to identify one that best fits your business requirements.
- Engage with multiple vendors, request demonstrations, and conduct pilot tests to evaluate the functionality and user-friendliness of the systems. 3. Form an Implementation Team:
- Assemble a cross-functional team comprising members from various departments like IT, finance, HR, and operations.
- Appoint a skilled project manager to lead the implementation, ensuring they have the authority and resources to make key decisions.

---

## Slide 69: How to implement ERP

4. Develop a Detailed Plan:
- Outline a detailed implementation timeline, including major milestones and deadlines.
- Allocate necessary resources, including personnel, technology, and budget, for each phase of the project.
- Include contingency plans to address potential delays or challenges. 5. Data Migration and Cleansing:
- Conduct a comprehensive review of existing data to identify and cleanse any inaccuracies or redundancies.
- Develop a detailed data mapping plan to align existing data structures with the new ERP system.
- Choose efficient data migration tools and techniques to ensure a smooth transition. 6. Configuration and Customization:
- Customize and configure the ERP system to align with specific business processes and workflows.
- Engage key users in the customization process to ensure the system meets their needs and expectations.

---

## Slide 70: How to implement ERP

7. Training and Change Management:
- Develop a comprehensive training program for all users, tailored to different roles and departments.
- Implement a change management strategy to address employee concerns and resistance, ensuring clear communication about the benefits and changes brought by the ERP system. 8. Pilot Testing:
- Conduct a pilot phase with a select group of users to test the functionality and performance of the ERP system in a controlled environment.
- Collect and analyze feedback to make necessary adjustments before full deployment. 9. Full Deployment:
- Implement the ERP system across the entire organization, ensuring all necessary integrations and data migrations are complete.
- Provide ongoing support and resources to address any issues during the transition.

---

## Slide 71: How to implement ERP

10. Monitor and Optimize:
- Establish a system for ongoing support and maintenance, addressing any technical issues promptly.
- Continuously monitor the system's performance and user feedback to identify areas for improvement. 11. Evaluate and Refine:
- Conduct regular evaluations of the ERP system to assess its impact on business processes and objectives.
- Make iterative refinements and updates to ensure the system remains aligned with evolving business needs and technology advancements.

---

## Slide 72: ERPNext: Cutting-edge Enterprise

Management Tool

- https://aws.amazon.com/marketplace/pp/pro dview-evtwbtmdkl3ya

---

## Slide 73: In-Class: ERP Lab (BlueFin eFoils)

BlueFin eFoils, Inc. is a fictional maker of electric hydrofoil boards. Demand for its BF100 kit has jumped and stock is tight.
Get In-Class_ERP-Lab_BlueFin.ipynb from the In-Class: ERP Lab assignment on Canvas and open it in Google Colab. Group work, one notebook per project team.
Four required parts:
Part 1: map Order-to-Cash and Procure-to-Pay. Name the modules and master data, one risk and one control for each.
Part 2: Order-to-Cash. Allocate stock first come, first served, then invoice.
Part 3: clean and de-duplicate the vendor master data.
Part 4: roles and segregation of duties. Write the access check and the conflict check.

Optional: reorders and receiving, a one-level MRP, and a KPI plot.
Each code part has a CHECK cell that prints PASS or says what to fix. Save a copy in
Drive first. Restart and run all, then upload the .ipynb. Due tonight, 11:59 PM.

---

## Slide 74: ERP System BPMN Model

> **Text from slide image (OCR, may contain errors):**
>
> Diagram labels: Yes · Pick · Pack · Ship · Create · Invoice · (Finance) · Apply · Cash · Post · GL · (Controller) · (Warehouse) · Complete · Sent · Payment · Received · Sales · Order · Allocate · Inventory · (SalesRep) · Stock · sufficient? · No · reate · Purchase · Receive · Goods · 3-Way · Match · Enter · AP · Backorder · (Planner) · (Buyer) · (APClerk) · Sent, · ASN/ · Invoice. · Vendor · PO · Send · ASN  

---

## Slide 75: HW #5 Salesforce Assignment

- This is an individual assignment.
- Complete the “Developer Beginner” trail on Trailhead (required: 6,500 points):
- https://trailhead.salesforce.com/trail/force_com_dev_beginner
- Submit a Word document with screenshots from your Trailhead account showing module progress, badges and points earned.
- Due: section 49 Sunday, September 27, 11:59 PM. Section 03 Sunday, October 4, 11:59 PM. Canvas has the date.

---

## Slide 76: References

- 
- 
- 
- 
- 
- 
- 
- 

https://www.oracle.com/webfolder/assets/ebook/complete-guide-to-modernerp/index.html http://www.dougengelbart.org/pubs/augment-3906.html http://nexus.awakentech.com:8080/at/awaken1.nsf/UNIDs/CFB70C1957A686E988
25654000699E1B?OpenDocument https://www.tableau.com/sites/default/files/media/designing-greatvisualizations.pdf http://proquest.safaribooksonline.com/book/operations/9788131760994 https://www.safaribooksonline.com/library/view/identity-managementa/9781583470930/ https://www.safaribooksonline.com/library/view/core-conceptsof/9781118022306/ https://www.mulesoft.com/resources/esb/erp-integration-applicationarchitecture

---

## Slide 77: (no text)

> **Text from slide image (OCR, may contain errors):**
>
> SAN JOSE STATE UNIVERSITY Powering SILICON VALLEY  

---
