---
system: rabbitmq
status: verified
checked: 2026-09-22
tags: [rabbitmq, docker-compose, migration, node-rename, sorm, definitions]
---
# RabbitMQ configuration transfer to 172.28.0.186

Date of check and transfer: 2026-09-22. Translated from Russian.

## Task

Transfer the Docker Compose file and RabbitMQ configuration from the old host to the new one.

## Context

- Source: `youdo@10.16.26.61:/data`.
- Destination: `root@172.28.0.186:/root/rabbitmq`.
- Task: transfer the Docker Compose and RabbitMQ configuration.

## Actions

Transferred over SSH directly between the nodes:

- `/data/docker-compose.yml` -> `/root/rabbitmq/docker-compose.yml`;
- `/data/etc/advanced.config` -> `/root/rabbitmq/etc/advanced.config`;
- `/data/etc/enabled_plugins` -> `/root/rabbitmq/etc/enabled_plugins`.

A streaming `tar` over SSH was used, without a local intermediate copy. The destination directory already existed and was empty.

SHA-256 checked on source and destination: all three files match. Owner on the target node is `root:root`; file permissions `0644`, directory `etc` `0755`.

`docker compose config -q` on the target node completed successfully. Compose reported only a warning that the top-level `version` field is obsolete and ignored.

## Findings

Configuration and operational notes:

- Image: `rabbitmq:3.8.34-management-alpine`.
- Container name: `rabbitmq`; hostname: `spb2-rabbit01`.
- Ports: AMQP `5672`, management UI `15672`.
- Plugins `rabbitmq_management` and `rabbitmq_prometheus` are enabled.
- `consumer_timeout` is disabled in `advanced.config`.
- Compose expects local directories `./data` and `./logs`; the Mnesia runtime data and the Erlang cookie from the source `/data/data` were intentionally not transferred within the scope of the configuration-transfer request.
- The container on the target server was not started (at this stage).

### Security and risks

`docker-compose.yml` embeds the values of `RABBITMQ_ERLANG_COOKIE`, `RABBITMQ_DEFAULT_USER` and `RABBITMQ_DEFAULT_PASS`. Their values are not recorded in the knowledge base. It is recommended to move them into a protected store/environment variables and to consider rotation after the migration.

Before starting, check whether the existing queue state needs to be transferred and whether the directories `/root/rabbitmq/data` and `/root/rabbitmq/logs` need to be created with proper permissions.

## Changes

### Node rename after start

On the same day the container was started and the node name was changed from `rabbit@spb2-rabbit01` to `rabbit@sorm-rabbitmq` by replacing `hostname` in `/root/rabbitmq/docker-compose.yml` with `sorm-rabbitmq` and recreating the container.

Checked before recreating: there were no active connections, queues or messages; users `admin` and `youdo`, vhosts `/` and `sorm`, and the permissions of both users existed. Definitions were exported to `/root/rabbitmq/data/definitions-before-node-rename.json` with permissions `0600` and imported back after the new node started.

Compose backup: `/root/rabbitmq/docker-compose.yml.before-node-rename-20260922`.

Final check:

- node and cluster name: `rabbit@sorm-rabbitmq`;
- container `rabbitmq` is running;
- users, vhosts and permissions restored;
- ports `5672` and `15672` listen on IPv4 and IPv6;
- no alarms and no network partitions.

## Open items

The old Mnesia directories `rabbit@spb2-rabbit01*` are kept next to the new `rabbit@sorm-rabbitmq*` as a temporary rollback option. Do not delete them until the application-level check is confirmed. RabbitMQ also warns that passing the Erlang cookie through `RABBITMQ_ERLANG_COOKIE` is deprecated; the cookie should be moved into a file or a protected configuration mechanism during planned maintenance.

## Portable lesson

[`~/ai/general/knowledge/rabbitmq/rename-node-in-docker-compose.md`](../../../../general/knowledge/rabbitmq/rename-node-in-docker-compose.md)
