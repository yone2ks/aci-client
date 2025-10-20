"""
Tenant model usage example
"""
from aci_client import ACIClient
from aci_client.models import Tenant

# APIC connection details
APIC_URL = "https://sandboxapicdc.cisco.com"
USERNAME = "admin"
PASSWORD = "!v3G@!4@Y"


def main():
    """Tenant model example"""
    print(f"Connecting to APIC: {APIC_URL}")
    
    with ACIClient(APIC_URL, USERNAME, PASSWORD) as aci:
        print("✅ Connected successfully!\n")
        
        # Get all tenants from APIC
        print("📋 Fetching tenants...")
        cobra_tenants = aci.lookupByClass('fvTenant')
        
        # Convert Cobra MOs to Tenant objects
        tenants = [Tenant.from_mo(mo) for mo in cobra_tenants]
        print(f"   Found {len(tenants)} tenants\n")
        
        # Display tenant information
        for tenant in tenants[:5]:  # Show first 5
            print(f"Tenant: {tenant.name}")
            print(f"  DN: {tenant.dn}")
            print(f"  Description: {tenant.description or '(no description)'}")
            print()
        
        # Get specific tenant by DN
        print("\n🔍 Looking up 'common' tenant...")
        common_mo = aci.lookupByDn('uni/tn-common')
        if common_mo:
            common = Tenant.from_mo(common_mo)
            print(f"   Found: {common}")
            
            # Convert to dictionary
            data = common.to_dict()
            print(f"   Dictionary: {data}")
            
            # Access original Cobra object
            print(f"   Original Cobra MO: {type(common.mo).__name__}")
            print(f"   Children count: {len(list(common.mo.children))}")
        
        print("\n✅ Done!")


if __name__ == "__main__":
    main()
