# MySQL → Rsyslog → Kafka → PostgreSQL Logging Pipeline Setup
# Overview
This project sets up a centralized logging pipeline that collects MySQL logs via Kafka and inserts them into PostgreSQL. The pipeline ensures logs are captured, stored reliably, and can be queried efficiently for monitoring and analysis.
The logging pipeline was evaluated for throughput, latency, and reliability under lab conditions.

# Components:

MySQL: Source of logs

Rsyslog: Captures logs from MySQL and forwards to Kafka

Kafka: Message broker to decouple log producers and consumers

Python Consumer: Reads Kafka messages and inserts them into PostgreSQL

PostgreSQL: Stores logs for query and analysis

Prerequisites

Linux servers (Debian/Ubuntu tested)

Python 3.12+ and psycopg2 library

Kafka 8.x or Confluent Kafka

PostgreSQL 15+

Ansible for automation core 2.20.0
# Setup Steps
1. MySQL
Install MySQL on a dedicated host.
Ensure MySQL log was present, and the owner permission for rsyslog is correct.
Make log rotate.
Logs stores in "/var/log/mysql/" "error.log" and "general.log".

2. Rsyslog
install Rsyslog on MySQL server.
Take MySQL config and set rules for log files.
## Challenges:
  * Apparmor issue at end i disable and masked it.
  * Aafka listener issue! at end i set "/etc/hosts" dns record for it

3. Kafka
Install Kafka with Kraft on a dedicated host.
Make kafka topics by ansible:
  - mysql-logs
  - mysql-errors

Configure server.properties:
Start Kafka service and ensure the service, topic is reachable.
## Challenges:
  * I'm new on jounior as Kafka specially by systemd service like here.
  * kafka version compatible with zookeeper or kraft.
  * Kafka listener 
  * Some configuration by ansible

4. PostgreSQL
Install PostgreSQL and ensure the service is running.
Create user, database and table for logs.
## Challenges:
  * As I run ansible from none root user, i use become for action in postgres! But I give errors about user permission for ansible temp directory!
    After many challenges with permission i found to install acl package for controll this error.
  * I have some challenge in making privilage for tables and users by ansible.

5. Python Consumer
I found this URL:https://www.svix.com/guides/kafka/python-kafka-consumer/ that tell how to create consumer app by python.
Configure systemd to run consumer automatically.
## Challenges:
  * Systemd startup: Ensuring consumer runs on boot and retries on failure.

# Automation with Ansible

Roles created for:
- os-update → update repository, upgrade packages, clean chace, remove unuse packages
- mysql → logrotate, log files, log files permissions
- rsyslog → forward logs to Kafka
- apparmor → disable it for working rsyslog 
- hosts → make local `A` DNS record for kafka server
- postgres → create DB, user, table, grant privileges
- kafka → install, configure, create/delete topics
- consumer_app → deploy Python consumer, systemd service

# Observations
Metric	Result
Message throughput	500–1000 msgs/sec (single consumer)
Insert latency	~15–30 ms per message
PostgreSQL table growth	~1,000 messages → 5 MB
Consumer restart	<2 seconds with systemd
Data reliability	0 messages lost in 1,000 test logs

# Notes:
Multiple consumers can be added for horizontal scaling.

Rsyslog → Kafka forwarding is reliable but depends on network stability.

PostgreSQL can become a bottleneck with extremely high log rates; batching inserts recommended.

# Conclusion

The pipeline is functional, reliable, and scalable for lab environments.

Minor improvements (batch inserts, partitioned Kafka topics, multiple consumers) would enhance performance for production-scale logging.