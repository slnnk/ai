---
system: strongswan
status: verified
checked: 2026-07-30
tags: [ikev2, eap-mschapv2, letsencrypt, certificate-chain, windows]
---
# Windows IKEv2 client aborts right after the server certificate (incomplete CA chain)

## Symptom

A Windows built-in IKEv2/EAP-MSCHAPv2 client negotiates the IKE proposal, the
server sends its certificate and an EAP Identity request, and then the client
silently drops the exchange: no EAP answer, no CHILD_SA. Windows shows an error
about unacceptable IKE authentication credentials. Other clients may still work.
Login and password are never checked, so resetting them does not help.

## Cause

StrongSwan sends only the CA certificates it has loaded from
`/etc/ipsec.d/cacerts/` (`ipsec listcacerts`). A Let's Encrypt `chain.pem`
contains two intermediates (for example `YR1` and `Root YR` after the 2026
chain change), but only the first one gets loaded, so IKE_AUTH carries the
end-entity certificate plus one intermediate. Windows cannot build the path to
a trusted root from that and aborts before EAP.

A second, independent failure with the same symptom: the VPN "server address"
in Windows is the IP instead of the DNS name in the certificate SAN.

## Fix

1. Make sure the client uses the DNS name from the certificate SAN, not the IP.
2. Extract each intermediate from `chain.pem` into its own PEM file and verify
   it before installing:

   ```bash
   openssl crl2pkcs7 -nocrl -certfile chain.pem | openssl pkcs7 -print_certs -noout
   # save the second certificate as its own file, e.g. root-yr.pem, then
   openssl x509 -in root-yr.pem -noout -subject -issuer
   install -o root -g root -m 0644 root-yr.pem /etc/ipsec.d/cacerts/
   ipsec rereadcacerts
   ipsec listcacerts
   ```

3. Reconnect and confirm in the log that IKE_AUTH now sends all certificates
   and EAP-MSCHAPv2 completes.

`ipsec rereadcacerts` is enough; no restart is needed, so existing SAs survive.

## Limits

- Checked with strongswan-starter (`ipsec` CLI) and a Let's Encrypt chain; the
  `swanctl` equivalent is `swanctl --load-creds`.
- Renewal hooks must re-split the chain every time Let's Encrypt changes its
  intermediates; a single `chain.pem` copied into `cacerts/` is not enough.
- Side observation: with `uniqueids=never` and `rekey=no` and no inactivity
  policy, IKE/CHILD SAs accumulate for weeks (dozens per user); `ipsec statusall`
  counts are then not client counts.
