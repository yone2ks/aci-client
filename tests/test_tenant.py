"""
Tests for Tenant model
"""
import json
import pytest
from unittest.mock import Mock, patch
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


@patch('aci_client.models.tenant.toJSONStr')
def test_tenant_to_json_pretty(mock_tojsonstr):
    """Test to_json method with pretty formatting"""
    # Mock the toJSONStr function
    mock_json_data = {
        "fvTenant": {
            "attributes": {
                "dn": "uni/tn-test",
                "name": "test",
                "descr": "Test tenant"
            }
        }
    }
    mock_tojsonstr.return_value = json.dumps(mock_json_data, indent=2)
    
    # Create tenant with mock MO
    mock_mo = Mock()
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        description='Test tenant',
        mo=mock_mo
    )
    
    # Test pretty formatting (default)
    result = tenant.to_json()
    
    # Verify toJSONStr was called with correct parameters
    mock_tojsonstr.assert_called_once_with(mock_mo, prettyPrint=True)
    
    # Verify result is formatted JSON
    assert '"fvTenant"' in result
    assert '"attributes"' in result
    assert '"dn": "uni/tn-test"' in result
    assert '"name": "test"' in result


@patch('aci_client.models.tenant.toJSONStr')
def test_tenant_to_json_compact(mock_tojsonstr):
    """Test to_json method with compact formatting"""
    # Mock the toJSONStr function
    mock_json_data = {
        "fvTenant": {
            "attributes": {
                "dn": "uni/tn-test",
                "name": "test"
            }
        }
    }
    mock_tojsonstr.return_value = json.dumps(mock_json_data)
    
    # Create tenant with mock MO
    mock_mo = Mock()
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        mo=mock_mo
    )
    
    # Test compact formatting
    result = tenant.to_json(pretty=False)
    
    # Verify toJSONStr was called with correct parameters
    mock_tojsonstr.assert_called_once_with(mock_mo, prettyPrint=False)
    
    # Verify result is compact JSON
    assert '"fvTenant"' in result
    assert result.count('\n') == 0  # No newlines in compact format


def test_tenant_to_json_no_mo():
    """Test to_json method raises error when no MO is available"""
    tenant = Tenant(
        dn='uni/tn-test',
        name='test'
    )
    
    # Should raise ValueError when mo is None
    with pytest.raises(ValueError, match="No Cobra MO available"):
        tenant.to_json()


@patch('aci_client.models.tenant.toJSONStr')
def test_tenant_to_json_error_handling(mock_tojsonstr):
    """Test to_json method error handling"""
    # Mock toJSONStr to raise an exception
    mock_tojsonstr.side_effect = Exception("JSON conversion failed")
    
    # Create tenant with mock MO
    mock_mo = Mock()
    tenant = Tenant(
        dn='uni/tn-test',
        name='test',
        mo=mock_mo
    )
    
    # Should raise RuntimeError with wrapped exception
    with pytest.raises(RuntimeError, match="Failed to convert to ACI JSON"):
        tenant.to_json()


@patch('aci_client.models.tenant.toJSONStr')
def test_tenant_to_json_real_format(mock_tojsonstr):
    """Test to_json method with realistic ACI JSON format"""
    # Mock realistic ACI JSON response
    mock_json_data = {
        "fvTenant": {
            "attributes": {
                "annotation": "",
                "descr": "Production tenant",
                "dn": "uni/tn-production",
                "name": "production",
                "nameAlias": "",
                "ownerKey": "",
                "ownerTag": ""
            },
            "children": []
        }
    }
    mock_tojsonstr.return_value = json.dumps(mock_json_data, indent=2)
    
    # Create tenant with mock MO
    mock_mo = Mock()
    tenant = Tenant(
        dn='uni/tn-production',
        name='production',
        description='Production tenant',
        mo=mock_mo
    )
    
    # Test JSON output
    result = tenant.to_json()
    
    # Parse result to verify structure
    parsed = json.loads(result)
    
    assert "fvTenant" in parsed
    assert "attributes" in parsed["fvTenant"]
    assert parsed["fvTenant"]["attributes"]["dn"] == "uni/tn-production"
    assert parsed["fvTenant"]["attributes"]["name"] == "production"
    assert parsed["fvTenant"]["attributes"]["descr"] == "Production tenant"


@patch('aci_client.models.tenant.toJSONStr')
def test_tenant_to_json_from_mo_integration(mock_tojsonstr):
    """Test to_json method with tenant created from MO"""
    # Mock realistic JSON output
    mock_json_data = {
        "fvTenant": {
            "attributes": {
                "dn": "uni/tn-common",
                "name": "common",
                "descr": "Common tenant"
            }
        }
    }
    mock_tojsonstr.return_value = json.dumps(mock_json_data, indent=2)
    
    # Create mock MO
    mock_mo = Mock()
    mock_mo.dn = 'uni/tn-common'
    mock_mo.name = 'common'
    mock_mo.descr = 'Common tenant'
    mock_mo.parentDn = 'uni'
    
    # Create tenant from MO
    tenant = Tenant.from_mo(mock_mo)
    
    # Test JSON conversion
    result = tenant.to_json()
    
    # Verify toJSONStr was called with the original MO
    mock_tojsonstr.assert_called_once_with(mock_mo, prettyPrint=True)
    
    # Verify JSON structure
    parsed = json.loads(result)
    assert parsed["fvTenant"]["attributes"]["name"] == "common"
