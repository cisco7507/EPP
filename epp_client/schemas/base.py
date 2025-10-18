import xml.etree.ElementTree as ET
from xml.dom import minidom

# EPP XML Namespaces
NS_EPP = "urn:ietf:params:xml:ns:epp-1.0"
NS_DOMAIN = "urn:ietf:params:xml:ns:domain-1.0"
NS_CONTACT = "urn:ietf:params:xml:ns:contact-1.0"
NS_HOST = "urn:ietf:params:xml:ns:host-1.0"
NS_SEC_DNS = "urn:ietf:params:xml:ns:secDNS-1.1"

def register_namespaces():
    """Registers the EPP namespaces with ElementTree."""
    ET.register_namespace("epp", NS_EPP)
    ET.register_namespace("domain", NS_DOMAIN)
    ET.register_namespace("contact", NS_CONTACT)
    ET.register_namespace("host", NS_HOST)
    ET.register_namespace("secDNS", NS_SEC_DNS)

def build_epp_command(command_name, command_data, cltrid="", extensions=None):
    """Builds a generic EPP command XML."""
    register_namespaces()

    epp = ET.Element(f"{{{NS_EPP}}}epp")
    command = ET.SubElement(epp, f"{{{NS_EPP}}}command")

    cmd_element = ET.SubElement(command, f"{{{NS_EPP}}}{command_name}")

    # Add command-specific data
    if command_data is not None:
        cmd_element.append(command_data)

    if extensions:
        extension_element = ET.SubElement(command, f"{{{NS_EPP}}}extension")
        for ext in extensions:
            extension_element.append(ext)

    if cltrid:
        cltrid_element = ET.SubElement(command, f"{{{NS_EPP}}}clTRID")
        cltrid_element.text = cltrid

    # Pretty print XML
    xml_str = ET.tostring(epp, 'utf-8')
    reparsed = minidom.parseString(xml_str)
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode('utf-8')

def parse_epp_response(xml_response):
    """Parses an EPP response and returns the root element."""
    return ET.fromstring(xml_response)

# Example of how to create a more specific command builder
def build_login_xml(username, password, cltrid=""):
    """Builds the EPP login command."""
    login_data = ET.Element(f"{{{NS_EPP}}}login")
    cl_id = ET.SubElement(login_data, f"{{{NS_EPP}}}clID")
    cl_id.text = username
    pw = ET.SubElement(login_data, f"{{{NS_EPP}}}pw")
    pw.text = password

    options = ET.SubElement(login_data, f"{{{NS_EPP}}}options")
    version = ET.SubElement(options, f"{{{NS_EPP}}}version")
    version.text = "1.0"
    lang = ET.SubElement(options, f"{{{NS_EPP}}}lang")
    lang.text = "en"

    svcs = ET.SubElement(login_data, f"{{{NS_EPP}}}svcs")
    obj_uri_domain = ET.SubElement(svcs, f"{{{NS_EPP}}}objURI")
    obj_uri_domain.text = NS_DOMAIN
    obj_uri_contact = ET.SubElement(svcs, f"{{{NS_EPP}}}objURI")
    obj_uri_contact.text = NS_CONTACT
    obj_uri_host = ET.SubElement(svcs, f"{{{NS_EPP}}}objURI")
    obj_uri_host.text = NS_HOST

    return build_epp_command("login", login_data, cltrid)

def build_logout_xml(cltrid=""):
    """Builds the EPP logout command."""
    return build_epp_command("logout", None, cltrid)
