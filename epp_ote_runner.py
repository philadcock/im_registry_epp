"""
epp_ote_runner.py
Version: 1.0
Author: Phil Adcock
Date: June 2025

Description:
Main script to execute NIC.IM EPP OT&E test sequence. Connects to the test server and runs all
required EPP operations in order.
"""

import socket
import ssl
import logging
import time
import struct
import uuid
from epp_commands import *
from xml.dom import minidom
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

HOST = ""           # Enter hostname of EPP server here
PORT = 700
CLIENT_ID = ""      # Enter username supplied by NIC.IM registry here
PASSWORD = ""       # Enter password supplied by NIC.IM registry here
NEW_PASSWORD = ""   # Create a new password here for OT&E test

class EppClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.ssl_sock = None

    def connect(self):
        logging.info("Connecting to %s:%d", self.host, self.port)
        raw_sock = socket.create_connection((self.host, self.port))
        context = ssl.create_default_context()
        self.ssl_sock = context.wrap_socket(raw_sock, server_hostname=self.host)
        logging.info("Connected.")
        greeting = self.read()
        try:
            formatted_greeting = minidom.parseString(greeting).toprettyxml(indent="  ")
        except Exception:
            formatted_greeting = greeting  # fallback if not valid XML
        logging.info("Server Greeting:\n%s", formatted_greeting)

    def send(self, xml):
        data = xml.encode("utf-8")
        total_len = len(data) + 4
        header = struct.pack("!I", total_len)
        self.ssl_sock.sendall(header + data)

    def read(self):
        header = self.ssl_sock.recv(4)
        if len(header) < 4:
            raise ConnectionError("Failed to read message length header.")
        total_len = struct.unpack("!I", header)[0]
        payload_len = total_len - 4
        response = b""
        while len(response) < payload_len:
            chunk = self.ssl_sock.recv(payload_len - len(response))
            if not chunk:
                raise ConnectionError("Unexpected disconnect during response read.")
            response += chunk
        return response.decode("utf-8")

    def disconnect(self):
        if self.ssl_sock:
            self.ssl_sock.close()
        logging.info("Disconnected.")

def send_and_expect(client, xml, expected_code="1000", expect_result_code=True):
    logging.info("Sending:\n%s", xml)
    client.send(xml)
    response = client.read()

    try:
        formatted_response = minidom.parseString(response).toprettyxml(indent="  ")
    except Exception:
        formatted_response = response  # fallback if not valid XML

    logging.info("Received:\n%s", formatted_response)
    if expect_result_code and f'result code="{expected_code}"' not in response:
        logging.error("Expected code %s but got:\n%s", expected_code, response)
        raise SystemExit(1)

def get_expiry_date_from_info(client, domain):
    logging.info("Requesting domain info for expiry date...")
    xml = build_domain_info(domain)
    logging.info("Sending:\n%s", xml)
    client.send(xml)
    response = client.read()
    logging.info("Received:\n%s", response)

    try:
        root = ET.fromstring(response)
        ns = {'domain': 'urn:ietf:params:xml:ns:domain-1.0'}
        exdate = root.find('.//domain:exDate', ns)
        if exdate is None:
            logging.error("No <domain:exDate> found in domain info response.")
            raise SystemExit(1)
        return exdate.text.split('T')[0]  # Extract YYYY-MM-DD
    except Exception as e:
        logging.error("Failed to parse expiry date: %s", e)
        raise SystemExit(1)

def run_ote_sequence():
    client = EppClient(HOST, PORT)
    client.connect()

    send_and_expect(client, build_login(CLIENT_ID, PASSWORD))
    send_and_expect(client, build_hello(), expect_result_code=False)
    send_and_expect(client, build_logout(), expected_code="1500")

    client.connect()
    send_and_expect(client, build_login_with_newpw(CLIENT_ID, PASSWORD, NEW_PASSWORD))
    send_and_expect(client, build_logout(), expected_code="1500")

    client.connect()
    send_and_expect(client, build_login(CLIENT_ID, NEW_PASSWORD))
    send_and_expect(client, build_hello(), expect_result_code=False)
    send_and_expect(client, build_domain_create("deleteme.im", 1, "abc123","dom001", "dom002","dom003", "dom004",["ns1.example.org", "ns2.example.org"]))
    send_and_expect(client, build_domain_create("maximum.im", 10, "abc123", "dom001", "dom002", "dom003", "dom004",["ns1.example.org", "ns2.example.org"]))
    send_and_expect(client, build_domain_create("abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxy.im", 1, "abc123", "dom001", "dom002", "dom003", "dom004",["ns1.example.org", "ns2.example.org"]))
    send_and_expect(client, build_domain_check("xyz123.im"))
    send_and_expect(client, build_domain_check("advsys.co.im"))
    send_and_expect(client, build_domain_info("domicilium.im"))

    expiry = get_expiry_date_from_info(client, "renewme.im")
    send_and_expect(client, build_domain_renew("renewme.im", expiry, 10))
    send_and_expect(client, build_domain_delete("deleteme.im"))
    send_and_expect(client, build_domain_transfer("epp.im", "qazxsw"))
    send_and_expect(client, build_domain_info("epp.im"))
    send_and_expect(client, build_domain_update("epp.im", add_contacts={"admin": "CH1234"}))

    send_and_expect(client, build_domain_update("epp.im", add_statuses=["clientUpdateProhibited"], status_message="Payment Overdue"))
    send_and_expect(client, build_domain_info("epp.im"))
    send_and_expect(client, build_domain_update("epp.im", rem_statuses=["clientUpdateProhibited"]))
    send_and_expect(client, build_domain_update("epp.im", add_ns=[("ns1.epp.im", "10.0.0.1")]))
    send_and_expect(client, build_domain_update("epp.im", add_ns=["ns1.example.org"]))
    send_and_expect(client, build_domain_info("epp.im"))
    send_and_expect(client, build_domain_update("epp.im", rem_ns=[("ns1.epp.im", "10.0.0.1")]))


    send_and_expect(client, build_contact_create("HAR001", "Chris Harper", "Harper Industries", "charper@domicilium.com", "01624823833", ["Domicilium House", "Malew Street"], "Castletown", "Isle of Man", "IM9 1AE", "GB", "qwertyuiop", "01624823899"))
    send_and_expect(client, build_domain_create_no_authcode("exception.im", 1, "", "dom001", "dom002", "dom003", "dom004", ["ns1.example.org", "ns2.example.org"]), expected_code="2400")
    send_and_expect(client, build_domain_transfer("transfer3.im", "1234"), expected_code="2400")
    send_and_expect(client, build_domain_create("1ylewOAxia8rl38rle2iesluql1broesoeGie6ROAs4oaBro6bluviespLAxiUstl.im", 1, "abc123", "dom001", "dom002", "dom003", "dom004", ["ns1.example.org", "ns2.example.org"]), expected_code="2400")
    send_and_expect(client, build_contact_create("JS1234", "John Smith", "Acme Widgets", "jsmith@acmewidgets.com", "01624823833", ["Acme House", "Acme Street"], "Castletown", "Isle of Man", "IM9 1AE", None, "qwertyuiop", "01624823899"), expected_code="2002")

    client.disconnect()
    logging.info("OT&E Test completed successfully.")


if __name__ == '__main__':
    run_ote_sequence()
