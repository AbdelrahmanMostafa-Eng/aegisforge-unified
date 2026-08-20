.PHONY: validate test skills search route index evaluate doctor package check

validate:
	PYTHONPATH=. python3 -m aegisforge validate .

test:
	PYTHONPATH=. python3 -m unittest discover -s tests -v

skills:
	PYTHONPATH=. python3 -m aegisforge skills . --pretty

search:
	PYTHONPATH=. python3 -m aegisforge search "$(QUERY)" --root . --limit 10

route:
	PYTHONPATH=. python3 -m aegisforge route "$(QUERY)" --root . --limit 5

index:
	PYTHONPATH=. python3 -m aegisforge index .

evaluate:
	PYTHONPATH=. python3 -m aegisforge evaluate evaluation/scenarios.json --json

doctor:
	PYTHONPATH=. python3 -m aegisforge doctor .

package:
	python3 -m pip wheel --no-deps . -w dist

check: validate test evaluate doctor
