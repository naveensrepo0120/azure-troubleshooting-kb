# Data Model Design

## Overview
Each troubleshooting record is stored as a single document representing a resolved or investigated issue.
The data model is designed to support full-text search, filtering, and future enhancements.

## Troubleshooting Entry Schema

### Core Fields

| Field Name        | Type      | Description |
|------------------|-----------|-------------|
| id               | string    | Unique identifier for the troubleshooting entry |
| title            | string    | Short, descriptive title of the issue |
| issueDescription | string    | Description of the problem and symptoms |
| stepsTaken       | array     | Ordered list of troubleshooting steps |
| resolution       | string    | Final resolution or outcome |
| status           | string    | Open, Resolved, or Inconclusive |
| tags             | array     | Keywords such as service names or issue categories |

### Metadata Fields

| Field Name   | Type   | Description |
|-------------|--------|-------------|
| createdBy   | string | Engineer who created the entry |
| createdDate | string | Creation timestamp |
| updatedBy   | string | Last engineer to update the entry |
| updatedDate | string | Last update timestamp |

## Example Troubleshooting Document

```json
{
  "id": "uuid",
  "title": "AVD login stuck at black screen",
  "issueDescription": "Users experienced a black screen during login to Azure Virtual Desktop sessions.",
  "stepsTaken": [
    "Verified FSLogix profile container availability",
    "Checked storage account connectivity",
    "Reviewed AVD agent logs"
  ],
  "resolution": "FSLogix profile container was locked due to stale session",
  "status": "Resolved",
  "tags": ["AVD", "FSLogix", "Login"],
  "createdBy": "engineer1",
  "createdDate": "2026-02-10",
  "updatedBy": "engineer1",
  "updatedDate": "2026-02-10"
}

