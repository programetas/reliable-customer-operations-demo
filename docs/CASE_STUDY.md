# Case study: reliable automation with human control

## Problem

Operational teams handle many requests that look similar but carry different levels of risk. A workflow that retrieves an existing invoice is materially different from one that changes a payment method or deletes an account.

## Design

The demo separates interpretation from authority. An LLM may extract fields or suggest a category, but a deterministic policy decides whether the system can act. Sensitive categories enter an approval queue. Unsupported requests stay manual.

Every decision produces an evidence event containing the request identifier, the policy result, a redacted summary, a UTC timestamp, and a hash. Repeating the same request identifier returns a duplicate decision instead of executing the action again.

## Reliability lessons

The hard part of automation is rarely the successful path. Production systems need explicit states for missing credentials, MFA, captchas, ambiguous data, unavailable portals, partial failures, and human decisions. The action layer should stop cleanly, preserve context, and support a controlled retry.

## Production extension

A production version would use a durable queue and database, authenticated connectors, structured telemetry, retries with backoff, dead-letter handling, role-based approval, and a managed secret store. It would also define data retention and incident procedures before connecting a real customer system.

