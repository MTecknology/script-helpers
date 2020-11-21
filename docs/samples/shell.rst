Shell Samples
=============

Basic Skeleton::

    #!/bin/sh
    . /path/to/shell

    # Check minimum helpers version
    helper_version '1.0.0' || die 'Must have shell_helpers >= 1.0.0'

    # Check host
    is_release '20.04' '20.04' ||
            die 'Only Ubuntu 20.04 and 20.10 are supported.'

    # Grab a lock
    lock acquire "$0" || die 'Another process seems to be running.'

    # Wipe temp job cache, if present
    if [ -e '/tmp/razzle' ]; then
        log "$INFO" 'Incomplete job detected; deleting...'
        rm -rf '/tmp/razzle'
    fi

    log "$DEBUG" "Kicking things off at approx. $(date)."

    # Kick off CI/CD process
    #[...]

    if is_true "$build_status"; then
        log "$INFO" 'SUCCESS: Razzle dazzle, baby!'
        #[...]
    fi

    log "$DEBUG" "Ending things at exactly $(date)."

    # Release the lock
    lock destroy "$0"
