# NIC.IM EPP OT&E Test Client

This Python project provides a complete, automated EPP (Extensible Provisioning Protocol) test client that performs the official OT&E (Operational Test & Evaluation) test sequence required by the NIC.IM registry to gain access to their production EPP interface.

## Features

- Fully automated execution of all steps outlined in the NIC.IM EPP OT&E Procedures (v1.11)
- TLS-secured connection to the NIC.IM EPP test server
- Sends and validates standard EPP commands for domains and contacts
- Logs each request and response
- Stops execution on first failure (`fail-fast`)
- Generates correct test results for both successful and error-based flows

## Requirements

- Python 3.7+
- Internet access to NIC.IM OT&E systems

## Installation

```bash
git clone https://github.com/philadcock/im_registry_epp.git
cd im_registry_epp
pip install -r requirements.txt
```

There are no external libraries required beyond the Python standard library.

## Usage

Edit `epp_ote_runner.py` and configure the following variables at the top:

```python
CLIENT_ID = "your-client-id"
PASSWORD = "initial-password"
NEW_PASSWORD = "new-password"
```

Run the script:

```bash
python3 epp_ote_runner.py
```

The script will connect to the OT&E server, perform all test steps in sequence, and stop immediately if any command fails. All traffic is logged to the console.

## OT&E Test Coverage

This project implements all the required tests as per the NIC.IM OT&E Procedures v1.11:

- ✅ Connection and session management (hello, login, logout, password change)
- ✅ Domain operations (create, update, check, info, renew, transfer, delete)
- ✅ Contact operations (create, with and without optional fields)
- ✅ Hostname/nameserver updates
- ✅ Error handling tests (e.g., missing auth-info, invalid domain length, missing country code)

The test flow matches the structure and numbering of the NIC.IM test plan to allow easy verification and submission.

## File Overview

- `epp_ote_runner.py` – Main script that executes the test plan
- `epp_commands.py` – XML command builders for various EPP operations
- `README.md` – This documentation

## License

MIT License

## Notes

This client is intended for use in the NIC.IM OT&E environment. It can be adapted for other EPP registries with minimal changes.
