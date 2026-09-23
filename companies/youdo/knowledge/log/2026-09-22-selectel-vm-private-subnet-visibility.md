---
system: selectel
status: verified
checked: 2026-09-22
tags: [selectel, openstack, network, subnet, global-router, vm-creation]
---
# Selectel: private subnet visibility when creating a VM

## Task

Explain why the Selectel VM creation form did not offer the existing private subnet
`172.28.0.0/24` and offered to create a new subnet instead.

## Context

- Checked: 2026-09-22 (Europe/Moscow).
- Repository: `/home/slnnk/git/selectel-tf`.
- Project: `youdo_vpc`; region: Moscow `ru-2`.
- Network: `youdo_network` (`a7d2ec39-2e7d-46f1-be0d-a3d1d75fe393`).
- Private subnet: `172.28.0.0/24` (`4cd0f32d-967d-49a8-b64e-c1cf7de3d267`).
- Cloud router: `youdo_router`, interface address `172.28.0.254`.
- The private network is also connected to a Selectel Global Router.

## Actions (investigation)

- The Selectel VM creation form showed no existing private subnets and offered
  creation of a new subnet with an address such as `192.168.0.2`.
- The network page confirmed that `172.28.0.0/24` exists and is attached to
  `youdo_router`.
- Consul Terraform state `terraform/selectel-network` also contains managed
  resources `openstack_networking_network_v2.youdo_network` and
  `openstack_networking_subnet_v2.youdo_subnet`.
- Terraform source of truth: `network/networking.tf`; production stacks resolve
  the subnet by the name `youdo_subnet` in `prod/data.tf` and related stacks.

## Findings: conclusion and checks

- The subnet is not missing. Existing subnets offered during VM creation are
  constrained by the VM location. This subnet belongs to `ru-2`; a VM created in
  another region cannot attach directly to its L2 network even when the networks
  are joined by a Global Router. The Global Router provides L3 connectivity, not
  cross-region L2 attachment.
- Verify the VM's **Name and location** block. To attach directly to this subnet,
  create the VM in Moscow `ru-2` and choose existing subnet `172.28.0.0/24`.
- If the VM must stay in another location, create a local network/subnet there,
  connect it to the same Global Router, and use a non-overlapping CIDR.
- Do not use `192.168.0.2` for a port in this subnet; choose a free address from
  `172.28.0.0/24`. Reserved/in-use addresses include the subnet gateway
  `172.28.0.1`, DNS hosts `172.28.0.6` and `.7`, cloud-router address
  `172.28.0.254`, and Selectel service addresses shown in the control panel.

## Open items (remaining uncertainty)

- The VM creation screenshot did not include the selected location. If it was
  already `ru-2`, check project selection and refresh/reopen the form; if the
  subnet still does not appear, this is likely a control-panel filtering issue
  and should be compared with `openstack subnet list` or reported to Selectel.

## Portable lesson

none
