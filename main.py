import yaml
import logging
from epp_client.client import EPPClient
from epp_client.commands.domain import check_domain, info_domain, create_domain
from epp_client.schemas.dnssec import create_dnssec_data

def main():
    """Main function to demonstrate EPP client usage."""
    # Load configuration
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Configure logging
    logging.basicConfig(level=config['logging']['level'])

    # Create EPP client instance
    client = EPPClient(
        host=config['epp']['host'],
        port=config['epp']['port'],
        username=config['epp']['username'],
        password=config['epp']['password'],
        ssl_certfile=config['epp'].get('ssl_certfile'),
        ssl_keyfile=config['epp'].get('ssl_keyfile')
    )

    try:
        # Connect and get greeting
        greeting = client.connect()
        logging.info("Received greeting:\n%s", greeting)

        # Login
        login_response = client.login()
        logging.info("Login response:\n%s", login_response)

        # Check a domain
        domain_to_check = "example.com"
        check_xml = check_domain(domain_to_check, cltrid="client-check-01")
        check_response = client.send_command(check_xml)
        logging.info("Domain check response for %s:\n%s", domain_to_check, check_response)

        # Info a domain
        domain_to_info = "example.com"
        info_xml = info_domain(domain_to_info, cltrid="client-info-01")
        info_response = client.send_command(info_xml)
        logging.info("Domain info response for %s:\n%s", domain_to_info, info_response)

        # Create a domain with DNSSEC
        ds_records = [
            {'keyTag': 12345, 'alg': 8, 'digestType': 2, 'digest': 'e1f6c427339178b0453303c03a6a1bf6d7c4a22b0e633d3b71597a7e8286dc5a'}
        ]
        dnssec_xml = create_dnssec_data(ds_records)
        create_xml = create_domain(
            "example-dnssec.com",
            period=1,
            ns=["ns1.example.com", "ns2.example.com"],
            registrant="CONTACT-123",
            admin="CONTACT-123",
            tech="CONTACT-123",
            auth_info="somepassword",
            dnssec_data=dnssec_xml,
            cltrid="client-create-01"
        )
        # create_response = client.send_command(create_xml)
        # logging.info("Domain create response:\n%s", create_response)

        # Poll for messages
        poll_response = client.poll()
        logging.info("Poll response:\n%s", poll_response)

        # In a real application, you would parse the poll response
        # and if there is a message, you would ack it.
        # msg_id = ... # parse from poll_response
        # if msg_id:
        #     ack_response = client.ack(msg_id)
        #     logging.info("Ack response:\n%s", ack_response)

    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)
    finally:
        # Logout
        if client.sock:
            logout_response = client.logout()
            logging.info("Logout response:\n%s", logout_response)
            logging.info("Disconnected from EPP server.")

if __name__ == "__main__":
    main()
