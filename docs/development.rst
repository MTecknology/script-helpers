Development
===========

To Do...

Code Standards
--------------

In general, coding standards follow language-defined specificaitons--PEP8 and
POSIX for example.

Requirements:

- **ALL** new features **MUST** come with test units.
- Keep commits small, well-documented, and signed.

Shell Notes
-----------

**printf vs. echo:**

The use of echo should typically be avoided because it can have unexpected
behavior between different shells when certain values (leading options,
backslashes, etc.) are provided.

**find w/ xargs:**

The ``-print0`` and ``-0`` options are GNU extensions and should not be used.
Additionally, piping find directly into xargs can be problematic. To address
these issues, the following form should be used:

.. code-block:: sh
    find ... | sed 's/./\\&/g' | xargs command

**quotes:**

Use them!

**case:**

A leading ``(`` for each component is optional. For the sake of syntax
highlighting and making a choice... it's not optional.

**subshells:**

Do not use subshells unless absolutely necessary. These can potentially hide
errors, return codes, etc.

**0-9 vs. 123..:**

In ``case`` statements, spell out ``[0123456789])`` instead of ``[0-9])``. Some
very obsure locales have extra characters between 0 and 9.
