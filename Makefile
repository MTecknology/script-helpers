export WORKSPACE ?= $(abspath $(PWD)/)

# Clean up build artifacts
.PHONY: clean
clean:
	rm -rf _build docs/helpers/*.rst

# Build documentation
.PHONY: docs
docs: clean
	sphinx-build docs/ _build/docs/

# Run all tests
.PHONY: test
test: test_shell shellcheck

# Run only shell tests
.PHONY: test_shell
test_shell:
	sh ./tests/test_shell

# Run only shellcheck tests
.PHONY: shellcheck
shellcheck:
	shellcheck lib/shell tests/test_shell

# Run only python tests
#.PHONY: test_py
#test_py:
#	pytest
