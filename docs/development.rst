.. _dev:

Development
===========

Code Standards
--------------

In general, coding standards follow language-defined specificaitons--PEP8 and
POSIX for example.

Requirements:

- **ALL** new features **MUST** come with test units.
- Keep commits small, well-documented, and signed.

Shell Notes
-----------

.. seealso::

    These notes apply **only** to shell library development!

    This library is built with many edge cases in mind. In practice, it's
    unlikely these situations will even be encountered. For example, ``[0-9]``
    is not used in the extremely unlikely chance it is not expanded to
    ``0123456789``. This library cares about such edge cases; typical consumer
    scripts should prefer the shorter and more readable form.

    Refer to :ref:`Shell Samples` for general script writing tips.

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

Note: This is why ``version_compare()`` includes the following additional logic:

.. code-block:: sh

    # Check for valid responses or bail early
    case "$_cmp" in
        (1|0|2) :;;     # Expected (valid) resturn values
        (*) die "$_cmp" 'version comparison failed';;
    esac

**[0-9] vs. [012..]:**

In ``case`` statements, spell out ``[0123456789])`` instead of ``[0-9])``. Some
very obsure locales have atypical characters between 0 and 9.

**die():**

In some cases, it will be appropriate to invoke ``die()`` from within the
library. However, it should be avoided whenever possible. It is better to avoid
situations where an early failure may be needed (i.e. prefer shorter/simpler
functions over kitchen-sink solutions)
