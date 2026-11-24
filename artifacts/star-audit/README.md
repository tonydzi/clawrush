# Star event inspection prototype

Educational single-file prototype; Python 3.9+, standard library only. This is an artifact in an existing repository, not a new packaged product.

Download `star_audit.py` beside this README, then run:

```sh
python3 star_audit.py psf/requests --pages 5 --sample 60 --json
```

Optional `GITHUB_TOKEN` environment variable raises API quota. The tool does not search files for credentials and writes no local telemetry. It reads public repository/profile data and a public GH Archive mirror, falling back when the API errors or the requested pages exceed its bound.

The sample is systematic, not random. Archive completeness/freshness is unknown; inspect event dates separately. Profiles are current, while stars may be historical. Empty or deleted accounts do not establish bot identity. Missing accounts are nevertheless counted in the flagged-profile numerator by this heuristic; do not interpret that numerator as bot prevalence. Thresholds are unvalidated heuristics and do not prove purchases by repository owners. Color labels are only triage hints. A 404 is an observed response, not proof of a GitHub-wide policy.

Tests: `python3 -m unittest _test_star_audit`. Synthetic tests check mechanics only, not detection accuracy. The prototype was used internally on three public projects; another person's independent usability trial has not been recorded, so release confidence remains limited.

MIT. Invented by Mycroft and Tony, Palo Alto AI Research Lab. https://github.com/tonydzi
