doc: doc_shell

doc_shell:
	./misc/build_shelldoc

test: test_shell test_py

test_shell:
	sh ./tests/test_shell

test_py:
	#pytest

.PHONY: doc doc_shell test test_shell test_py
