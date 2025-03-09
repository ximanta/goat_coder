"""Tests for Java name convention conversion.

This module tests the conversion of Python snake_case names to Java camelCase,
covering various edge cases and special scenarios.
"""

import pytest
from main.type_mapping_system.java.java_name_converter import to_java_name

def test_basic_conversion():
    """Test basic snake_case to camelCase conversion."""
    assert to_java_name("hello_world") == "helloWorld"
    assert to_java_name("convert_to_int") == "convertToInt"
    assert to_java_name("parse_json") == "parseJson"

def test_single_word():
    """Test single word names without underscores."""
    assert to_java_name("hello") == "hello"
    assert to_java_name("test") == "test"
    assert to_java_name("function") == "function"

def test_multiple_underscores():
    """Test names with multiple consecutive underscores."""
    assert to_java_name("hello__world") == "helloWorld"
    assert to_java_name("test___function") == "testFunction"
    assert to_java_name("multiple___underscore___test") == "multipleUnderscoreTest"

def test_leading_trailing_underscores():
    """Test names with leading and/or trailing underscores."""
    assert to_java_name("_hello_world") == "helloWorld"
    assert to_java_name("hello_world_") == "helloWorld"
    assert to_java_name("_hello_world_") == "helloWorld"
    assert to_java_name("__test__") == "test"

def test_mixed_case_input():
    """Test handling of mixed case input."""
    assert to_java_name("Hello_World") == "helloWorld"
    assert to_java_name("HELLO_WORLD") == "helloWorld"
    assert to_java_name("hello_WORLD") == "helloWorld"
    assert to_java_name("hElLo_wOrLd") == "helloWorld"

def test_numbers():
    """Test names containing numbers."""
    assert to_java_name("convert_2_int") == "convert2Int"
    assert to_java_name("parse_number_123") == "parseNumber123"
    assert to_java_name("test_42_function") == "test42Function"
    assert to_java_name("array_2d") == "array2d"

def test_special_characters():
    """Test handling of special characters (should be removed or handled appropriately)."""
    with pytest.raises(ValueError):
        to_java_name("hello@world")
    with pytest.raises(ValueError):
        to_java_name("test$function")
    with pytest.raises(ValueError):
        to_java_name("special#case")

def test_empty_components():
    """Test empty string components between underscores."""
    assert to_java_name("hello__") == "hello"
    assert to_java_name("__hello") == "hello"
    assert to_java_name("hello__world__test__") == "helloWorldTest"

def test_acronyms():
    """Test handling of common acronyms."""
    assert to_java_name("convert_xml_to_json") == "convertXmlToJson"
    assert to_java_name("parse_html_url") == "parseHtmlUrl"
    assert to_java_name("get_api_response") == "getApiResponse"

def test_edge_cases():
    """Test various edge cases."""
    # Empty string
    with pytest.raises(ValueError):
        to_java_name("")
    
    # Only underscores
    with pytest.raises(ValueError):
        to_java_name("_")
    with pytest.raises(ValueError):
        to_java_name("___")
    
    # Whitespace
    with pytest.raises(ValueError):
        to_java_name("hello world")
    with pytest.raises(ValueError):
        to_java_name("test\tfunction")
    with pytest.raises(ValueError):
        to_java_name("\n")

def test_java_keywords():
    """Test conversion of names that could conflict with Java keywords."""
    assert to_java_name("public_method") == "publicMethod"
    assert to_java_name("class_name") == "className"
    assert to_java_name("package_info") == "packageInfo"
    assert to_java_name("interface_definition") == "interfaceDefinition"

def test_type_prefixes():
    """Test handling of common type prefixes."""
    assert to_java_name("int_value") == "intValue"
    assert to_java_name("string_builder") == "stringBuilder"
    assert to_java_name("boolean_flag") == "booleanFlag"
    assert to_java_name("list_items") == "listItems"

def test_preserve_camel_case():
    """Test that existing camelCase names are preserved."""
    assert to_java_name("maxNumber") == "maxNumber"
    assert to_java_name("inputString") == "inputString"
    assert to_java_name("numElements") == "numElements"
    assert to_java_name("isValid") == "isValid"
