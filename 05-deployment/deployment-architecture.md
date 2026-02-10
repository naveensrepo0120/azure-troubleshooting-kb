# Deployment Architecture

## Overview
This document describes how the Azure Troubleshooting Knowledge Base is deployed across Azure environments, subscriptions, and resource groups.

The goal is to provide clear separation between environments while keeping operational complexity low.

## Environments

### Development
Purpose:
- Active development and experimentation
- Frequent changes

Characteristics:
- Lower cost configuration
- No production data
- Relaxed availability requirements

### Production
Purpose:
- Stable environment for engineers to use
- High confidence and reliability

Characteristics:
- Controlled changes
- Production data only
- Monitoring and auditing enabled

## Subscription Strategy
- A single Azure subscription can host both environments initially
- Environments are logically separated using resource groups
- Subscription separation can be introduced later if required

## Resource Group Design

### Development Resource Group
Example:
- Name: rg-aztkb-dev
- Contains:
  - Web App (Frontend)
  - API App (Backend)
  - Cosmos DB
  - Azure Cognitive Search
  - Application Insights

### Production Resource Group
Example:
- Name: rg-aztkb-prod
- Contains:
  - Web App (Frontend)
  - API App (Backend)
  - Cosmos DB
  - Azure Cognitive Search
  - Application Insights

## Naming Conventions
- All resource names follow a consistent prefix
- Environment name is included in all resource identifiers
- Names are descriptive and avoid abbreviations where possible

## Networking Considerations
- Services use Azure-managed networking by default
- No inbound access to backend services except through defined endpoints
- Secure communication is enforced using HTTPS

## Deployment Boundaries
- Each environment is deployed independently
- No shared state between development and production
- Infrastructure changes are applied using Infrastructure as Code

