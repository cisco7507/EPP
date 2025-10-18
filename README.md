# EPP GUI

A web-based graphical user interface for the Extensible Provisioning Protocol (EPP), built on top of a Python EPP client.

## Architecture

- **Frontend:** Next.js, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python
- **Worker:** Celery, Redis
- **Database:** Postgres (for audit logs, etc.)

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd epp-gui
   ```

2. **Build and run the containers:**

   ```bash
   docker-compose up --build
   ```

3. **Access the application:**

   - **Frontend:** http://localhost:3000
   - **Backend API:** http://localhost:8000/docs

## Security

- **Authentication:** JWTs are used for authentication.
- **EPP Credentials:** EPP credentials should be stored in a secure manner, such as a KMS or Secrets Manager, and not in the source code.

## Extending the Client

The EPP client can be extended by adding new commands to the `backend/epp_client/commands` directory.
