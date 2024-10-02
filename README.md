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