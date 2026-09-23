---
system: vpn-gateway
status: verified
checked: 2026-07-30
tags: [strongswan, ikev2, eap-mschapv2, l2tp, letsencrypt, windows, vpn]
---
# VPN gateway `91.218.141.22`

## 2026-07-30: StrongSwan check

- Host: `gateway`, access: `ssh root@91.218.141.22`.
- Active service: `strongswan-starter`.
- Main connection configuration: `/etc/ipsec.conf`.
- Credentials and keys of the starter configuration: `/etc/ipsec.secrets`.
- Additional site-to-site configuration: `/etc/swanctl/swanctl.conf`.
- Client IKEv2 uses `rightauth=eap-mschapv2`; the EAP account is defined in `/etc/ipsec.secrets`.
- L2TP with PSK and a separate IKEv2 site-to-site tunnel are also configured. Secret values were not copied into the note.
- Server IKEv2 ID: `fabalonueyisk.beget.app`; client pool: `10.250.0.0/16`; DNS: `8.8.8.8`, `8.8.4.4`.
- Status check: `systemctl status strongswan-starter`; view loaded connections: `ipsec statusall`.

### Windows IKEv2 diagnostics

- The Windows client successfully negotiates the IKE proposal and receives the server certificate with an EAP Identity request, but does not continue the EAP exchange; so the refusal happens before the client login and password are checked.
- The certificate is valid from `2026-07-28` to `2026-10-26`, contains EKU `TLS Web Server Authentication` and SAN `fabalonueyisk.beget.app`, `www.fabalonueyisk.beget.app`.
- DNS `fabalonueyisk.beget.app` points to `91.218.141.22`.
- For Windows, the VPN address field must use `fabalonueyisk.beget.app`, not the IP address, otherwise the server name does not match the certificate SAN and Windows shows an error about unacceptable IKE authentication credentials.
- The server sends the end-entity certificate and the Let's Encrypt intermediate certificate `YR1`.
- After the certificate renewal on 2026-07-28 the current chain became `YR1 -> Root YR -> ISRG Root X1`.
- The Let's Encrypt file `chain.pem` contains `YR1` and `Root YR`, however `ipsec listcacerts` shows that StrongSwan loaded only `YR1`. In IKE_AUTH the server also sends only the end-entity certificate and `YR1`.
- Windows aborts the exchange right after the certificates, not even answering the EAP Identity. With the correct domain name, the most likely confirmed cause is the incomplete sent chain: `Root YR` is missing.
- Fix: save `Root YR` as a separate PEM file in `/etc/ipsec.d/cacerts/`, re-read the StrongSwan CA certificates and verify in the logs that both intermediate certificates are sent during IKE_AUTH. Do not restart the service unnecessarily: at the time of diagnosis there were many active SAs.

### Chain fix, 2026-07-30

- The second certificate from the current Let's Encrypt `chain.pem` was extracted and verified before installation: subject `Root YR`, issuer `ISRG Root X1`.
- `/etc/ipsec.d/cacerts/root-yr.pem` was installed with owner `root:root` and mode `0644`.
- `ipsec rereadcacerts` was executed; a service restart was not required.
- `ipsec listcacerts` shows both `YR1` and `Root YR` loaded simultaneously.
- `strongswan-starter` stayed active; the existing 89 Security Associations were not torn down.
- It remained to confirm with a new Windows connection that the server sends the full chain in IKE_AUTH and EAP authentication completes.
- The new Windows attempt at `2026-07-30 21:50:27-21:50:28` succeeded: the server sent three certificates, EAP-MSCHAPv2 completed successfully, `IKE_SA ikev2-vpn[2353]` and `CHILD_SA ikev2-vpn{1582}` were created, the client received `10.250.0.77`.

### Accumulated SAs

- The number `89 up` does not mean 89 clients: 90 IKE SAs and 89 CHILD SAs were found, but only 18 unique public IPs.
- The entries are up to 49 days old; dozens of SAs belong to the same public IP and EAP user.
- Cause of the accumulation: `uniqueids=never`, `rekey=no`, and the IKEv2 profile has no cleanup policy for inactive SAs.
- Cleanup and changes to the lifecycle parameters have not been performed yet.
- Control snapshot after the Windows connection: only 1 client was actually passing traffic, virtual IP `10.250.0.77`, external IP `193.160.204.45`; the activity was right at the moment of the check. Over the 5, 15 and 60 minute windows the number of active clients is the same: 1.

## Portable lesson

`~/ai/general/knowledge/strongswan/windows-ikev2-aborts-before-eap-incomplete-ca-chain.md`
