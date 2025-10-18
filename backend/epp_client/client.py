import socket
import ssl
import struct
import xml.etree.ElementTree as ET
import logging
from .schemas.base import build_login_xml, build_logout_xml, build_epp_command
from .exceptions import EPPError

log = logging.getLogger(__name__)

class EPPClient:
    def __init__(self, host, port, username, password, ssl_certfile=None, ssl_keyfile=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.sock = None
        self.greeting = None

    def connect(self):
        """Connects to the EPP server and returns the greeting."""
        plain_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        plain_sock.connect((self.host, self.port))

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        if self.ssl_certfile and self.ssl_keyfile:
            context.load_cert_chain(certfile=self.ssl_certfile, keyfile=self.ssl_keyfile)

        self.sock = context.wrap_socket(plain_sock, server_hostname=self.host)

        self.greeting = self._receive()
        return self.greeting

    def disconnect(self):
        """Disconnects from the EPP server."""
        if self.sock:
            self.sock.close()
            self.sock = None

    def _send(self, xml_data):
        """Sends XML data to the EPP server with proper framing."""
        if not self.sock:
            raise ConnectionError("Not connected to EPP server.")

        log.debug("Sending XML:\n%s", xml_data)
        # EPP framing: 4-byte header with total length
        # The length is the size of the XML payload plus the 4-byte header.
        xml_len = len(xml_data)
        total_len = xml_len + 4

        self.sock.sendall(struct.pack('!I', total_len) + xml_data.encode('utf-8'))

    def _receive(self):
        """Receives data from the EPP server and returns the XML response."""
        if not self.sock:
            raise ConnectionError("Not connected to EPP server.")

        # Read the 4-byte header to get the total length
        header = self.sock.recv(4)
        if not header:
            raise ConnectionError("Connection closed by server.")

        total_len = struct.unpack('!I', header)[0]

        # The actual data length is total_len minus the 4-byte header
        data_len = total_len - 4

        # Read the XML data
        xml_response_bytes = b""
        while len(xml_response_bytes) < data_len:
            chunk = self.sock.recv(data_len - len(xml_response_bytes))
            if not chunk:
                raise ConnectionError("Connection closed by server during read.")
            xml_response_bytes += chunk

        xml_response = xml_response_bytes.decode('utf-8')
        log.debug("Received XML:\n%s", xml_response)

        # Parse and check for errors
        root = ET.fromstring(xml_response)
        result = root.find("{urn:ietf:params:xml:ns:epp-1.0}response/{urn:ietf:params:xml:ns:epp-1.0}result")
        if result is not None:
            code = int(result.get("code"))
            if code >= 2000:
                msg = result.find("{urn:ietf:params:xml:ns:epp-1.0}msg").text
                raise EPPError(msg, code, xml_response)

        return xml_response

    def login(self):
        """Logs in to the EPP server."""
        login_xml = build_login_xml(self.username, self.password)
        self._send(login_xml)
        response = self._receive()
        return response

    def logout(self):
        """Logs out from the EPP server."""
        logout_xml = build_logout_xml()
        self._send(logout_xml)
        response = self._receive()
        self.disconnect()
        return response

    def send_command(self, command_xml):
        """Sends a generic EPP command and returns the response."""
        self._send(command_xml)
        return self._receive()

    def poll(self, op="req", cltrid=""):
        """Sends a poll command."""
        poll_element = ET.Element("poll", op=op)
        poll_xml = build_epp_command("poll", poll_element, cltrid)
        return self.send_command(poll_xml)

    def ack(self, msg_id, cltrid=""):
        """Sends an ack command."""
        ack_element = ET.Element("ack", msgID=msg_id)
        ack_xml = build_epp_command("poll", ack_element, cltrid)
        return self.send_command(ack_xml)
