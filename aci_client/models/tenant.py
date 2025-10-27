from dataclasses import dataclass
from typing import ClassVar, Optional
from cobra.model.fv import Tenant as FvTenant


@dataclass(frozen=True)
class Tenant:
    """
    Tenant data model
    
    Represents a Cisco ACI Tenant (fvTenant) with simplified access to properties.
    
    This is an immutable data class that wraps Cobra SDK's fvTenant object.
    
    Attributes:
        dn: Distinguished name (e.g., 'uni/tn-common')
        name: Tenant name
        description: Tenant description
        parent_dn: Parent distinguished name (always 'uni' for tenants).
                   Kept as a field for consistency with other model classes (e.g., BridgeDomain, EPG)
        mo: Original Cobra SDK Tenant object (fvTenant)
    
    Example:
        >>> # Create from Cobra MO
        >>> cobra_tenant = aci.lookupByDn('uni/tn-common')
        >>> tenant = Tenant.from_mo(cobra_tenant)
        >>> print(tenant.name)
        'common'
        
        >>> # Access original Cobra object
        >>> print(tenant.mo.name)
        'common'
    """
    CLASSNAME: ClassVar[str] = FvTenant.meta.moClassName  # 'fvTenant'
    PREFIX: ClassVar[str] = FvTenant.meta.rnPrefixes[0][0]   # 'tn-'
    
    # Instance attributes
    dn: str
    name: str
    description: str = ""
    parent_dn: str = "uni"
    mo: Optional[FvTenant] = None
    
    def __post_init__(self):
        """Validate DN and name consistency"""
        expected_dn = f"uni/{self.PREFIX}{self.name}"
        if self.dn != expected_dn:
            raise ValueError(
                f"DN '{self.dn}' does not match name '{self.name}'. "
                f"Expected '{expected_dn}'"
            )
    
    @classmethod
    def from_mo(cls, mo: FvTenant) -> "Tenant":
        """
        Create Tenant from Cobra MO (Managed Object)
        
        Args:
            mo: Cobra SDK fvTenant object
            
        Returns:
            Tenant instance
            
        Example:
            >>> cobra_tenant = aci.lookupByDn('uni/tn-common')
            >>> tenant = Tenant.from_mo(cobra_tenant)
        """
        return cls(
            dn=str(mo.dn),
            name=mo.name,
            description=mo.descr or "",
            parent_dn=str(mo.parentDn) if hasattr(mo, 'parentDn') else "uni",
            mo=mo,
        )
    
    def to_dict(self, include_mo: bool = False) -> dict:
        """
        Convert to dictionary
        
        Args:
            include_mo: Include Managed Object (default: False)
        
        Returns:
            Dictionary representation
            
        Example:
            >>> tenant = Tenant(dn='uni/tn-test', name='test')
            >>> tenant.to_dict()
            {'dn': 'uni/tn-test', 'name': 'test', 'description': '', 'parent_dn': 'uni'}
            
            >>> tenant.to_dict(include_mo=True)
            {'dn': 'uni/tn-test', 'name': 'test', 'description': '', 'parent_dn': 'uni', 'mo': <FvTenant>}
        """
        data = {
            'dn': self.dn,
            'name': self.name,
            'description': self.description,
            'parent_dn': self.parent_dn,
        }
        if include_mo:
            data['mo'] = self.mo
        return data
    
    def __str__(self) -> str:
        """String representation"""
        return f"Tenant(name='{self.name}', dn='{self.dn}')"
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return (
            f"Tenant(dn='{self.dn}', name='{self.name}', "
            f"description='{self.description}')"
        )
