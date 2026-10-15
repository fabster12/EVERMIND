# Delta Spec: Candidate Drafting — EverMind

## ADDED

### Requirement: A drafted answer cites the evidence it rests on

Every drafted answer MUST carry at least one citation, and every citation
MUST name a passage that was retrieved for that group during that run.

A draft that cites nothing, or that cites a passage not retrieved for that
group, MUST be rejected before it reaches the reviewer. Such a draft is not
a weak answer; it is an invalid one.

#### Scenario: A grounded answer is accepted

- **Given** a group with two retrieved passages about duty liability
- **When** an answer is drafted
- **Then** the answer carries at least one citation
- **And** every citation names one of those two passages
- **And** the candidate reaches the review queue

#### Scenario: An uncited answer is rejected

- **Given** a drafted answer carrying no citation
- **When** the candidate is checked
- **Then** it is rejected and does not reach the review queue

#### Scenario: A citation to unretrieved evidence is rejected

- **Given** a group for which passages A and B were retrieved
- **And** a drafted answer citing passage C
- **When** the candidate is checked
- **Then** it is rejected and does not reach the review queue

---

### Requirement: No answer is drafted without supporting evidence

When no evidence was retrieved for a group, the system MUST NOT produce an
answer. It MUST record that the gap is real and that the corpus does not
currently support answering it.

Declining to answer is a correct outcome. Producing a plausible answer from
no evidence is the most damaging failure available to this system, because a
wrong entry that reads well will be approved and then served to everyone.

#### Scenario: An unsupported gap produces no answer

- **Given** a group dispositioned as a genuine gap with no retrieved evidence
- **When** drafting runs
- **Then** no answer text is produced
- **And** the candidate records low confidence
- **And** the candidate records that no supporting evidence exists

#### Scenario: Partial evidence does not license a complete answer

- **Given** a group asking about both duty liability and refund timelines
- **And** retrieved evidence covering duty liability only
- **When** the answer is drafted
- **Then** the answer addresses only the part the evidence supports
- **And** the unsupported part is not answered

---

### Requirement: A candidate is reviewable without further work

Each candidate MUST carry enough for a reviewer to accept or reject it
without opening another system: the question it answers, how many logged
questions it covers, the proposed answer where one exists, its citations,
its disposition, a confidence level, and a reason where it was refused or
marked duplicate.

A proposed answer MUST be short enough to review at a glance. Answers MUST
NOT exceed 150 words.

#### Scenario: A reviewer can judge a candidate from the queue alone

- **Given** a candidate in the review queue
- **When** a reviewer reads it
- **Then** they can see the question, the proposed answer, its citations and
  its confidence
- **And** they do not need to consult the query log or the source corpus to
  make a decision

#### Scenario: An overlong answer is rejected

- **Given** a drafted answer of 300 words
- **When** the candidate is checked
- **Then** it is rejected and does not reach the review queue
