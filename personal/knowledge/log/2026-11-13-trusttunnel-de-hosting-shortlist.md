---
system: trusttunnel-de
status: verified
checked: 2026-11-13
tags: [hosting, vps, budget, migration]
---
# Budget Russian relay hosting research

## Task
User requested hosting research within300RUB/month plus/minus100, following their decision to stop diagnosing the current Russian relay provider. Scope is the Russian relay replacement, not the German backend. No purchase or migration authorized.

## Current selection status

Superseded: the user selected SimpleCloud and authorized deployment, now verified in [migration outcome](2026-11-13-trusttunnel-de-simplecloud-relay-migration.md). The availability-gap statements below describe the earlier search stage only.

User corrected actual order availability: AdminVPS tariff cannot currently be ordered;
IHOR offers only Europe in the user's current ordering flow. A subsequent user screenshot
of FirstByte billing shows only Finland, Netherlands, Germany, Bulgaria, Spain, USA and
Brazil, with no Russia. These observations supersede public landing-page availability
assumptions. None of these three is currently a suitable orderable Russian-relay choice.
Earlier candidate recommendations below are retained as research history, not active picks.
Budget remains200–400RUB; no suitable in-stock Russian option has been confirmed.

## Findings
Primary candidate: [IHOR Ferrum](https://ihor.online/vds), Moscow, advertised300RUB per month,1vCPU/1GB RAM/20GBdisk, KVM, up to200Mbit/s unlimited outgoing subject to fair use, dedicated IP and VNC. Extra1GBRAM is100RUB/month, so the advertised upgraded configuration totals400RUB. [Proxy offering](https://ihor.online/vds/vds-s-proxy) explicitly markets proxy usage. [FAQ](https://ihor.online/faq) does not promise IP replacement for testing VPN protocols. [VDS SLA](https://ihor.online/agreements/predostavlenie-virtualnogo-vydelennogo-servera-soglashenie-ob-urovne-uslug) contains standard abuse/legal-use restrictions; no blanket private-VPN ban was found in inspected terms. This is a candidate for a one-month trial, not a verified guarantee of reliability or private-relay contractual acceptance. Checkout stock, final IPv4 pricing and exact intended relay acceptance were not independently confirmed with support; no support message was sent.

Excluded or lower priority:
- [FirstVDS pricing](https://firstvds.ru/docs/tariffs.html):299RUB/1GB/15GBSSD/100Mbit/s withIPv4, but [current conditions](https://firstvds.ru/docs/main/usloviya_predostavleniya_uslug_ao_iot.pdf) section2.10 explicitly includes intermediary VPN infrastructure in prohibited use. Attractive price does not make it suitable for this relay.
- [RUVDS](https://ruvds.com/ru/vps_start/):349RUB/1GB/20GBSSD, but [contract](https://ruvds.com/ru-rub/contract) section2.3.5 restricts public VPN/proxy, private deployments above10GB/day and access to restricted resources. Do not recommend for this relay.
- [AdminVPS](https://adminvps.ru/vps/vps_russia.php): initial indexed Lite299RUB was stale. Follow-up direct HTML retrieval shows349RUB/month,1vCPU/1GB/15GBNVMe/100Mbit/s and1TB/calendar month. Conditional candidate, not rejected on an established Russia-wide VPN ban; see follow-up below. Included IPv4/final total and exact relay acceptance unverified.
- [JustHost](https://justhost.ru/): current primary page has229RUB introductory first-month price with subsequent automatic tariff change, regular1GB pricing above budget. Do not advertise229RUB as recurring price.
- [RuWeb](https://ruweb.net/vds): current1GBMICRO471RUB/month above budget;512MBNANO393RUB is too tight for the existing full relay/security stack. [Terms](https://ruweb.net/info/tos) distinguish public VPN from ordinary family use; older landing-page prices conflict with current tariff page.
- [VDSka](https://vdska.ru/page/vds-servera/): old2022resource-price note and live calculator/fixed-price output disagree; do not recommend an unconfirmed343RUB quote.
- HostingRussia250RUB has attractive published specifications but substantial recent outage/return complaints, including provider replies on [Hosting101](https://hosting101.ru/hosting-russia.ru); excluded from a reliability-led recommendation. User reviews are not independently verified incident proof.

## Status and risks
Research complete; agent recommendation is IHOR Ferrum300RUB for an initial one-month trial, optionally2GBRAM400RUB. User has not selected it. Site uptime ratings measure provider websites rather than the future guest or route to Germany; performance/reliability remain unverified. Further migration planning stays in central TODO. No new checks against the old relay, no purchase, contact, provisioning, DNS edit or deployment. All commands completed, no background work.

## AdminVPS follow-up requested by user

Direct curl retrieval of the Russian VPS page succeeded (494783bytes), saved at `/home/slnnk/ai-data/vpn-proxy-diagnostics/adminvps-russia.html`. Current Lite price349RUB/month supersedes search-index299RUB; Promo499RUB is outside the stated budget. Specs remain1vCPU,1GBRAM,15GBNVMe,100Mbit/s,1TB/calendar month. No explicit IPv4 inclusion or traffic-accounting/overage detail was found in the inspected page; do not claim349RUB is the independently verified all-in checkout total.

Direct [offer PDF](https://adminvps.ru/about/oferta.php) reads returned HTTP200/application-pdf with0bytes, not a readable complete document. The provider's indexed PDF excerpt says VPN use is prohibited in Belarus and Kazakhstan; it does not establish a blanket Russia ban. Index search also shows restrictions on proxy-checkers, which must not be conflated with a private relay. Original third-party catalogue VPN/proxy warning remains insufficient to reject the Russian VPS. General VPN advertising does not prove that this specific private TCP/UDP relay is contractually accepted.

Agent assessment: AdminVPS is a reasonable conditional candidate within budget if support confirms final price including IPv4, acceptance of a private nginx TCP/UDP443 passthrough relay to a German VPN endpoint,1TBaccounting and behavior after the limit. A relay crosses the VPS network twice per payload, so traffic accounting matters; no assumption is made that the provider bills both directions. Draft questions only; none sent. No purchase/deployment, performance or reliability test. User is still comparing providers; migration proposal stays open without implementation permission. All task commands completed, no background operations.

## Availability corrections and additional screening

User said `adminvps тариф сейчас нельзя заказать, ihor - только европа`. Then supplied a FirstByte billing screenshot showing the datacenter selector without Russia. Do not infer actual stock from a public tariff, a Moscow hostname in a plan name, or a generic order button. These facts apply to this task/date and do not establish a permanent provider restriction. Stock confirmation remains missing for new alternatives; no registration or cart/order mutation is authorized.

Additional primary-page screening:
- FirstByte public Moscow SSD page advertises189RUB/1GB or349RUB/2GB, but is superseded by the user's real billing screenshot: exclude Russia availability now.
- [SimpleCloud](https://simplecloud.ru/) advertises360RUB/1GB/20GB/unlimited, and [FAQ](https://simplecloud.ru/faq/) names Moscow/IXcellerate and SaintPetersburg/Miran2. However [offer](https://simplecloud.ru/doc/oferta.pdf) technical standards8.3 prohibits proxy/SOCKS software in broad wording. Do not recommend for this relay without clarification; current stock and included IPv4 were not verified.
- [HandyHost Russian VPS](https://handyhost.ru/linux-vps/) showsRU-KVM-1:1core/1GB/20GBNVMe,419RUB monthly or359RUB/month when paid yearly. The public order form includesSaintPetersburg andIPv4. Nevertheless its [VPS rules](https://handyhost.ru/help/vps-i-vyidelennyie-servera/pravila-ispolzovaniya-uslug-vps-i-vyidelennyix-serverov.html)2.1 prohibits proxy servers;1.18/1.21 restrict public VPN/resale. Generic WireGuard marketing does not establish private nginx relay acceptance. Exclude as an unconditional recommendation; monthly price also exceeds budget.
- [IHC](https://www.ihc.ru/kvmvds.html) live standard1GB15GB plan660RUB/month; [cheap offers](https://www.ihc.ru/cheap-vds.html) are explicitly sold out and add separateIPv4 charges.
- [Hostland](https://www.hostland.ru/vds) has dynamic public pricing, not verified order stock or a confirmed in-budget configuration. No recommendation.
- [Hostkey public current VPS list](https://hostkey.ru/documentation/server_order/vps_list/) begins490RUB forRU1GB, above budget; no live stock verification performed.
- Eurobyte pages expose daily pricing and inconsistent older monthly text; current in-budget1GB monthly order not verified. VPS.one currently lists Europe only.

Web search subsequently failedHTTP403, including the alternate connected search tool. Public-site fallback used read-only urllib/curl and local HTML/PDF parsing; all generated artifacts under `/home/slnnk/ai-data/vpn-proxy-diagnostics/`. No remote operations against the current relay were performed. Current outcome is a search gap, not a confirmed suitable provider; migration/provider selection remains open in central TODO. All subprocesses finished, no background operations.

## User selected SimpleCloud and authorized migration

The user added simplecloud-msk-01, changed DNS and requested deployment, old-relay poweroff and SID transfer. This resolves the provider-selection/budget-expansion discussion without assuming a new budget value. Prior unselected-candidate and no-deployment-permission statements are historical. Deployment and remaining DNS/monitor convergence are recorded in [migration evidence](2026-11-13-trusttunnel-de-simplecloud-relay-migration.md).
