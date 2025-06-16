# PVSimulator: PV Simulator Challenge

This Simulator prepares for PV simulator challenge and include to run RabbitMQ and to simulate PV power values. 

## Requirements

To run this project, you will need the following:

- Python 3.8+
- Docker
- Docker Compose
- RabbitMQ
- Pandas
- matplotlib

## Setup

### Activate the virtual environment:

1. **Create the virtual environment:**

    ```sh
    python -m venv .venv
    ```

2. **Activate the virtual environment:**
    - On Windows:

        ```sh
        .venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source .venv/bin/activate
        ```

### Install the dependencies

1. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Run RabbiMQ Message broker for python: based https://github.com/pazfelipe/python-rabbitmq.git 

    Run the RabbitMQ container using Docker Compose:
    ```bash
    docker compose -f compose_files/rabbitmq-python.yaml up -d
    ````
    Close Container :
    ```bash
    docker compose -f compose_files/rabbitmq-python.yaml down
    ````
### Note

The RabbitMQ management console can be accessed at [http://localhost:15672](http://localhost:15672).

## Define Publisher classes in src/publisher.py
### Publish a message

1. **Run the publisher script to publish a test message:**

    ```sh
    python3 src/publisher.py
    ```

## Define Consumer classes in src/consumer.py
### Consume messages

1. **Run the consumer script to consume and save test messages:**

    ```sh
    python3 src/consumer.py
    ```

# Replication Meter data

For simulation reading meters, I assume that MeterA is the amount of electricity from line and MeterB is the amount of generated electricity of PV,
so the usage of house is the summation of MeterA and MeterB.

Assumption Reading: Read amount of the both meters at the same time and publish which may be different time differences.
Assumption Comsuming: Consumer save published time, meter of MeterA, meter of MeterB, Sum(MeterA + MeterB), Generated exlectrricity from PV (in KWH, scaled for better comparison) for each publication for more fine time scale than publisher.

## After finish consuming messages, one have to stop Consumer in this test

Cunsumer is waiting to publish messages until error or Keystroke to stop waiting

## Further modification: Wait more messages or spend time before consume messages


# Running with Container:
## Clone PVSimulator from github

    ```bash
    git clone https://github.com/kangkabseok2021/PVSimulator.git 
    ```

## Docker Build: In PVSimulator

    ```bash
    docker build -t pv-simulator .
    ````

## Run the RabbitMQ container using Docker Compose: In PVSimulator
    ```bash
    docker compose -f compose_files/rabbitmq-python.yaml up -d
    ````

## Run conrtainer: Run mkdir Images In PVSimulator if it needed

    ```bash
    docker container run --network host -it -v ./Images:/PVSimulator/Images pv-simultor bash
    ```

### Run publisher and consumer inside container: Need to stop consumer manually