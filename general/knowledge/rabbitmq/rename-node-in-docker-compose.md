---
system: rabbitmq
status: verified
checked: 2026-09-22
tags: [rabbitmq, docker-compose, node-name, hostname, mnesia, definitions, erlang-cookie]
---
# Rename a single RabbitMQ node running under Docker Compose

## Symptom

A RabbitMQ container was moved to another host or given a new role, and its node name
(`rabbit@<old-hostname>`) should change. Just editing `hostname:` in `docker-compose.yml` and
recreating the container starts an **empty** node: the Mnesia directory is keyed by node name
(`/var/lib/rabbitmq/mnesia/rabbit@<hostname>`), so users, vhosts, permissions and queues are
gone from the new node's point of view.

## Cause

RabbitMQ derives the node name from the container hostname (`RABBITMQ_NODENAME` defaults to
`rabbit@$HOSTNAME`). Metadata lives in a per-node Mnesia schema that cannot be renamed
in-place on a running node; `rabbitmqctl rename_cluster_node` requires a stopped node and is
awkward in containers. For a node with no messages in flight, export/import of definitions is
the simplest safe path.

## Fix

1. Confirm the node is quiet and record its state:

   ```bash
   docker exec rabbitmq rabbitmqctl list_connections
   docker exec rabbitmq rabbitmqctl list_queues name messages
   docker exec rabbitmq rabbitmqctl list_users; docker exec rabbitmq rabbitmqctl list_vhosts
   docker exec rabbitmq rabbitmqctl export_definitions /var/lib/rabbitmq/definitions-before-rename.json
   chmod 0600 <bind-mounted path>/definitions-before-rename.json
   cp docker-compose.yml docker-compose.yml.before-node-rename-$(date +%Y%m%d)
   ```

2. Change `hostname:` (or set `RABBITMQ_NODENAME=rabbit@<new>`) in `docker-compose.yml` and
   `docker compose up -d --force-recreate`.
3. Import the definitions into the new node and verify:

   ```bash
   docker exec rabbitmq rabbitmqctl import_definitions /var/lib/rabbitmq/definitions-before-rename.json
   docker exec rabbitmq rabbitmqctl cluster_status   # node and cluster name = rabbit@<new>
   docker exec rabbitmq rabbitmqctl list_permissions -p <vhost>
   ss -ltn | grep -E ':(5672|15672) '
   ```

4. Keep the old `rabbit@<old>*` Mnesia directories next to the new ones until the
   application-level check passes; revert by restoring the backup compose file and
   recreating. Delete them afterwards.

When migrating config between hosts, copy `docker-compose.yml`, `etc/advanced.config` and
`etc/enabled_plugins` with `tar | ssh ... tar -x` and compare `sha256sum` on both sides;
`docker compose config -q` validates the result (a warning about the obsolete top-level
`version:` key is harmless).

## Limits

- Definitions do not include messages. If queues hold data, drain them first or use
  `rename_cluster_node` on the stopped node instead.
- `RABBITMQ_ERLANG_COOKIE` in the environment is deprecated (RabbitMQ 3.8+ warns); move the
  cookie to `/var/lib/rabbitmq/.erlang.cookie` or a secret. Credentials embedded in
  `docker-compose.yml` belong in an env file or secret store and should be rotated after a
  host move.
- Checked with `rabbitmq:3.8.34-management-alpine`, single node, no cluster peers.
