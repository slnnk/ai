---
system: nginx
status: verified
checked: 2026-08-13
tags: [nginx, upload, client_body_temp, request-buffering, nexus, artifact-repository, disk-full]
---
# Multi-gigabyte PUT through nginx fails with 413/500 and fills the root filesystem

## Symptom

Uploading a large artifact (several GB) to a repository manager (Nexus, Artifactory, MinIO) behind
nginx:

- through the external reverse proxy: `HTTP 413 Request Entity Too Large`;
- through the internal nginx: the transfer runs for minutes, then `HTTP 500`; at the same time the
  monitoring shows the proxy host's `/` at <1% free; free space returns as soon as the request aborts
  and nginx deletes its temp file. The object is not created (`HTTP 404` afterwards).

## Cause

By default nginx buffers the whole request body before proxying (`proxy_request_buffering on`) into
`client_body_temp_path` (Debian/Ubuntu: `/var/cache/nginx/client_temp`), which usually sits on the
small root filesystem, while the backend's data directory lives on a big separate volume. The upload
also has to fit `client_max_body_size` at every proxy layer.

## Fix

Pick one, in order of preference:

1. Stream the body straight to the backend for the upload locations:

   ```nginx
   location /repository/ {
       client_max_body_size 0;          # or an explicit limit large enough
       proxy_request_buffering off;
       proxy_http_version 1.1;
       proxy_pass http://127.0.0.1:8081;
   }
   ```

2. Or move the temp directory to the large volume:

   ```nginx
   client_body_temp_path /data/nginx/client_temp 1 2;
   ```

   (create the directory owned by the nginx worker user, `nginx -t`, reload).

3. Emergency one-off: bypass nginx entirely with an SSH tunnel to the backend port and stream the
   file, then verify the stored blob's size and checksum:

   ```bash
   ssh -L 18081:127.0.0.1:8081 repo-host
   curl --fail -u "$USER:$PASS" -T big.tar.zst http://127.0.0.1:18081/repository/raw/path/big.tar.zst
   curl -sI -r 0-0 https://repo.example/repository/raw/path/big.tar.zst   # expect HTTP 206
   ```

Raise `client_max_body_size` on the external proxy as well, or the 413 remains.

## Limits

- With request buffering off, nginx cannot retry the request on another upstream and the backend
  must handle slow clients; fine for artifact uploads, check for other locations.
- Check every hop: an external load balancer or WAF may enforce its own body limit.
- Watch the backend's own disk: the blob store must have room for the object plus temporary copies.
