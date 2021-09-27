export WORKSPACE ?= $(abspath $(PWD)/)

# Clean up build artifacts
.PHONY: clean
clean:
	@#rm -rf _build docs/helpers/*.rst
	git clean -fxd

# Build documentation
.PHONY: docs
docs:
	sphinx-build docs/ _build/docs/

# Run all tests
.PHONY: test
test: test_py3 test_shell shellcheck

# Run only py3 tests
.PHONY: test_py3
test_py3:
	python3 -m pytest --rootdir=tests/test_py3

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
