# Python EPP Client

A client for the Extensible Provisioning Protocol (EPP), used for communication with domain name registries.

## Features

- TCP/TLS connection management
- EPP command framing
- Modular command structure
- DNSSEC extension support
- Poll message handling
- Configuration via YAML file

## Installation

```bash
pip install pyyaml
```

## Configuration

Copy the `config.yaml.example` to `config.yaml` and edit it to match your environment.

```yaml
epp:
  host: "ote.verisign-grs.com"
  port: 700
  username: "your_username"
  password: "your_password"
  ssl_certfile: "/path/to/your/cert.pem"
  ssl_keyfile: "/path/to/your/key.pem"
logging:
  level: "INFO"
```

## Usage

Run the `main.py` script to see an example of how to use the client.

```bash
python main.py
```

## Extending the Client

To add new commands, create a new function in the appropriate module in the `epp_client/commands` directory. For example, to add a `delete` command for domains, you would add a `delete_domain` function to `epp_client/commands/domain.py`.

## XML Examples

### Domain Check Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <check>
      <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>example.com</domain:name>
      </domain:check>
    </check>
    <clTRID>client-check-01</clTRID>
  </command>
</epp>
```

### Domain Check Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:cd>
          <domain:name avail="1">example.com</domain:name>
        </domain:cd>
      </domain:chkData>
    </resData>
    <trID>
      <clTRID>client-check-01</clTRID>
      <svTRID>server-trid-123</svTRID>
    </trID>
  </response>
</epp>
```
