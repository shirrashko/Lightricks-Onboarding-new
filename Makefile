.PHONY: lint format

# Linting the code
lint:
	flake8 --max-line-length=120 ./source

# Formatting the code
format:
	black --line-length 110 ./source

