# Delta Spec: Review Queue — EverMind

## ADDED

### Requirement: The knowledge base is never modified by the system

The system MUST NOT create, modify, append to or delete any entry in the
knowledge base. Publishing an approved candidate is a separate action taken
by a person.

This MUST hold structurally rather than by policy: no part of the system has
the ability to write to the knowledge base, so no decision it makes can
result in a published entry.

#### Scenario: A full run leaves the knowledge base untouched

- **Given** a knowledge base in a known state
- **When** a full batch of logged questions is processed
- **Then** the knowledge base is byte-for-byte identical to its prior state

#### Scenario: A high-confidence candidate is still not published

- **Given** a candidate with a well-cited answer and the highest confidence
  the system can assign
- **When** the run completes
- **Then** the candidate is in the review queue
- **And** the knowledge base contains no new entry

---

### Requirement: Every group in a batch appears in the queue

The review queue MUST contain exactly one candidate per group processed, in
every disposition including refusals. A refused question is information the
content owner needs, not noise to be filtered out before they see it.

#### Scenario: Refused and duplicate groups still appear

- **Given** a batch producing twelve groups: seven genuine gaps, three
  duplicates and two refusals
- **When** the run completes
- **Then** the review queue contains twelve candidates
- **And** each refusal carries its reason
- **And** each duplicate names the published entry it matches

---

### Requirement: Every decision can be traced to what produced it

For each candidate, it MUST be possible to establish which passages were
retrieved and which were cited, so that a reviewer can verify a claim rather
than trust it.

Without this the approval step is ceremonial: a reviewer who cannot check a
citation is only agreeing that the answer reads well.

#### Scenario: A reviewer can verify a citation

- **Given** a candidate citing a passage
- **When** the reviewer follows that citation
- **Then** they reach the exact passage text the answer was drawn from

#### Scenario: Activity for a run is recoverable

- **Given** a completed run
- **When** the recorded activity is read
- **Then** it shows, for each group, which steps ran and what evidence was
  retrieved

---

### Requirement: Re-running a batch does not duplicate candidates

Running the same batch twice MUST produce the same set of candidates with
the same identifiers, so that a re-run after a failure is safe and does not
confront the reviewer with a second copy of work already queued.

#### Scenario: A repeated run is idempotent

- **Given** a batch that has been processed once
- **When** the same batch is processed again
- **Then** the candidates carry the same identifiers as the first run
- **And** the reviewer sees no duplicated entries
