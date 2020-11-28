.. _samples_shell:

Shell Samples
=============

Basic Skeleton
--------------

.. code-block:: sh

    #!/bin/sh
    ##
    # Manage an imaginary build process.
    ##
    . /path/to/shell


    main() {
        safety_checks
        parse_options "$@"

        # Grab a lock
        lock acquire "$0" ||
                die 'Another process seems to be running.'

        # Wipe temp job cache, if present
        if [ -e '/tmp/razzle' ]; then
            log "$INFO" 'Incomplete job detected; deleting...'
            rm -rf '/tmp/razzle'
        fi

        log "$DEBUG" "Kicking things off at approx. $(date)."

        # Kick off CI/CD process
        run_cicd

	# Get build status
        build_status="$(get_cicd 'status')"
        if is_true "$build_status"; then
            log "$INFO" 'SUCCESS: Razzle dazzle, baby!'
            #[...]
        fi

        log "$DEBUG" "Ending things at exactly $(date)."

        # Release the lock
        lock destroy "$0"
    }


    safety_checks() {
        detect_release || die 'Unable to detect release.'

        # Check minimum helpers version
        helper_version '1.0.0' ||
                die 'Must have shell_helpers >= 1.0.0'

        # Check host
        is_release '20.04' '20.10' ||
                die 'Only *buntu 20.04 and 20.10 are supported.'
    }


    parse_options() {
        while getopts 'i:h' OPT; do
            case "$OPT" in
                i) export CICD_MAGIC_ID="$OPTARG";;
                h) show_help; exit 1;;
                *) die "Unexpected argument provided: '$OPT'";;
            esac
        done
    }


    show_help() {
        cat <<-EOF
    Run a CICD build.

    Usage: script_name [options]

    Options:
      -i X\tExports CICD_MAGIC_ID for build process
      -h\tPrint this help text and exit
    EOF
    }


    run_cicd() {
        :
    }


    main "$@"
