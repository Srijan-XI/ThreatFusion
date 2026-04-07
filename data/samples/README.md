# ThreatFusion Sample Data Guide

This folder contains test artifacts for validating scanner behavior.

## Expected Outcomes

1. `sample.txt`
- Expected: benign / low risk
- Purpose: baseline control

2. `benign_system_report.txt`
- Expected: benign / low risk
- Purpose: false-positive control for common admin commands

3. `suspicious_test.txt`
- Expected: medium to high risk
- Signals: suspicious APIs, URLs, command execution strings

4. `suspicious_powershell_log.txt`
- Expected: high risk
- Signals: encoded PowerShell patterns, bypass flags, process injection APIs

5. `threat_ioc_bundle.txt`
- Expected: high risk
- Signals: IOC-heavy indicators (domains, URLs, IPs, LOLBins, persistence keys)

6. `network_scan_artifact.log`
- Expected: medium to high risk
- Signals: recon/lateral movement style command chain

7. `macro_dropper_simulation.vbs`
- Expected: medium risk
- Signals: script execution + suspicious API marker strings

8. `malicious_script.sh`
- Expected: high to critical risk
- Signals: payload download, exfiltration command patterns, reverse shell style syntax

9. `edge_case_mixed_signals.txt`
- Expected: medium risk (mixed)
- Purpose: threshold tuning (benign + suspicious overlap)

## Notes

- These are simulation artifacts for local testing and scoring validation.
- They are intentionally text-based and non-executable in normal workflows.
- Use this set to verify both detection sensitivity and false-positive handling.
