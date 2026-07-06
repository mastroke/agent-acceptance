# Logikality — vendor (5(b) mortgage underwriting QC)

**To:** product / compliance contact (logikality.ai)
**Subject:** Layer verdict on top of your audit trail — EU AI Act design-partner pilot

Hi [NAME],

Logikality's underwriting-QC agents already emit decision-ready packets with
what/why/evidence/who/when. That audit trail answers *what was decided*. It
doesn't run the cross-provider-layer experiment that shows *which layer moved*
when behavior drifts — vendor API vs your agent harness vs prompt/tool changes.

I'm building `agent-acceptance`, an OSS CLI that runs that controlled A/B on a
frozen probe set and outputs a signed acceptance report. For Annex III 5(b)
credit systems, the output maps to Art. 25 substantial-modification and Art. 26
deployer/provider boundary questions — especially as PLD transposition lands
9 Dec 2026.

Your audit trail and our layer verdict are complementary, not competing.

Open to a 30-minute design-partner call? I'd like a 90-day no-charge pilot on
a small frozen mortgage-QC scenario set and your feedback on whether the report
is something your buyers would accept at handoff.

Best,
Masoob Alam
github.com/mastroke/agent-acceptance
