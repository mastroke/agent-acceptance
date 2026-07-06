# Seattle Fire Department — buyer/deployer (5(d))

**To:** (city procurement / fire chief public affairs — find via seattle.gov/fire)
**Subject:** Layer attribution for Corti 911 triage — reproducible probe-set pilot

Hi [NAME],

I'm reaching out because of the public reporting on SFD's use of Corti for 911
medical-call triage since Dec 2023 — specifically the gap between what the
system decides and what can be independently verified when the vendor stack
updates.

Your audit trail can show *what* was routed and *which model version was
declared*. It cannot show *which layer moved* when behavior shifts — vendor
weights, vendor harness, or SFD's own integration — without a controlled
experiment on a frozen probe set.

I build open-source acceptance tooling (`agent-acceptance`) that runs exactly
that experiment and emits a signed cross-layer verdict report. The output is
the kind of evidence pack regulators and councils ask for when outcomes are
disputed but metrics aren't public.

Would you take a 30-minute design-partner call? I'd like to run a no-charge
90-day pilot on a small frozen probe set (your diverted-call scenarios or a
public EMS benchmark stratum) and hand you a reproducible acceptance report
you can use internally or in public review.

No sales pitch — I'm validating whether this tooling closes a real gap for
high-risk deployers, not vendors.

Best,
Masoob Alam
github.com/mastroke/agent-acceptance
