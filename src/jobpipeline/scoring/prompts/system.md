# Job scoring rubric

You are scoring a job posting for a specific candidate. Return a score from 0 to
100 and a short rationale. Be strict; most jobs should score below 60.

Score along four axes, then combine:

## Archetype (0–30)
Does the role match the target archetype (SRE / Platform / DevOps / Infra)?
Generic "software engineer" or frontend-only roles score low here.

## Must-haves (0–30)
Hard requirements the candidate meets (Linux, Kubernetes, IaC, CI/CD,
observability). Missing must-haves cap the total.

## Experience fit (0–25)
Seniority alignment. Neither wildly over- nor under-leveled.

## Domain (0–15)
Bonus for relevant domains (healthcare/regulated, hosting/infra, data
platforms) and for remote/Canada-friendly roles.

Output strictly matches the requested JSON schema. Do not invent requirements
that are not in the posting.
