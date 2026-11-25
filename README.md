# Java Crypto Roadmap

Maintain an Excel history of Oracle Java cryptographic changes, with a separate list of future roadmap plans and matching JSON data for a browser application.

The initial baseline was reviewed on **November 25, 2026**, using Oracle's roadmap updated **November 5, 2026**. It contains **70 released changes** from January 2016 through October 2026 and **9 planned changes**. Of the released rows, 53 explicitly list at least one of JDK 8, 11, 17, 21, or 25; historical rows for other releases are also retained.

Open the workbook listed under [Current baseline](Java-Crypto-Roadmap-Update-Workflow.md#current-baseline). Its **Released** and **Planned** tabs include delivery versions, target windows, effective conditions, and links to Oracle's technical guidance. Delivery-version links open release notes when Oracle provides them.

## Update the data

Open this repository in your coding assistant and use this request:

> Run `Java-Crypto-Roadmap-Update-Workflow.md` through the current date, including validation and advancing the baseline after a successful update. Do not commit or push changes.

The [update workflow](Java-Crypto-Roadmap-Update-Workflow.md) contains the complete instructions; it does not depend on a separately installed skill. It refreshes both released changes and plans, preserves previous files, validates the workbook against the source and JSON, and then advances its Current baseline section. Simply opening the Markdown file does not run an update.

## Scope and interpretation

- The catalog reflects the **published Oracle cryptographic roadmap**, not every cryptographic change in every JDK release note. It describes Oracle's bundled implementations and policies; it does not assess third-party providers or an application's runtime configuration.
- A blank JDK cell means **not explicitly listed**, rather than proof that the change is absent. A newer major release may have inherited a feature without appearing in a backport row.
- Released changes and future plans stay separate. A planned date passing does not establish delivery. A release date also differs from a certificate issuance cutoff or other effective condition.
- The JSON preserves exact listed versions, including builds. A viewer should compare numeric versions **within the selected JDK family**, rather than using release dates alone. Build-sensitive comparisons require a build number. See the workflow for the comparison rules.
- `-perf` deliveries are excluded. Crypto changes have no CVE severity or CVSS score unless a separate, evidenced CVE relationship is added later.

## Repository contents

| Location | Purpose |
| --- | --- |
| `baseline/` | Original workbook, normalized JSON, and captured Oracle source evidence |
| `outputs/YYYY-MM-DD/` | Future validated updates and their evidence; created when needed |
| `Java-Crypto-Roadmap-Update-Workflow.md` | Instructions and authoritative pointer to the current baseline |
| `scripts/read_roadmap.py` | Optional Python 3 helper to fetch and parse Oracle's source data without executing JavaScript |
| `validation/2026-11-25.md` | Initial validation results and known source limitations |

The helper uses only Python's standard library. It extracts source data; it does **not** regenerate the workbook or advance the baseline by itself:

```sh
python3 scripts/read_roadmap.py --output /tmp/oracle-crypto-roadmap.json
```

The workbook and JSON can be read without Python. A browser application can embed the JSON at build time and run entirely offline; no database server is required.

Official sources: [Oracle cryptographic roadmap](https://www.java.com/en/jre-jdk-cryptoroadmap.html) and [technical guidance](https://www.java.com/en/configure_crypto.html).
