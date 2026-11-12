# Network & Data Flow Segmentation: QC Anomaly Detection Pipeline

## Current State (As-Built)

This pipeline currently runs **locally**, on a single machine, with
**no network connectivity** between it and plant OT systems (lab
instruments, SCADA, PLCs). Data enters via manually exported Excel
files from the LIMS system.


This is the **lowest-risk possible architecture** from a cybersecurity
standpoint — there is no attack surface from the network, because
there is no network connection. The tradeoff is that it doesn't scale:
every batch requires a human to export and transfer the file.

## Target State (Future, if Automated)

If this pipeline is later connected directly to the LIMS system or
plant network for automation, it must be placed correctly relative to
IT/OT segmentation (per the Purdue model referenced in the capstone's
reference architecture):


**Key segmentation principle:** the QC Detector Pipeline should sit on
the **IT side (Level 4-5)**, consuming data FROM the LIMS system via
the DMZ, and should **never** have direct read/write access to Level
0-2 OT devices (lab instruments, PLCs). This is standard practice:
analytics and AI workloads belong on IT infrastructure, not embedded
in or directly connected to operational control systems.

## Data Flow Trust Boundaries

| Boundary | Current | Target (Automated) |
|---|---|---|
| Lab instrument -> LIMS | Trusted (physical/vendor-controlled) | Same |
| LIMS -> QC Pipeline | Manual file transfer (air-gapped) | Should cross DMZ, read-only, authenticated |
| QC Pipeline -> Alert output | Local file/console | Should be access-controlled if shared |

## Recommendation

Until there is a documented, approved automated data path (API or
scheduled export with access control) from LIMS to this pipeline, the
current manual, air-gapped approach is **appropriate and should not be
changed casually**. Automating this connection without addressing
authentication, network segmentation, and the DMZ boundary would
introduce new risk for marginal convenience gain.

