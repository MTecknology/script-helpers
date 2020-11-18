test: test_shell test_py

test_shell:
	sh ./tests/test_shell

test_py:
	#pytest

.PHONY: test test_shell test_py
