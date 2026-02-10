# Backend API Contract

## Overview
This document defines the backend API exposed by the Azure Troubleshooting Knowledge Base.
The API acts as the single access point for all data and operations.

All requests require authentication and are subject to authorization checks.

---

## Authentication
- All API requests require a valid access token
- Unauthorized requests return HTTP 401
- Forbidden actions return HTTP 403

---

## API Endpoints

### Create Troubleshooting Entry
**Endpoint**
POST /api/troubleshooting

**Description**
Create a new troubleshooting entry.

**Request Body**
- title (string)
- issueDescription (string)
- stepsTaken (array of strings)
- resolution (string)
- status (string)
- tags (array of strings)

**Response**
- 201 Created
- Returns the created troubleshooting entry

**Error Cases**
- 400 Bad Request (invalid input)
- 401 Unauthorized
- 403 Forbidden

---

### Update Troubleshooting Entry
**Endpoint**
PUT /api/troubleshooting/{id}

**Description**
Update an existing troubleshooting entry.

**Request Body**
- Same fields as create

**Response**
- 200 OK
- Returns the updated troubleshooting entry

**Error Cases**
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

---

### Get Troubleshooting Entry
**Endpoint**
GET /api/troubleshooting/{id}

**Description**
Retrieve a single troubleshooting entry by ID.

**Response**
- 200 OK
- Returns the troubleshooting entry

**Error Cases**
- 401 Unauthorized
- 404 Not Found

---

### Search Troubleshooting Entries
**Endpoint**
GET /api/troubleshooting/search

**Query Parameters**
- q (string) – search query
- tags (optional) – filter by tags
- status (optional) – filter by status

**Response**
- 200 OK
- Returns a list of matching troubleshooting entries

**Error Cases**
- 401 Unauthorized
- 400 Bad Request

---

## Common Response Characteristics
- All responses are JSON
- Timestamps use ISO 8601 format
- Errors include a message and error code

