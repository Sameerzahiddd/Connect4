The Problem
When Laurel ships a release, the communication process is entirely manual. A PM writes release
notes. Then a separate internal Slack announcement. Then Sales needs a different version
emphasizing customer-facing impact. Then CS needs to know which customers are affected and
what to tell them. Then Support needs FAQs for the inevitable inbound questions. The same
information gets rewritten 4-5 times, inconsistently, and usually late. Sales sometimes learns about
new features from customers instead of from Product.
What We Want to See
Design and build a system that automates the release communication lifecycle. The system ingests
completed Linear tickets and generates tailored outputs for every audience that needs to know about
a release.
The system should ingest completed Linear tickets from a release cycle (titles, descriptions, labels, linked PRs, and any attached specs), classify changes by type and customer impact, automatically group related tickets into coherent release themes, and generate 5 output formats from a single
release: customer-facing release notes, internal changelog, sales enablement brief, CS/Support
FAQ, and a Slack announcement for #product-updates.
The system should also handle edge cases like partially shipped features, features behind feature
flags, and breaking changes that require customer communication.
Deliverables
● Working prototype: Build a system using a platform of choice that takes sample Linear
ticket data as input and generates all 5 output formats.
○ For the purpose of this activity, ask AI to create a realistic mock dataset of 5-10
tickets. Show how the system would work end to end. Include the actual prompts
driving the classification and generation, and explain why you structured them that
way.
● System architecture covering data flow from Linear through classification and grouping to
multi-format output generation, classification logic, consistency across outputs, and prompt
engineering strategy.
● Implementation plan covering MVP scope, quality validation app
