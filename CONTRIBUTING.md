# Contributing to Bug Hunter Toolkit

Thank you for contributing to bug bounty and security research tooling! 🛡️

## Ways to Contribute

- 🐛 Bug reports & fixes
- ✨ New security modules or checks
- 📖 Documentation & guides
- 🧪 Tests & wordlists
- 🗺️ Methodology improvements

## ⚠️ Contribution Ethics

All contributions must be for **defensive and authorized security testing** only. We do not accept contributions that:
- Target specific organizations without authorization
- Include illegal exploits or malware
- Violate responsible disclosure practices

## Getting Started

### 1. Fork & Clone

```bash
git fork https://github.com/codebytaki/bug-hunter-toolkit
git clone https://github.com/YOUR_USERNAME/bug-hunter-toolkit
cd bug-hunter-toolkit
```

### 2. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/new-module
git checkout -b fix/scanner-bug
```

### 4. Make Changes

- Follow existing code structure in `src/`
- Add tests in `tests/`
- Update README if adding new features
- Add examples in `examples/`

### 5. Test

```bash
pytest tests/ -v
pytest tests/ --cov=src
```

### 6. Commit (Conventional Commits)

```bash
git commit -m "feat: add SSRF detection module"
git commit -m "fix: handle timeout in port scanner"
git commit -m "docs: add SQLi detection examples"
```

### 7. Push & Open PR

```bash
git push origin feature/new-module
```

## Code Standards

- PEP 8 for Python
- Type hints on public functions
- Docstrings with parameters and return values
- Error handling for network operations

## Security Module Guidelines

When adding a new scanner/module:

1. Place in appropriate `src/` subdirectory
2. Include rate limiting to avoid overloading targets
3. Always check for authorization headers/flags
4. Include a `--dry-run` flag for safe testing

## Pull Request Guidelines

- One feature/fix per PR
- Include test cases
- Update docs/README for new features
- Pass all CI checks

## Questions?

Open a [Discussion](https://github.com/codebytaki/bug-hunter-toolkit/discussions) or [Issue](https://github.com/codebytaki/bug-hunter-toolkit/issues).
