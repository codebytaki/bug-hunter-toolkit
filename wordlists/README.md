# Wordlists

This directory contains wordlists for security testing.

## Files

- `common.txt` - Common directory and file names
- Add your custom wordlists here

## Usage

```python
from bug_hunter import SubdomainFinder

finder = SubdomainFinder(domain="example.com")
finder.enumerate(wordlist="wordlists/common.txt")
```

## Note

Always use wordlists responsibly and only on systems you have permission to test.
