# vision-telematics-backend

## Project Tree

``` bash
.
├── apps
│   └── example # A django rest app
│       ├── api
│       │   ├── v1 # Only the "presentation" layer exists here.
│       │   │   ├── __init__.py
│       │   │   ├── serializers.py
│       │   │   ├── urls.py
│       │   │   └── views.py
│       │   ├── v2 # Only the "presentation" layer exists here.
│       │   │   ├── __init__.py
│       │   │   ├── serializers.py
│       │   │   ├── urls.py
│       │   │   └── views.py
│       │   └── __init__.py
│       ├── fixtures # Constant "seeders" to populate your database
│       ├── management
│       │   ├── commands # Try and write some database seeders here
│       │   │   └── command.py
│       │   └── __init__.py
│       ├── migrations
│       │   └── __init__.py
│       ├── templates # App-specific templates go here
│       ├── tests # All your integration and unit tests for an app go here.
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── models.py
│       ├── services.py # Your business logic and data abstractions go here.
│       ├── urls.py
│       └── views.py
├── common # An optional folder containing common "stuff" for the entire project
├── config
│   ├── settings.py
│   ├── asgi.py
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── deployments # Isolate Dockerfiles and docker-compose files here.
├── docs
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── deployment.md
│   ├── local-development.md
│   └── swagger.yaml
├── requirements
│   ├── common.txt # Same for all environments
│   ├── development.txt # Only for a development server
│   ├── local.txt # Only for a local server (example: docs, performance testing, etc.)
│   └── production.txt # Production only
├── static # Your static files
├── .env.example # An example of your .env configurations. Add necessary comments.
├── static # Your static files
├── .gitignore # https://github.com/github/gitignore/blob/main/Python.gitignore
├── entrypoint.sh # Any bootstrapping necessary for your application
├── manage.py
├── pytest.ini
└── README.md
```


Migration order:

settings --> engineer --> products --> orders --> services


Important Note: The Service table tracks what work needs to be done (install the car kit), while the Booking table tracks when and who will do it (appointment date and assigned engineer).

Let's clarify the flow of the **Service** and **Booking** tables and when to use each one in your application. I'll explain the roles and how they fit into the overall process of installing a car kit by customer order.

### **Concept Overview:**

1. **Service Table**:
    - The **Service** table represents the actual work being performed, such as installing a car kit. It links to both an **Order** (representing the customer’s purchase) and an **Engineer** (the person performing the work). Each order may result in one or more services.
    - Use the **Service** table to track the details of the specific tasks that need to be carried out for a particular order.

2. **Booking Table**:
    - The **Booking** table represents the **scheduled time** for the service to be performed. It contains a one-to-one link to the **Order** and a foreign key to the **Engineer**. This table focuses on the logistics, such as the appointment date and time when the engineer will perform the service.
    - Use the **Booking** table to manage the scheduling aspect of the service (date, time, and engineer assignment).

### **Flow Explanation**:

Here’s how these tables would work together in the flow of your application:

#### **1. Order is Placed (Trigger for Creating Service)**
- **Example**: A customer orders a car kit installation online.
- **Order**: The order is placed and stored in the `Order` table, which contains all the details of the products purchased (e.g., car kit) and customer information.
- **Service**: At this point, a new service entry can be created in the `Service` table because the installation will be a specific task associated with the order. The **Service** record represents the actual installation that will take place.

**Example Service Entry**:
- **Order**: Links to the customer’s order.
- **Engineer**: Will be assigned later, once the engineer is selected.
- **Service Details**: Could include notes or a status indicating that the installation is "pending."

#### **2. Schedule the Installation (Trigger for Creating Booking)**
- **Example**: Once the order is processed, the service team contacts the customer and schedules an appointment for the installation.
- **Booking**: A new entry is created in the `Booking` table to store the date, time, and engineer assigned to the installation.

**Example Booking Entry**:
- **Order**: Links to the customer’s order (one-to-one relationship with the `Order` table).
- **Engineer**: The specific engineer assigned to perform the installation.
- **Scheduled Time**: Date and time for the appointment.

> **Important Note**: The **Service** table tracks **what** work needs to be done (install the car kit), while the **Booking** table tracks **when** and **who** will do it (appointment date and assigned engineer).

#### **3. Installation Day (Service Execution)**
- **Service**: On the day of the scheduled installation, the engineer arrives at the customer’s location and installs the car kit. After the work is completed, the status of the service is updated to "Completed" in the `Service` table.
- **Booking**: Once the installation is complete, the booking status can also be marked as "Completed" to indicate that the appointment has taken place.

#### **When to Use Each Table**:

- **Service Table**:
    - Use this table to represent **what work is required** for an order, such as the installation of a car kit.
    - Each time an order is placed that requires a service (like installation), a new **Service** entry should be created.
    - The **Service** table focuses on the task itself and tracks the assigned engineer and the status of the service.

- **Booking Table**:
    - Use this table to manage **when and who will perform the service**. This table stores the logistics, such as the scheduled appointment date and the engineer responsible for the task.
    - Each service-related order should have one corresponding **Booking** entry to schedule the task.
    - The **Booking** table helps with scheduling, tracking appointment times, and managing engineer assignments.

---

### **Real-Life Example of the Flow**:

1. **Order Placement**:
    - **Customer Action**: John, a customer, orders a car kit online.
    - **System Action**: The order is created in the `Order` table, and a corresponding service is created in the `Service` table, which will handle the installation of the car kit.
    - **Service**: A new service entry is created, indicating that a car kit installation needs to be performed for John's order.

2. **Service Scheduling**:
    - **Customer Action**: The service team contacts John to schedule an installation appointment.
    - **System Action**: A new booking entry is created in the `Booking` table, storing the appointment date and the engineer assigned to install the car kit.
    - **Booking**: Tracks that John's installation is scheduled for next Monday at 10 AM with Engineer Sarah.

3. **Service Execution**:
    - **Customer Action**: Engineer Sarah arrives at John’s home on the scheduled date and installs the car kit.
    - **System Action**: After the installation, the status of the service in the `Service` table is marked as "Completed."
    - **Booking**: The booking is also updated to reflect that the appointment has been completed.

---

### **Summary of Table Usage**:

- **Service Table**:
    - Tracks what needs to be done (install a car kit).
    - Associates the service with an order and an engineer.
    - Used to track the progress of the task (e.g., pending, in progress, completed).

- **Booking Table**:
    - Tracks when and who will do the service.
    - Manages the logistics of scheduling the service and assigning an engineer.
    - Keeps a record of the appointment and its completion status.

By separating the **Service** and **Booking** tables, you gain the flexibility to manage both the task of car kit installation and the logistics of scheduling and assigning engineers. This allows for better tracking and organization of services for both internal management and customer satisfaction.


Certainly! The `Service` model represents a service or maintenance request related to a specific customer, possibly for equipment or products they purchased. This model helps in tracking service details, scheduling, faults reported, resolutions, and customer satisfaction. Here’s a breakdown of each field and its business purpose:

### Fields and Business Purpose

1. **`service_ref` (CharField)**
    - **Purpose**: A unique reference or identifier for each service record.
    - **Business Use**: Used to track and distinguish each service instance in the system. This could be an order number or a service request ID for easy retrieval.

2. **`purchase_date` (DateField)**
    - **Purpose**: The date when the equipment or service was originally purchased.
    - **Business Use**: Helps in calculating warranty periods and understanding if a service request falls within or outside of warranty. Useful for invoicing and maintenance records.

3. **`first_return_visit` (DateField)**
    - **Purpose**: The date of the first follow-up or return visit after the initial service.
    - **Business Use**: Used to schedule or track follow-ups for maintenance or inspection. This field is particularly useful if recurring service is part of the offering.

4. **`fault_reported_date` (DateField)**
    - **Purpose**: The date on which the customer reported an issue or fault with the equipment.
    - **Business Use**: Helps in measuring response time from fault reporting to resolution and tracking performance metrics for customer service.

5. **`contact` (CharField)**
    - **Purpose**: Stores the name of the contact person associated with the service.
    - **Business Use**: Ensures clear communication with the correct person at the customer’s end regarding service updates or scheduling.

6. **`service_call_date` (DateField)**
    - **Purpose**: The date when a service call was made, either for an inspection or troubleshooting.
    - **Business Use**: Helps track the timeline of the service process, including when the company reached out or scheduled a visit after the fault was reported.

7. **`time` (TimeField)**
    - **Purpose**: The time for the scheduled service call or visit.
    - **Business Use**: Used for scheduling purposes to allocate resources and avoid overlaps in engineers’ schedules.

8. **`nature_of_fault` (CharField)**
    - **Purpose**: A description of the issue or fault reported.
    - **Business Use**: Provides a quick overview for service staff and engineers to understand the problem. Useful for tracking common issues or faults and analyzing trends in equipment failures.

9. **`equipment_details` (TextField)**
    - **Purpose**: Detailed information about the equipment requiring service.
    - **Business Use**: Helps engineers understand the specifications and setup of the equipment before they arrive on-site, allowing them to bring the right tools and parts.

10. **`notes` (TextField)**
    - **Purpose**: Additional notes regarding the service, such as observations, recommendations, or special instructions.
    - **Business Use**: Useful for internal documentation and communication between different service staff. Helps ensure continuity of service if multiple engineers are involved.

11. **`date_resolved` (DateField)**
    - **Purpose**: The date the fault or issue was resolved.
    - **Business Use**: Important for calculating the resolution time, which can impact performance metrics, customer satisfaction, and possibly contractual obligations.

12. **`customer_satisfied` (BooleanField)**
    - **Purpose**: Indicates whether the customer was satisfied with the service provided.
    - **Business Use**: Used for quality assurance and customer satisfaction tracking. Helps identify areas for improvement in service processes.

13. **`invoice_received_date` (DateField)**
    - **Purpose**: Date on which the invoice for this service was received from the engineer or service provider.
    - **Business Use**: Helps track the billing process, ensuring that services are billed promptly and that the company receives invoices in a timely manner.

14. **`invoice_authorised_date` (DateField)**
    - **Purpose**: Date on which the invoice was authorized or approved for payment.
    - **Business Use**: Ensures proper auditing and accounting processes are followed. Tracks when an invoice is cleared for payment, ensuring efficient payment processing.

15. **`maintenance` (BooleanField)**
    - **Purpose**: Indicates whether the service is for routine maintenance rather than a fault repair.
    - **Business Use**: Helps differentiate between preventive maintenance and reactive repairs. Maintenance can be scheduled ahead of time, while repairs might require urgent attention.

16. **`engineer` (ForeignKey to `Engineer`)**
    - **Purpose**: The engineer assigned to this service task.
    - **Business Use**: Allows for tracking which engineer handled a specific service call, which is helpful for accountability, skill-matching, and evaluating performance.

17. **`order` (ForeignKey to `Order`)**
    - **Purpose**: Links the service to a specific order, if applicable.
    - **Business Use**: Allows tracking services against the original order, which can be useful for warranty claims, service tracking, and billing accuracy.

18. **`customer` (ForeignKey to `Customer`)**
    - **Purpose**: The customer associated with the service request.
    - **Business Use**: Links the service request directly to the customer, which is essential for communication, tracking service history, and providing personalized support.

19. **`install_level` (ForeignKey to `InstallLevel`)**
    - **Purpose**: The level or type of installation required for the service (e.g., standard, premium, specialized).
    - **Business Use**: Allows differentiation of service types or levels based on complexity or customer requirements. Helps in billing and resource allocation for complex installations.

### Business Use Cases for the Service Model

- **Service Scheduling**: By recording the `service_call_date` and `time`, and linking to an engineer, the model enables the effective scheduling of service calls, ensuring engineers are allocated effectively.

- **Customer Service Tracking**: With fields like `customer`, `contact`, and `nature_of_fault`, you can track a customer’s issues and service requests, enabling better customer relationship management.

- **Response Time & Performance Metrics**: Fields like `fault_reported_date`, `service_call_date`, and `date_resolved` allow you to calculate the time taken to respond and resolve issues, which can help measure performance.

- **Billing & Invoicing**: By tracking `invoice_received_date` and `invoice_authorised_date`, the company can manage its billing cycle more efficiently, ensuring engineers and suppliers are paid promptly.

- **Quality Assurance**: Tracking `customer_satisfied` and `date_resolved` helps the business gather feedback on service quality and customer satisfaction, which can inform future improvements.

- **Maintenance vs. Repairs**: Differentiating between `maintenance` and regular service calls allows for proactive scheduling of preventive maintenance, which can reduce the occurrence of issues and enhance customer satisfaction.

In summary, the `Service` model provides a detailed record of service interactions with customers, enabling scheduling, tracking, billing, performance measurement, and customer satisfaction analysis. It supports both reactive repairs and proactive maintenance, improving overall service quality and efficiency.