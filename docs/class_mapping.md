# ACI REST API Class Name Mapping

Mapping between Cisco ACI REST API class names and aci-client data model class names.

**Naming Convention: Aligned with Ansible ACI modules**

## Tenant & Networking

| ACI REST API Class | Cobra SDK Class | Ansible Module | aci-client Model | Description |
|-------------------|-----------------|----------------|------------------|-------------|
| `fvTenant` | `cobra.model.fv.Tenant` | `aci_tenant` | `Tenant` | Tenant (logical management unit) |
| `fvAp` | `cobra.model.fv.Ap` | `aci_ap` | `AP` | Application Profile |
| `fvAEPg` | `cobra.model.fv.AEPg` | `aci_epg` | `EPG` | Endpoint Group (Application) |
| `fvBD` | `cobra.model.fv.BD` | `aci_bd` | `BD` | Bridge Domain (L2 forwarding construct) |
| `fvSubnet` | `cobra.model.fv.Subnet` | `aci_bd_subnet` | `Subnet` | Subnet |
| `fvCtx` | `cobra.model.fv.Ctx` | `aci_vrf` | `VRF` | VRF (Context/Private Network) |

## Contracts & Filters

| ACI REST API Class | Cobra SDK Class | Ansible Module | aci-client Model | Description |
|-------------------|-----------------|----------------|------------------|-------------|
| `vzBrCP` | `cobra.model.vz.BrCP` | `aci_contract` | `Contract` | Contract (EPG communication policy) |
| `vzSubj` | `cobra.model.vz.Subj` | `aci_contract_subject` | `ContractSubject` | Subject (communication rule within contract) |
| `vzFilter` | `cobra.model.vz.Filter` | `aci_filter` | `Filter` | Filter (L2-L4 communication conditions) |
| `vzEntry` | `cobra.model.vz.Entry` | `aci_filter_entry` | `FilterEntry` | Filter Entry (specific communication rule) |

## External Connectivity

| ACI REST API Class | Cobra SDK Class | Ansible Module | aci-client Model | Description |
|-------------------|-----------------|----------------|------------------|-------------|
| `l3extOut` | `cobra.model.l3ext.Out` | `aci_l3out` | `L3Out` | L3 External Connection |
| `l3extInstP` | `cobra.model.l3ext.InstP` | `aci_l3out_extepg` | `L3ExtEPG` | External EPG (L3) |
| `l3extRsEctx` | `cobra.model.l3ext.RsEctx` | - | - | L3Out to VRF relationship |
| `l2extOut` | `cobra.model.l2ext.Out` | `aci_l2out` | `L2Out` | L2 External Connection |
| `l2extInstP` | `cobra.model.l2ext.InstP` | `aci_l2out_extepg` | `L2ExtEPG` | External EPG (L2) |

## Domains

| ACI REST API Class | Cobra SDK Class | Ansible Module | aci-client Model | Description |
|-------------------|-----------------|----------------|------------------|-------------|
| `physDomP` | `cobra.model.phys.DomP` | `aci_domain` (type: phys) | `PhysDomain` | Physical Domain |
| `vmmDomP` | `cobra.model.vmm.DomP` | `aci_domain` (type: vmm) | `VMMDomain` | Virtual Machine Manager Domain |
| `l3extDomP` | `cobra.model.l3ext.DomP` | `aci_domain` (type: l3dom) | `L3Domain` | L3 Domain |
| `l2extDomP` | `cobra.model.l2ext.DomP` | `aci_domain` (type: l2dom) | `L2Domain` | L2 Domain |

## Management

| ACI REST API Class | Cobra SDK Class | Ansible Module | aci-client Model | Description |
|-------------------|-----------------|----------------|------------------|-------------|
| `mgmtInB` | `cobra.model.mgmt.InB` | `aci_node_mgmt_epg` (type: in_band) | `InBandMgmt` | In-Band Management EPG |
| `mgmtOoB` | `cobra.model.mgmt.OoB` | `aci_node_mgmt_epg` (type: out_of_band) | `OutOfBandMgmt` | Out-of-Band Management EPG |

## Fabric Access

| ACI REST API Class | Cobra SDK Class | Ansible Module | aci-client Model | Description |
|-------------------|-----------------|----------------|------------------|-------------|
| `infraAttEntityP` | `cobra.model.infra.AttEntityP` | `aci_aep` | `AEP` | Attachable Entity Profile (AEP) |
| `infraNodeP` | `cobra.model.infra.NodeP` | `aci_fabric_node` | `FabricNode` | Node Profile |
| `infraLeafP` | `cobra.model.infra.LeafP` | `aci_access_port_to_interface_policy_leaf_profile` | `LeafProfile` | Leaf Profile |
| `infraSpineP` | `cobra.model.infra.SpineP` | `aci_access_spine_interface_profile` | `SpineProfile` | Spine Profile |

## Common Attributes

Common attributes across all model classes:

| Attribute | Description |
|-----------|-------------|
| `dn` | Distinguished Name (unique identifier) |
| `name` | Object name |
| `description` | Description (descr) |
| `parent_dn` | Parent object's DN |
| `mo` | Reference to Cobra SDK Managed Object |

## Naming Conventions

### ACI REST API Class Name Pattern

- **Prefix**: Indicates package name (2-6 characters)
  - `fv`: Fabric Virtualization
  - `vz`: vz (Contract/Policy)
  - `l3ext`: Layer 3 External
  - `l2ext`: Layer 2 External
  - `infra`: Infrastructure
  - `mgmt`: Management
  - `phys`: Physical
  - `vmm`: Virtual Machine Manager

- **Body**: Object type
  - `Tenant`, `Ap`, `AEPg`, `BD`, `Ctx`, etc.

### Ansible ACI Module Naming Convention

- **Format**: `aci_<object_name>`
- Uses **snake_case**
- Examples: `aci_tenant`, `aci_bd`, `aci_epg`, `aci_vrf`

### aci-client Model Class Names

**Aligned with Ansible ACI modules**:

- **Basic Rules**:
  - Remove `aci_` prefix from Ansible module name
  - Convert to **PascalCase**
  - Examples: `aci_bd` → `BD`, `aci_epg` → `EPG`, `aci_vrf` → `VRF`

- **Handling Abbreviations**:
  - Keep common abbreviations as-is (`BD`, `EPG`, `VRF`, `AP`, `AEP`)
  - Use PascalCase for multi-word names (`ContractSubject`, `FilterEntry`)

- **Benefits**:
  - ✅ Intuitive for Ansible users
  - ✅ Easy migration from existing Ansible Playbooks
  - ✅ Short and memorable

## Implementation Priority

Phase 1 (Basic - Tenant & Networking):
1. ✅ `Tenant` (fvTenant / aci_tenant)
2. `BD` (fvBD / aci_bd)
3. `VRF` (fvCtx / aci_vrf)
4. `AP` (fvAp / aci_ap)
5. `EPG` (fvAEPg / aci_epg)
6. `Subnet` (fvSubnet / aci_bd_subnet)

Phase 2 (Policy - Contracts & Filters):
7. `Contract` (vzBrCP / aci_contract)
8. `Filter` (vzFilter / aci_filter)
9. `FilterEntry` (vzEntry / aci_filter_entry)
10. `ContractSubject` (vzSubj / aci_contract_subject)

Phase 3 (External Connectivity - L3Out):
11. `L3Out` (l3extOut / aci_l3out)
12. `L3ExtEPG` (l3extInstP / aci_l3out_extepg)

Phase 4 (Advanced Features):
12. Domains
13. Management
14. Fabric Access

## Usage Comparison

### Ansible (Before)

```yaml
- name: Create a new BD
  cisco.aci.aci_bd:
    host: apic
    username: admin
    password: password
    tenant: production
    bd: web_bd
    vrf: prod_vrf
    state: present
```

### aci-client (After)

```python
from aci_client import ACIClient
from aci_client.models import BD

aci = ACIClient('https://apic', 'admin', 'password')

# Query via Cobra SDK
bd_mo = aci.lookupByDn('uni/tn-production/BD-web_bd')

# Convert to aci-client model
bd = BD.from_mo(bd_mo)
print(bd.name)  # 'web_bd'
print(bd.tenant_name)  # 'production'
```

## References

- [Ansible cisco.aci Collection](https://docs.ansible.com/ansible/latest/collections/cisco/aci/index.html) - Naming reference
- [Cisco ACI Policy Model Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/policy-model-guide/b-Cisco-ACI-Policy-Model-Guide.html)
- [Cisco APIC REST API Configuration Guide](https://www.cisco.com/c/en/us/support/cloud-systems-management/application-policy-infrastructure-controller-apic/products-programming-reference-guides-list.html)
- [Cisco ACI Management Information Model Reference](https://developer.cisco.com/docs/aci/)
