# Contributing to ThreatFusion 🤝

Thanks for helping improve ThreatFusion. We welcome contributions from beginners and experienced maintainers alike.

ThreatFusion combines threat analysis, network inspection, reporting, and a web interface. Because this is a multi-language repository (Python, C++, Go, and web code), this guide explains how to contribute safely and effectively.

## 🌟 Ways You Can Contribute

- 🐞 Report reproducible bugs
- ✨ Propose new detection features
- 🛡️ Improve security checks and hardening
- 🧪 Add tests and improve reliability
- 📚 Improve docs and developer guides
- ⚡ Optimize performance in scanning and analysis pipelines

## 🚀 Quick Start

1. Fork the repository.
2. Create a branch from the default branch:
   - `git checkout -b feat/short-description`
3. Create and activate a virtual environment (Windows PowerShell):
   - `py -3 -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Run the app:
   - `python run.py`

Optional web interface setup:

- `cd web`
- `npm install`
- `npm run dev`

## 🧭 Project Areas (What to Touch)

- `analyzer_py/`: detection and heuristics logic
- `network/`: network analysis features
- `ml_module/`: anomaly detection and training tooling
- `core/`: logging, reporting, and error handling
- `web/`: UI dashboard and API integration
- `scanner_cpp/` and `net_analyzer_go/`: performance/scanning helpers

When possible, keep a PR scoped to one area. Smaller, focused changes are easier to review and merge.

## 🧱 Development Guidelines

- Keep pull requests focused and atomic.
- Follow existing naming and style patterns.
- Prefer clear, explicit logic over clever but hard-to-read shortcuts.
- Add short comments for complex logic that would otherwise be hard to understand.
- Do not commit generated output files unless the change explicitly requires them.

## ✅ Testing and Validation Expectations

Before opening a PR, validate the impacted area:

- Run the relevant scripts (for example, demos or analyzers) affected by your change.
- If modifying the web app, verify core pages load and basic flows work.
- If modifying scanners/analyzers, include sample output or logs proving behavior.
- Confirm your changes do not break existing workflows.

Good PR evidence includes:

- command(s) executed
- output snippets
- screenshots (for UI changes)
- before/after behavior notes

## 🧾 Commit Message Guidance

Use clear, action-oriented commit messages:

- `feat: add heuristic for suspicious obfuscation pattern`
- `fix: handle missing geo cache file gracefully`
- `docs: expand setup steps for web dashboard`

If your change addresses an issue, reference it in the PR description:

- `Closes #123`

## 🔍 Pull Request Checklist

Please make sure your PR includes:

- [ ] Clear summary of what changed
- [ ] Rationale for why this change is needed
- [ ] Validation evidence (logs, screenshots, or command output)
- [ ] Notes about compatibility or migration impact (if any)
- [ ] Documentation updates (if behavior or setup changed)

## 🛡️ Security and Sensitive Data Rules

- Never commit API keys, tokens, credentials, or private datasets.
- Avoid logging sensitive data in plaintext.
- Use placeholders for secrets in docs and examples.
- For vulnerabilities, do **not** create a public issue. Follow `SECURITY.md`.

## 🐛 Bug Reports and ✨ Feature Requests

Use the issue templates in `.github/ISSUE_TEMPLATE/`.

Helpful bug reports include:

- exact steps to reproduce
- expected behavior
- actual behavior
- environment details (OS, Python version, branch/commit)
- relevant stack traces/logs

Helpful feature requests include:

- problem statement
- expected user value
- proposed approach
- alternatives considered

## 🙌 Contributor Etiquette

- Be respectful and constructive in discussions.
- Assume good intent.
- Offer actionable feedback when reviewing others.
- Keep collaboration professional and kind.

## 📄 License and Contribution Terms

By contributing, you agree your contributions are provided under the repository's license.

Thanks again for helping make ThreatFusion better. 💙