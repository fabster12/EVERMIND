# Delta Spec: Evidence Retrieval — EverMind

## ADDED

### Requirement: Evidence comes only from the trusted source corpus

The system MUST retrieve supporting passages exclusively from the trusted
source corpus. It MUST NOT consult any other source of information, and it
MUST NOT rely on knowledge not present in a retrieved passage.

Each retrieved passage MUST be identifiable, so that a later claim can be
traced back to it.

#### Scenario: Retrieval returns identified passages

- **Given** a group dispositioned as a genuine gap about duty liability
- **And** a source document covering incoterms and duty responsibility
- **When** evidence is retrieved
- **Then** one or more passages are returned
- **And** each returned passage carries an identifier naming the document it
  came from

#### Scenario: No external source is consulted

- **Given** any group proceeding to evidence retrieval
- **When** evidence is retrieved
- **Then** the only material considered is the trusted source corpus

---

### Requirement: Retrieved evidence is available to later steps

Every passage retrieved for a group MUST be recorded in a way that later
steps can read, so that a drafted answer can be checked against the evidence
that was actually available.

The record MUST be scoped to the run and to the group, so that evidence
retrieved for one group cannot support a claim made about another.

#### Scenario: Evidence retrieved is recoverable after drafting

- **Given** a group for which three passages were retrieved
- **When** the answer has been drafted
- **Then** the identifiers of exactly those three passages can be read back
  for that group

#### Scenario: Evidence does not leak between groups

- **Given** two groups processed in the same run
- **When** evidence is retrieved for both
- **Then** the evidence recorded for each group contains only the passages
  retrieved for that group

---

### Requirement: Absence of evidence is reported, not filled in

When the corpus contains no passage supporting an answer, the system MUST
report that no evidence was found. It MUST NOT return a loosely related
passage in order to produce an answer.

A genuine gap with no supporting evidence MUST still reach the reviewer as a
gap worth knowing about.

#### Scenario: An unsupported gap returns no evidence

- **Given** a group dispositioned as a genuine gap about insurance limits for
  fine art
- **And** no document in the corpus covering fine-art insurance
- **When** evidence is retrieved
- **Then** no passages are returned
- **And** the group is recorded as a gap with no supporting evidence

#### Scenario: A loosely related passage is not substituted

- **Given** the same group
- **And** a document covering general liability limits but not fine art
- **When** evidence is retrieved
- **Then** the general liability passage is not returned as support for a
  fine-art answer
