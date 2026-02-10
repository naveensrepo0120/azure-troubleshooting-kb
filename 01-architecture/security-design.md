# Security Design

## Security Objectives
The security design aims to:
- Ensure only authorized engineers can access the system
- Restrict who can create or modify troubleshooting entries
- Maintain an audit trail of changes
- Protect troubleshooting data from unauthorized access

## Authentication
Authentication is handled using Microsoft Entra ID.

- All users must authenticate using corporate identities
- No local user accounts are supported
- Authentication tokens are validated by the backend API

## Authorization Model

### Roles

#### Reader
- View and search troubleshooting entries
- Cannot create, edit, or delete entries

#### Contributor
- Create new troubleshooting entries
- Edit entries they have created
- View all entries

#### Administrator
- Edit or delete any troubleshooting entry
- Manage tags and categories
- Access audit and operational data

## Authorization Enforcement
- Authorization is enforced at the backend API layer
- The web UI does not directly enforce permissions
- Role information is derived from authenticated user claims

## Data Protection
- All data access occurs through the backend API
- Direct access to the data store is restricted
- Data is encrypted at rest and in transit using Azure-managed controls

## Auditing and Traceability
- All create, update, and delete actions are logged
- Logs include user identity, timestamp, and action performed
- Audit data is retained according to organizational policies

## Security Boundaries
- The web UI has no direct access to data stores
- Search and data services are accessed only by the backend API
- Identity services are isolated from application logic

## Failure Scenarios
- Authentication failure results in denied access
- Authorization failure returns a forbidden response
- Security-related failures are logged for investigation

