from epp_client.schemas.base import build_epp_command, NS_DOMAIN
import xml.etree.ElementTree as ET

def check_domain(domain_name, cltrid=""):
    """Builds the XML for a domain check command."""
    domain_check = ET.Element(f"{{{NS_DOMAIN}}}check")
    name = ET.SubElement(domain_check, f"{{{NS_DOMAIN}}}name")
    name.text = domain_name
    return build_epp_command("check", domain_check, cltrid)

def info_domain(domain_name, cltrid=""):
    """Builds the XML for a domain info command."""
    domain_info = ET.Element(f"{{{NS_DOMAIN}}}info")
    name = ET.SubElement(domain_info, f"{{{NS_DOMAIN}}}name")
    name.text = domain_name
    return build_epp_command("info", domain_info, cltrid)

def create_domain(domain_name, period, ns, registrant, admin, tech, auth_info, dnssec_data=None, cltrid=""):
    """Builds the XML for a domain create command."""
    domain_create = ET.Element(f"{{{NS_DOMAIN}}}create")
    name = ET.SubElement(domain_create, f"{{{NS_DOMAIN}}}name")
    name.text = domain_name

    _period = ET.SubElement(domain_create, f"{{{NS_DOMAIN}}}period", unit="y")
    _period.text = str(period)

    ns_element = ET.SubElement(domain_create, f"{{{NS_DOMAIN}}}ns")
    for ns_host in ns:
        host_obj = ET.SubElement(ns_element, f"{{{NS_DOMAIN}}}hostObj")
        host_obj.text = ns_host

    reg_id = ET.SubElement(domain_create, f"{{{NS_DOMAIN}}}registrant")
    reg_id.text = registrant

    for contact_type, contact_id in [("admin", admin), ("tech", tech)]:
        contact = ET.SubElement(domain_create, f"{{{NS_DOMAIN}}}contact", type=contact_type)
        contact.text = contact_id

    auth = ET.SubElement(domain_create, f"{{{NS_DOMAIN}}}authInfo")
    pw = ET.SubElement(auth, f"{{{NS_DOMAIN}}}pw")
    pw.text = auth_info

    extensions = []
    if dnssec_data:
        extensions.append(dnssec_data)

    return build_epp_command("create", domain_create, cltrid, extensions=extensions)
