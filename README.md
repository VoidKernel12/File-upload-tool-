# HeartKiller Cloud Vault

A Termux-based Python Flask cloud vault for secure, room-based file sharing and storage. **HeartKiller Cloud Vault** provides a lightweight web dashboard that can run directly on Android through Termux, with persistent room metadata and optional public access through Cloudflare Tunnel.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Starting the Server](#starting-the-server)
- [Authentication and Rooms](#authentication-and-rooms)
- [Cloud Storage Workflow](#cloud-storage-workflow)
- [Auto-Recovery and Persistence](#auto-recovery-and-persistence)
- [Cloudflare Tunnel](#cloudflare-tunnel)
- [Multi-Device Sharing](#multi-device-sharing)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Data and Storage](#data-and-storage)
- [Updating the Project](#updating-the-project)
- [License](#license)

## Overview

**HeartKiller Cloud Vault** is designed for users who want a simple private cloud-style file vault that can be hosted from an Android device running Termux.

The application uses a Python Flask server and provides a browser-accessible dashboard for room-based file storage. A room can be created or joined using either a user-defined custom number or an automatically generated access token.

The project is suitable for:

- Personal file sharing between devices
- Temporary private cloud storage
- Local-network file management
- Termux-hosted file vaults
- Multi-device transfers
- Development and testing of Flask-based storage applications

> **Important:** Exposing a local server to the public internet changes its security profile. Review the security guidance in this README before using Cloudflare Tunnel for sensitive files.


```bash
git clone https://github.com/VoidKernel12/File-upload-tool-.git
```
```bash
cd File-upload-tool-
```
```bash
chmod +x install.sh
./install.sh
```
```bash
python tool.py
```
## Features

### 1. Dual Authentication

HeartKiller Cloud Vault supports two room-access methods.

#### Custom Number

Users can create or join a room with a custom number, for example:

```text
1234
```

This method is convenient when a short room identifier is preferred.

#### Auto-Generated Access Token

The application can also use a generated access token such as:

```text
HK-ACC-XXXXXXXX
```

The generated token is intended to provide a less predictable room-access identifier than a simple custom number.

Keep access credentials private. Anyone who obtains valid room-access information may be able to access the corresponding room depending on the application's configured authorization behavior.

---

### 2. Auto-Recovery and Persistence

Room metadata is stored in:

```text
vault_metadata.json
```

This allows the application to restore important room information after a server restart.

The persistence layer is intended to prevent room configuration and metadata from being lost simply because the Flask process was stopped or Termux was restarted.

Typical persistent information may include room-related metadata and storage references used by the application.

> The exact information persisted is determined by the implementation in `tool.py`.

---

### 3. Real-Time Cloud Storage Dashboard

The Flask web dashboard provides a browser-based interface for managing files.

Depending on the implementation, users can perform operations such as:

- Upload files
- View stored files
- Manage vault contents
- Download files
- Work with room-specific storage
- Access the vault from another device

The vault is hosted locally by default and listens on:

```text
http://127.0.0.1:5000
```

---

### 4. Cloudflare Tunnel Integration

Cloudflare Tunnel can be used to expose the local Flask server through a public Cloudflare URL.

This is useful when devices are not connected to the same local network.

The local Flask server remains bound to:

```text
127.0.0.1:5000
```

Cloudflare Tunnel forwards requests to that local service.

Example:

```bash
cloudflared tunnel --url http://127.0.0.1:5000
```

The command normally displays a public tunnel URL in the terminal.

---

## Project Structure

A basic project layout is:

```text
HeartKiller-Cloud-Vault/
├── tool.py
├── install.sh
├── vault_metadata.json
└── README.md
```

### `tool.py`

The main Python application.

It contains the Flask server and the application's core cloud-vault functionality, including the web interface, room handling, file operations, and persistence logic.

### `install.sh`

The installation helper script.

It is intended to automate the setup process required to run the project in Termux.

### `vault_metadata.json`

Persistent metadata used by the vault for recovery across server restarts.

If this file is generated automatically, do not manually modify it unless you understand the application's expected JSON structure.

### `README.md`

Project documentation and setup instructions.

---

## Requirements

The project is designed for an Android device with Termux.

Recommended requirements include:

- Android device
- Termux
- Python 3
- Flask
- Bash
- Internet connection when using Cloudflare Tunnel
- `cloudflared` when public tunneling is required

The installer script is intended to simplify dependency installation.

---

##

The actual generated token should be treated as a secret.

### Credential Handling

Do not publish room credentials in:

- Public GitHub repositories
- Screenshots
- Public chat messages
- Social-media posts
- Public issue trackers
- Untrusted websites

For sensitive files, prefer a strong, unpredictable access mechanism and additional application-level authentication where available.

---

## Cloud Storage Workflow

A typical workflow is:

1. Start Termux.
2. Navigate to the HeartKiller Cloud Vault project.
3. Start the Flask server.
4. Open the vault dashboard.
5. Create or join a room.
6. Authenticate using the configured room-access method.
7. Upload files through the dashboard.
8. Manage files from the vault interface.
9. Download files from another authorized device when required.
10. Stop the server when the vault is no longer needed.

For local-only usage, no public tunnel is required.

---

## Auto-Recovery and Persistence

HeartKiller Cloud Vault uses:

```text
vault_metadata.json
```

as its persistent metadata file.

The purpose of this file is to preserve room-related information so that the application can recover its state after a restart.

### Server Restart

If the Flask server is stopped and later started again:

```bash
python tool.py
```

the application can load the available metadata from:

```text
vault_metadata.json
```

This reduces the need to recreate room information after every restart.

### Protecting the Metadata File

Treat `vault_metadata.json` as application data.

Do not:

- Publish it to a public repository if it contains secrets
- Modify its structure without understanding the code
- Delete it while the application depends on its stored state
- Share it with untrusted users

For Git repositories, consider adding sensitive runtime data to `.gitignore` when appropriate.

Example:

```gitignore
vault_metadata.json
```

Whether this should be ignored depends on the project's intended backup and deployment model.

---

## Cloudflare Tunnel

Cloudflare Tunnel provides an optional way to make the locally running Flask application reachable through the internet.

### Start the Local Server First

In the first Termux session:

```bash
python tool.py
```

Leave this process running.

### Open a New Termux Session

In a separate Termux session, run:

```bash
cloudflared tunnel --url http://127.0.0.1:5000
```

Cloudflared will attempt to establish a tunnel to the local Flask server.

A public URL may be displayed by `cloudflared`. Use that URL to access the vault from an authorized remote device.

### Important

The public tunnel and the Flask application are separate processes:

```text
Remote Device
     │
     ▼
Cloudflare Tunnel
     │
     ▼
127.0.0.1:5000
     │
     ▼
HeartKiller Cloud Vault
     │
     ▼
Vault Storage
```

The Flask server must remain running for the tunnel to have a working local destination.

---

## Multi-Device Sharing

For devices connected to the same local network, local access may be sufficient depending on how the Flask server is configured.

For remote devices, Cloudflare Tunnel can provide an internet-accessible endpoint.

A typical remote-sharing workflow is:

```text
Android / Termux
      │
      ├── tool.py
      │
      └── Flask :5000
              │
              ▼
       Cloudflare Tunnel
              │
              ▼
       Public Tunnel URL
              │
       ┌──────┴──────┐
       ▼             ▼
   Phone/Tablet    Computer
```

Only share the public URL and room credentials with people who are authorized to access the vault.

---

## Security Notes

### Keep Access Credentials Private

Room numbers and access tokens should be considered sensitive access information.

Avoid sharing them publicly.

### Public Exposure

A server exposed through Cloudflare Tunnel is no longer limited to the local Android device.

Before exposing the service publicly:

- Use strong access credentials.
- Avoid storing highly sensitive information unless the application provides adequate protection.
- Keep Termux and project dependencies updated.
- Monitor who receives the tunnel URL.
- Stop the tunnel when remote access is no longer required.
- Do not assume that a tunnel URL itself provides application authentication.

### File Upload Security

File-upload applications should validate uploaded files and handle filenames safely.

If this project is modified, additional protections should be considered, including:

- Filename sanitization
- File-type validation
- Upload-size limits
- Authentication and authorization checks
- Protection against path traversal
- Safe storage paths
- Rate limiting
- Session security
- Logging and monitoring

### Do Not Commit Secrets

Never commit private access tokens, passwords, private metadata, or sensitive uploaded files to a public GitHub repository.

A `.gitignore` file can be used to exclude runtime data.

Example:

```gitignore
__pycache__/
*.pyc
vault_metadata.json
.env
```

Adjust this list according to the actual project behavior.

---

## Troubleshooting

### `python: command not found`

Verify that Python is installed:

```bash
python --version
```

If Python is missing, install it through Termux's package manager:

```bash
pkg update
pkg install python
```

Then run the installer again:

```bash
chmod +x install.sh
./install.sh
```

### Flask Module Error

If Python reports that Flask is missing, install it with:

```bash
pip install flask
```

Then retry:

```bash
python tool.py
```

If `install.sh` already installs Flask, prefer rerunning the installer instead of manually changing dependencies.

### Port 5000 Is Already in Use

If the application reports that port `5000` is already occupied, check whether another Flask or Python process is running.

Stop the previous server process and start the application again.

You can inspect running processes with:

```bash
ps
```

### Cloudflare Tunnel Cannot Connect

Make sure the Flask server is running first:

```bash
python tool.py
```

Then, from another Termux session:

```bash
cloudflared tunnel --url http://127.0.0.1:5000
```

Also verify that `cloudflared` is installed and available:

```bash
cloudflared --version
```

### Room Data Is Missing After Restart

Check whether:

```text
vault_metadata.json
```

exists in the expected project/runtime location.

Do not recreate or overwrite the file blindly, because doing so may remove previously stored metadata.

---

## Data and Storage

The project separates the concepts of:

- Flask application logic
- Room metadata
- Stored files
- Browser-based management
- Optional public tunneling

The exact physical location of uploaded files depends on the implementation in `tool.py`.

Before moving or deleting project directories, identify where the application stores uploaded files and metadata.

For backups, preserve both:

```text
vault_metadata.json
```

and the application's file-storage directory.

Backing up only the metadata may not preserve the actual uploaded files.

---

## Updating the Project

Before updating the application, create a backup of important runtime data.

Recommended backup targets include:

```text
vault_metadata.json
```

and the directory containing uploaded files.

After updating the source code, reinstall dependencies if necessary:

```bash
chmod +x install.sh
./install.sh
```

Then start the application:

```bash
python tool.py
```

Test local access before starting a public Cloudflare Tunnel.

---

## Recommended Operating Procedure

For local use:

```bash
chmod +x install.sh
./install.sh
python tool.py
```

For public/remote access:

**Termux Session 1**

```bash
python tool.py
```

**Termux Session 2**

```bash
cloudflared tunnel --url http://127.0.0.1:5000
```

When finished:

1. Stop the Cloudflare Tunnel.
2. Stop the Flask server.
3. Keep the metadata and uploaded files backed up if they are important.

---

## Development Notes

The project is intentionally centered around a lightweight Flask architecture so it can run directly in a Termux environment without requiring a dedicated server or desktop computer.

The main application entry point is:

```text
tool.py
```

The setup process is handled by:

```text
install.sh
```

Persistent vault metadata is stored through:

```text
vault_metadata.json
```

This structure keeps the project easy to deploy, inspect, back up, and operate from an Android terminal.

---

## Disclaimer

HeartKiller Cloud Vault is intended for legitimate personal, development, testing, and authorized file-sharing use.

You are responsible for the files you store, the credentials you distribute, the devices you connect, and the way you expose the service to the internet.

Do not use the application to access, store, distribute, or transfer data without appropriate authorization.

---

## License

No specific open-source license is defined by this README.

If this project is published on GitHub, add an appropriate license file such as `LICENSE` and update this section to match the chosen license.

---

## Quick Start

### Local Vault

```bash
chmod +x install.sh
./install.sh
python tool.py
```

Open:

```text
http://127.0.0.1:5000
```

### Public Tunnel

Start the application:

```bash
python tool.py
```

Then, in a new Termux session:

```bash
cloudflared tunnel --url http://127.0.0.1:5000
```

Use the generated Cloudflare Tunnel address to connect from an authorized remote device.

---

**HeartKiller Cloud Vault — Termux-powered room-based cloud storage.**
