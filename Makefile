.PHONY: validate test skills search route index check

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

check: validate test
