"""
Tests for Tenant model
"""
import pytest
from unittest.mock import Mock
from aci_client.models.tenant import Tenant


def test_tenant_creation():
    """Test basic tenant creation"""
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        description='Test tenant'
    )
    
    assert tenant.dn == 'uni/tn-test'
    assert tenant.name == 'test'
    assert tenant.description == 'Test tenant'
    assert tenant.parent_dn == 'uni'
    assert tenant.mo is None


def test_tenant_defaults():
    """Test tenant with default values"""
    tenant = Tenant(dn='uni/tn-test', name='test')
    
    assert tenant.description == ""
    assert tenant.parent_dn == "uni"
    assert tenant.mo is None


def test_tenant_validation():
    """Test DN and name validation"""
    # Valid tenant
    tenant = Tenant(dn='uni/tn-test', name='test')
    assert tenant.name == 'test'
    
    # Invalid DN (doesn't match name)
    with pytest.raises(ValueError, match="DN.*does not match name"):
        Tenant(dn='uni/tn-wrong', name='test')


def test_tenant_from_mo():
    """Test creating tenant from Cobra MO"""
    # Mock Cobra MO
    mock_mo = Mock()
    mock_mo.dn = 'uni/tn-common'
    mock_mo.name = 'common'
    mock_mo.descr = 'Common tenant'
    mock_mo.parentDn = 'uni'
    
    tenant = Tenant.from_mo(mock_mo)
    
    assert tenant.dn == 'uni/tn-common'
    assert tenant.name == 'common'
    assert tenant.description == 'Common tenant'
    assert tenant.parent_dn == 'uni'
    assert tenant.mo == mock_mo


def test_tenant_from_mo_no_description():
    """Test creating tenant from MO with no description"""
    mock_mo = Mock()
    mock_mo.dn = 'uni/tn-test'
    mock_mo.name = 'test'
    mock_mo.descr = None
    mock_mo.parentDn = 'uni'
    
    tenant = Tenant.from_mo(mock_mo)
    
    assert tenant.description == ""
    assert tenant.parent_dn == "uni"


def test_tenant_to_dict():
    """Test converting tenant to dictionary"""
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        description='Test tenant'
    )
    
    result = tenant.to_dict()
    
    assert result == {
        'dn': 'uni/tn-test',
        'name': 'test',
        'description': 'Test tenant',
        'parent_dn': 'uni',
    }
    assert 'mo' not in result


def test_tenant_to_dict_include_mo():
    """Test converting tenant to dictionary with mo"""
    mock_mo = Mock()
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        mo=mock_mo
    )
    
    result = tenant.to_dict(include_mo=True)
    
    assert result['mo'] == mock_mo
    assert result['name'] == 'test'


def test_tenant_str():
    """Test string representation"""
    tenant = Tenant(dn='uni/tn-test', name='test')
    
    assert str(tenant) == "Tenant(name='test', dn='uni/tn-test')"


def test_tenant_repr():
    """Test developer representation"""
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        description='Test tenant'
    )
    
    repr_str = repr(tenant)
    assert 'uni/tn-test' in repr_str
    assert 'test' in repr_str
    assert 'Test tenant' in repr_str


def test_tenant_immutability():
    """Test that tenant is immutable (frozen)"""
    tenant = Tenant(dn='uni/tn-test', name='test')
    
    # Should not be able to modify fields
    with pytest.raises(Exception):  # FrozenInstanceError
        tenant.name = 'changed'
    
    with pytest.raises(Exception):
        tenant.description = 'changed'


def test_tenant_class_constants():
    """Test Cobra SDK metadata constants"""
    # Test CLASSNAME constant
    assert Tenant.CLASSNAME == 'fvTenant'
    assert isinstance(Tenant.CLASSNAME, str)
    
    # Test PREFIX constant (extracted from tuple format)
    assert Tenant.PREFIX == 'tn-'
    assert isinstance(Tenant.PREFIX, str)
    
    # Verify PREFIX is used correctly in DN construction
    tenant = Tenant(dn='uni/tn-production', name='production')
    assert tenant.dn == f"uni/{Tenant.PREFIX}{tenant.name}"
    
    # Test DN validation uses PREFIX
    expected_dn = f"uni/{Tenant.PREFIX}production"
    assert expected_dn == 'uni/tn-production'
