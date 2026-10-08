# Security

This repository is a synthetic demonstration. Do not add production credentials, access tokens, customer data, exported tickets, invoices, or portal captures.

For a real deployment:

- store secrets in a managed secret store;
- scope connector permissions to the minimum required;
- encrypt durable queues and evidence at rest;
- require approval before financial, identity, deletion, or access-control actions;
- redact personal data before sending context to an LLM;
- retain an immutable audit record for decisions and approvals;
- define incident, rollback, and credential-rotation procedures.

Report security concerns privately to `marc@funhelps.com`.

