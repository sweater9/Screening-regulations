# Global Sanctions & High-Risk Jurisdiction Screening Regulations

Structured reference dataset of global economic sanctions regimes, issuing authorities, governing statutes, and screening lists, for use in AML/CFT and sanctions-screening compliance programs.

## Contents

- [`sanctions_regimes.json`](./sanctions_regimes.json) — Structured records covering:
  - **USA**: OFAC (SDN List, Non-SDN lists incl. SSI/CAPTA/NS-CMIC/NS-MBS, 50% Rule), BIS (Entity List, Unverified List, MEU List), State Dept./DDTC (ITAR Debarred List)
  - **UK**: HMT/OFSI Consolidated List under SAMLA 2018; FCDO sanctions regime guidance
  - **UNSC**: Consolidated Sanctions List (1267/1989/2253 ISIL-Al-Qaida, 1988 Taliban, 1718 DPRK, and related committees)
  - **FATF**: Black List (Call for Action) and Grey List (Increased Monitoring), Recommendations 6 & 7
  - **UAE**: Cabinet Decision No. (74) of 2020, EOCN Local Terrorist List, CBUAE/DFSA/FSRA implementing directives, 24-hour freeze timeline
  - **EU**: Council/EEAS Consolidated List under TFEU Art. 215, EU 50% aggregated ownership rule
  - **Other regimes**: Switzerland (SECO), Canada (SEMA/OSFI), Australia (DFAT)

## Schema

Each record follows:

```json
{
  "jurisdiction_or_body": "",
  "issuing_authority": "",
  "governing_law_or_statute": "",
  "list_name": "",
  "sanction_types": [],
  "target_categories": [],
  "ownership_control_rules": "",
  "update_frequency": "",
  "official_endpoint_or_source": ""
}
```

## Notes on methodology

- **FATF vs. statutory sanctions bodies**: FATF (see the FATF record) is a standard-setting body — it issues the Black/Grey Lists identifying jurisdictional AML/CFT deficiencies and sets global expectations (Recommendations 6 & 7) for targeted financial sanctions, but it does **not** itself impose asset freezes. OFAC, OFSI, the UNSC, and UAE authorities are statutory/enforcement bodies that legally compel asset freezes and other restrictions.
- **Ownership/control rules** are captured explicitly where a jurisdiction publishes a defined threshold (e.g., OFAC's 50% Rule, the EU's 50% aggregated rule, UK's "ownership or control" test). Where no single fixed numeric threshold is publicly codified, the record is labeled accordingly rather than inferring one.
- **Zero hallucination policy**: no legal citation, list name, or machine-readable endpoint was invented. Where an official structured feed (API/XML/CSV) is not publicly documented, the record states "Direct Government Directive" or "Not Publicly Specified."
- **UAE compliance timelines**: the UAE's Cabinet Decision No. (74) of 2020 mandates freezing of funds "without delay"; CBUAE guidance to Licensed Financial Institutions operationalizes this as a 24-hour screening/freeze window following a new designation.

## Disclaimer

This dataset is a compiled reference for screening-program design and is **not legal advice**. Always verify against the live official source listed in `official_endpoint_or_source` before relying on it for compliance decisions, as sanctions lists change frequently (often daily or ad-hoc).
