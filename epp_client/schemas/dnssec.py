import xml.etree.ElementTree as ET
from .base import NS_SEC_DNS

def create_dnssec_data(ds_records):
    """Builds the DNSSEC create data for a domain."""
    sec_create = ET.Element(f"{{{NS_SEC_DNS}}}create")
    for ds in ds_records:
        ds_data = ET.SubElement(sec_create, f"{{{NS_SEC_DNS}}}dsData")
        key_tag = ET.SubElement(ds_data, f"{{{NS_SEC_DNS}}}keyTag")
        key_tag.text = str(ds['keyTag'])
        alg = ET.SubElement(ds_data, f"{{{NS_SEC_DNS}}}alg")
        alg.text = str(ds['alg'])
        digest_type = ET.SubElement(ds_data, f"{{{NS_SEC_DNS}}}digestType")
        digest_type.text = str(ds['digestType'])
        digest = ET.SubElement(ds_data, f"{{{NS_SEC_DNS}}}digest")
        digest.text = ds['digest']
    return sec_create
