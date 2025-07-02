"""
epp_commands.py
Version: 1.0
Author: Phil Adcock
Date: June 2025

Description:
Support functions for the nic.im OT&E test sequence. Includes correctly formatted XML
suitable for the NIC.IM EPP server.
"""

import uuid
import random
import string
import logging
import xml.etree.ElementTree as ET

def generate_cltrid():
    return str(uuid.uuid4())

def build_hello():
    return """<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <hello/>
</epp>
"""

def build_login(username, password):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <login>
      <clID>{username}</clID>
      <pw>{password}</pw>
      <options>
        <version>1.0</version>
        <lang>en</lang>
      </options>
      <services>
        <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
        <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
        <objURI>urn:ietf:params:xml:ns:host-1.0</objURI>
      </services>
    </login>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_logout():
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <logout/>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_login_with_newpw(username, current_password, new_password):
    cltrid = generate_cltrid()  # Or use "ABC" if static value preferred
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <login>
      <clID>{username}</clID>
      <pw>{current_password}</pw>
      <newPW>{new_password}</newPW>
      <options>
        <version>1.0</version>
        <lang>en</lang>
      </options>
      <svcs>
        <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
        <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
      </svcs>
    </login>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_check(domain_name):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <check>
      <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
      </domain:check>
    </check>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_info(domain_name):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <info>
      <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
      </domain:info>
    </info>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_contact_create(
    contact_id,
    name,
    org,
    email,
    voice,
    street,
    city,
    region,
    postcode,
    country_code,
    password,
    fax=None
):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <create>
      <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>{contact_id}</contact:id>
        <contact:postalInfo type="int">
          <contact:name>{name}</contact:name>
          <contact:org>{org}</contact:org>
          <contact:addr>
            <contact:street>{street}</contact:street>
            <contact:city>{city}</contact:city>
            <contact:sp>{region}</contact:sp>
            <contact:pc>{postcode}</contact:pc>
            <contact:cc>{country_code}</contact:cc>
          </contact:addr>
        </contact:postalInfo>
        <contact:voice>{voice}</contact:voice>
        <contact:fax>{fax}</contact:fax>
        <contact:email>{email}</contact:email>
        <contact:authInfo>
          <contact:pw>{password}</contact:pw>
        </contact:authInfo>
      </contact:create>
    </create>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_contact_check(contact_id):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <check>
      <contact:check xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>{contact_id}</contact:id>
      </contact:check>
    </check>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_contact_info(contact_id):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <info>
      <contact:info xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>{contact_id}</contact:id>
      </contact:info>
    </info>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_contact_delete(contact_id):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <delete>
      <contact:delete xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>{contact_id}</contact:id>
      </contact:delete>
    </delete>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_contact_update_info(
    contact_id,
    name,
    org,
    street,
    city,
    region,
    postcode,
    country_code,
    voice,
    email
):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <update>
      <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>{contact_id}</contact:id>
        <contact:chg>
          <contact:postalInfo type="int">
            <contact:name>{name}</contact:name>
            <contact:org>{org}</contact:org>
            <contact:addr>
              <contact:street>{street}</contact:street>
              <contact:city>{city}</contact:city>
              <contact:sp>{region}</contact:sp>
              <contact:pc>{postcode}</contact:pc>
              <contact:cc>{country_code}</contact:cc>
            </contact:addr>
          </contact:postalInfo>
          <contact:voice>{voice}</contact:voice>
          <contact:email>{email}</contact:email>
        </contact:chg>
      </contact:update>
    </update>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_create(
    domain_name,
    period,
    auth_info,
    registrant_contact,
    admin_contact,
    tech_contact,
    billing_contact,
    nameservers
):
    cltrid = generate_cltrid()
    ns_block = build_ns(nameservers)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <create>
      <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
        <domain:period unit="y">{period}</domain:period>
{ns_block}
        <domain:registrant>{registrant_contact}</domain:registrant>
        <domain:contact type="admin">{admin_contact}</domain:contact>
        <domain:contact type="tech">{tech_contact}</domain:contact>
        <domain:contact type="billing">{billing_contact}</domain:contact>
        <domain:authInfo>
          <domain:pw>{auth_info}</domain:pw>
        </domain:authInfo>
      </domain:create>
    </create>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_create_no_authcode(
    domain_name,
    period,
    auth_info,
    registrant_contact,
    admin_contact,
    tech_contact,
    billing_contact,
    nameservers
):
    cltrid = generate_cltrid()
    ns_block = build_ns(nameservers)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <create>
      <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
        <domain:period unit="y">{period}</domain:period>
{ns_block}
        <domain:registrant>{registrant_contact}</domain:registrant>
        <domain:contact type="admin">{admin_contact}</domain:contact>
        <domain:contact type="tech">{tech_contact}</domain:contact>
        <domain:contact type="billing">{billing_contact}</domain:contact>
      </domain:create>
    </create>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_delete(domain_name):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <delete>
      <domain:delete xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
      </domain:delete>
    </delete>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_renew(domain_name, cur_exp_date, period):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <renew>
      <domain:renew xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
        <domain:curExpDate>{cur_exp_date}</domain:curExpDate>
        <domain:period unit="y">{period}</domain:period>
      </domain:renew>
    </renew>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_transfer_old(domain_name, op, auth_info=None, period=None):
    cltrid = generate_cltrid()
    auth_xml = f"<domain:authInfo><domain:pw>{auth_info}</domain:pw></domain:authInfo>" if auth_info else ""
    period_xml = f"<domain:period unit=\"y\">{period}</domain:period>" if period else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <transfer op="{op}">
      <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
        {period_xml}
        {auth_xml}
      </domain:transfer>
    </transfer>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""

def build_domain_transfer(domain_name, auth_info):
    cltrid = generate_cltrid()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <transfer op="request">
      <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
        <domain:authInfo>
          <domain:pw roid="">{auth_info}</domain:pw>
        </domain:authInfo>
      </domain:transfer>
    </transfer>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""


def build_domain_update(
        domain_name,
        add_ns=None,
        rem_ns=None,
        add_contacts=None,
        rem_contacts=None,
        add_statuses=None,
        rem_statuses=None,
        changereg=None,
        changepw=None,
        status_message=None
):
    """
    Builds a <domain:update> EPP request.

    - add_ns/rem_ns: list of nameserver hostnames
    - add_contacts/rem_contacts: dict {type: contact_id}, e.g. {"admin": "cid001", "tech": "cid002"}
    - add_statuses/rem_statuses: list of EPP domain statuses to add/remove
    - changereg: new registrant contact ID
    - changepw: new authInfo password
    - status_message: optional human-readable message (e.g., "Payment Overdue") to include with <domain:status>
    """
    cltrid = generate_cltrid()

    # Construct <add>
    add_parts = []
    if add_ns:
        add_parts.append(
            "<domain:ns>" + "".join(f"<domain:hostAttr><domain:hostName>{ns}</domain:hostName></domain:hostAttr>" for ns in add_ns) + "</domain:ns>")
    if add_contacts:
        add_parts += [f'<domain:contact type="{ctype}">{cid}</domain:contact>' for ctype, cid in add_contacts.items()]
    if add_statuses:
        add_parts += [
            f'<domain:status s="{s}" lang="en">{status_message}</domain:status>' if status_message else f'<domain:status s="{s}" />'
            for s in add_statuses
        ]
    add_xml = f"<domain:add>{''.join(add_parts)}</domain:add>" if add_parts else ""

    # Construct <rem>
    rem_parts = []
    if rem_ns:
        rem_parts.append(
            "<domain:ns>" + "".join(f"<domain:hostAttr><domain:hostName>{ns}</domain:hostName></domain:hostAttr>" for ns in rem_ns) + "</domain:ns>")
    if rem_contacts:
        rem_parts += [f'<domain:contact type="{ctype}">{cid}</domain:contact>' for ctype, cid in rem_contacts.items()]
    if rem_statuses:
        rem_parts += [f'<domain:status s="{s}" />' for s in rem_statuses]
    rem_xml = f"<domain:rem>{''.join(rem_parts)}</domain:rem>" if rem_parts else ""

    # Construct <chg>
    chg_parts = []
    if changereg:
        chg_parts.append(f"<domain:registrant>{changereg}</domain:registrant>")
    if changepw:
        chg_parts.append(f"<domain:authInfo><domain:pw>{changepw}</domain:pw></domain:authInfo>")
    chg_xml = f"<domain:chg>{''.join(chg_parts)}</domain:chg>" if chg_parts else ""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <update>
      <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>{domain_name}</domain:name>
        {add_xml}
        {rem_xml}
        {chg_xml}
      </domain:update>
    </update>
    <clTRID>{cltrid}</clTRID>
  </command>
</epp>
"""


# Helper functions
def build_ns(nameservers):
    """
    Returns a <domain:ns> XML block with <domain:hostAttr> elements.
    Example input: ["ns1.example.org", "ns2.example.org"]
    """
    ns_entries = "\n".join(
        f"""    <domain:hostAttr>
      <domain:hostName>{ns}</domain:hostName>
    </domain:hostAttr>""" for ns in nameservers
    )
    return f"""  <domain:ns>
{ns_entries}
  </domain:ns>
"""

def generate_contact_id():
    """
    Generate a random contact ID in the format: CIMxxxxxx-IM
    Where 'xxxxxx' is a mix of lowercase letters and digits
    """
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"CIM{suffix}-IM"

# These helper functions are used with build_domain_update
def domain_chg_registrant_xml(contact_id):
    return f"""<domain:chg>
  <domain:registrant>{contact_id}</domain:registrant>
</domain:chg>
"""

def domain_add_ns_xml(nameservers):
    return f"""<domain:add>
  <domain:ns>
    {''.join(f'<domain:hostObj>{ns}</domain:hostObj>' for ns in nameservers)}
  </domain:ns>
</domain:add>
"""

def domain_add_status_xml(statuses):
    return f"""<domain:add>
  {''.join(f'<domain:status s="{s}" />' for s in statuses)}
</domain:add>
"""

def domain_rem_status_xml(statuses):
    return f"""<domain:rem>
  {''.join(f'<domain:status s="{s}" />' for s in statuses)}
</domain:rem>
"""

def domain_chg_authinfo_xml(new_pw):
    return f"""<domain:chg>
  <domain:authInfo>
    <domain:pw>{new_pw}</domain:pw>
  </domain:authInfo>
</domain:chg>
"""

def extract_expiry_date_from_domain_create_response(xml_response):
    """
    Extracts the <domain:exDate> value from a domain create response.
    Returns the expiry date string in 'YYYY-MM-DD' format.
    """
    try:
        ns = {
            'domain': 'urn:ietf:params:xml:ns:domain-1.0'
        }
        root = ET.fromstring(xml_response)
        ex_date = root.find('.//domain:exDate', ns)
        if ex_date is not None:
            return ex_date.text.strip().split('T')[0]  # strip timestamp if present
        else:
            return None
    except Exception as e:
        logging.error("Error parsing domain:exDate: %s", e)
        return None
