export WORKSPACE ?= $(abspath $(PWD)/)

.PHONY: clean
clean:
	rm -rf \
		_build \
		docs/helpers/*.rst

.PHONY: docs
docs: clean
	sphinx-build docs/ _build/docs/

.PHONY: test
test: test_shell

.PHONY: test_shell
test_shell:
	sh ./tests/test_shell

#.PHONY: test_py
#test_py:
#	pytest
