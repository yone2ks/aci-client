import urllib3
from cobra.mit.session import LoginSession
from cobra.mit.access import MoDirectory

from .exceptions import ConnectionError, AuthenticationError


class ACIClient:
    """
    Client for interacting with Cisco ACI
    
    This class wraps Cobra SDK's MoDirectory to provide a simplified interface
    for common operations while maintaining full access to Cobra SDK functionality.
    
    Note: Automatically logs in to APIC on initialization.

    Args:
        url: APIC URL (e.g., 'https://apic.example.com')
        username: APIC username
        password: APIC password
        verify_tls: Enable TLS certificate verification (default: False)

    Raises:
        ConnectionError: If connection to APIC fails
        AuthenticationError: If authentication fails

    Primary Methods (MoDirectory wrappers):
        - lookupByClass(): Query managed objects by class name
        - lookupByDn(): Query object by DN (default: subtree='full', configOnly=True)
        - commit(): Commit configuration changes
        - query(): Execute query objects

    Example:
        >>> # Simple usage (auto-login on init)
        >>> aci = ACIClient('https://apic', 'admin', 'password')
        >>> 
        >>> # Query tenants
        >>> tenants = aci.lookupByClass('fvTenant')
        >>> for tenant in tenants:
        ...     print(tenant.name)
        >>> 
        >>> # Lookup specific object (with full subtree and config-only by default)
        >>> tenant = aci.lookupByDn('uni/tn-common')
        >>> 
        >>> # Logout when done
        >>> aci.logout()

        >>> # Using context manager (recommended for auto-cleanup)
        >>> with ACIClient('https://apic', 'admin', 'password') as aci:
        ...     tenants = aci.lookupByClass('fvTenant')
        ...     # Automatically logs out
    """

    def __init__(self, url: str, username: str, password: str, verify_tls: bool = False):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_tls = verify_tls

        if not verify_tls:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Cobra SDK objects
        self._login_session = LoginSession(self.url, self.username, self.password, secure=verify_tls)
        self._mo_dir = MoDirectory(self._login_session)

        # Auto-login on initialization
        self.login()

    def login(self):
        """
        Login to APIC
        
        Note: This is called automatically on initialization.
        You only need to call this manually if you want to reconnect after logout.

        Raises:
            ConnectionError: If connection fails
            AuthenticationError: If authentication fails
        """
        try:
            self._mo_dir.login()
        except Exception as e:
            error_msg = str(e).lower()
            if "authentication" in error_msg or "credentials" in error_msg or "login" in error_msg:
                raise AuthenticationError(f"Authentication failed: {e}")
            else:
                raise ConnectionError(f"Connection failed: {e}")

    def logout(self):
        """Logout from APIC"""
        try:
            self._mo_dir.logout()
        except Exception:
            pass  # Ignore logout errors

    def reauth(self):
        """
        Re-authenticate to extend session

        Raises:
            AuthenticationError: If re-authentication fails
        """
        try:
            self._mo_dir.reauth()
        except Exception as e:
            raise AuthenticationError(f"Re-authentication failed: {e}")

    def lookupByClass(self, className, parentDn=None, **queryParams):
        """
        Lookup managed objects by class name
        
        Wrapper for MoDirectory.lookupByClass()
        
        Args:
            className: Class name (e.g., 'fvTenant', 'fvBD', 'fvAp')
            parentDn: Parent distinguished name to scope the query
            **queryParams: Additional query parameters (propFilter, orderBy, etc.)
            
        Returns:
            List of managed objects
            
        Example:
            >>> # Get all tenants
            >>> tenants = aci.lookupByClass('fvTenant')
            >>> 
            >>> # Get tenants under specific parent
            >>> tenants = aci.lookupByClass('fvTenant', parentDn='uni')
            >>> 
            >>> # With query parameters
            >>> tenants = aci.lookupByClass('fvTenant', propFilter='eq(fvTenant.name, "common")')
        """
        return self._mo_dir.lookupByClass(className, parentDn=parentDn, **queryParams)

    def lookupByDn(self, dnStrOrDn, subtree='full', configOnly=True, **queryParams):
        """
        Lookup managed object by distinguished name
        
        Wrapper for MoDirectory.lookupByDn()
        
        Args:
            dnStrOrDn: Distinguished name as string or Dn object (e.g., 'uni/tn-common')
            subtree: Subtree scope ('full', 'children', 'no') - default: 'full'
            configOnly: Retrieve only configuration data (exclude operational data) - default: True
            **queryParams: Additional query parameters (propFilter, etc.)
            
        Returns:
            Managed object or None
            
        Example:
            >>> # Full subtree lookup (default)
            >>> tenant = aci.lookupByDn('uni/tn-common')
            >>> 
            >>> # Object only (no subtree)
            >>> tenant = aci.lookupByDn('uni/tn-common', subtree='no')
            >>> 
            >>> # Include operational data
            >>> tenant = aci.lookupByDn('uni/tn-common', configOnly=False)
        """
        return self._mo_dir.lookupByDn(dnStrOrDn, subtree=subtree, configOnly=configOnly, **queryParams)

    def commit(self, configObject, sync=False):
        """
        Commit configuration changes to APIC
        
        Wrapper for MoDirectory.commit()
        
        Args:
            configObject: ConfigRequest object with changes
            sync: If True, wait for confirmation (default: False)
            
        Returns:
            Response from APIC
            
        Example:
            >>> from cobra.mit.request import ConfigRequest
            >>> from cobra.model.fv import Tenant
            >>> config_req = ConfigRequest()
            >>> config_req.addMo(Tenant(uni, 'new-tenant'))
            >>> 
            >>> # Async commit (default)
            >>> aci.commit(config_req)
            >>> 
            >>> # Sync commit (wait for confirmation)
            >>> aci.commit(config_req, sync=True)
        """
        return self._mo_dir.commit(configObject, sync=sync)

    def query(self, queryObject):
        """
        Execute a query against APIC
        
        Wrapper for MoDirectory.query()
        
        Args:
            queryObject: Query object (DnQuery, ClassQuery, TraceQuery, etc.)
            
        Returns:
            Query results
            
        Example:
            >>> from cobra.mit.request import ClassQuery, DnQuery
            >>> 
            >>> # Class query
            >>> query = ClassQuery('fvTenant')
            >>> query.propFilter = 'eq(fvTenant.name, "common")'
            >>> tenants = aci.query(query)
            >>> 
            >>> # DN query
            >>> query = DnQuery('uni/tn-common')
            >>> query.subtree = 'full'
            >>> result = aci.query(query)
        """
        return self._mo_dir.query(queryObject)

    @property
    def mo_dir(self):
        """
        Get MoDirectory instance for direct Cobra SDK operations

        Returns:
            MoDirectory: Cobra SDK MoDirectory instance
        """
        return self._mo_dir

    def __enter__(self):
        """Context manager entry (already logged in on init)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.logout()
        return False

    def __repr__(self):
        """String representation"""
        return f"<ACIClient({self.url}, {self.username})>"
