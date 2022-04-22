#!/bin/sh
##
# Title:      Script Helpers (sh)
# Copyright:  2020 Michael Lustfield <MTecknology>
# License:    GPL-3+
##
# Documentation: https://script-helpers.readthedocs.io/en/latest/helpers/shell.html
# Usage: https://script-helpers.readthedocs.io/en/latest/samples/shell.html
##


##
# Convenience Variables
##

# Version of this script
SCRIPT_HELPER_VERSION='dev'
readonly SCRIPT_HELPER_VERSION
export SCRIPT_HELPER_VERSION

# Log Levels
DEBUG=0; D=0
INFO=1; I=1
WARN=2; W=2
ERROR=3; E=3
readonly DEBUG D INFO I WARN W ERROR E
export DEBUG D INFO I WARN W ERROR E


##
# Helper Functions
##


##
# Check if a command (or alias/function) is available.
#
# **Usage:** command_present bin
#
# - bin: name of command
#
# .. code-block:: sh
#
#    for cmd in 'grep' 'xterm'; do
#        command_present "$cmd" || die "$cmd not found"
#    done
##
command_present() {
	command -v "$1" >/dev/null && return 0
	alias | grep -q "\s$1=" 2>/dev/null && return 0
	return 1
}


##
# Run all detection routines.
#
# **Usage:** detect_all
#
# **Returns:** true if all detections succeed
#
# .. code-block:: sh
#
#    detect all || die 'Detections failed'
##
detect_all() {
	_e='0'
	detect_arch || _e='1'
	detect_codename || _e='1'
	detect_distro || _e='1'
	detect_init || _e='1'
	detect_kernel || _e='1'
	detect_release || _e='1'
	detect_virtual || _e='1'

	return "$_e"
}


##
# Detect architecture of running system.
#
# **Usage:** detect_arch
#
# **Returns:** true if detection succeeds
#
# **Exports:** H_ARCH
#
# .. code-block:: sh
#
#    detect_arch || die 'Architecture is not supported'
##
detect_arch() {
	if command_present 'uname'; then
		H_ARCH="$(uname -m)"; export H_ARCH
		return 0
	fi

	return 1
}


##
# Detect codename of running system.
#
# **Usage:** detect_codename
#
# **Returns:** true if detection succeeds
#
# **Exports:** H_CODENAME
#
# .. code-block:: sh
#
#    detect_codename || die 'Distro codename not found'
##
detect_codename() {
	if command_present 'lsb_release'; then
		_codename_lsb && return 0
	fi;if [ -f '/etc/os-release' ]; then
		_codename_release && return 0
	fi;if command_present 'sw_vers'; then
		_codename_swvers && return 0
	fi;if command_present 'freebsd-version'; then
		# FreeBSD does not have release code names
		export H_CODENAME=''
		return 0
	fi

	log "$WARN" 'Unable to determine release codename.'
	return 1
}

# Detect release codename using lsb_release
_codename_lsb() {
	H_CODENAME="$(to_lower "$(lsb_release --short --codename)")"
	export H_CODENAME
}

# Detect codename from os-release
_codename_release() {
	if command_present 'awk'; then
		H_CODENAME="$(to_lower "$(awk -F '=' '/^VERSION_CODENAME=/{print $2}' /etc/os-release)")"
		H_CODENAME="$(printf '%s' "$H_CODENAME" | sed 's/"//g')"
		if [ -n "$H_CODENAME" ]; then
			export H_CODENAME
			return 0
		fi
	fi
}

# Detect codename of Mac systems
# Note: sw_vers identifies a mac, but the tool is very limited
_codename_swvers() {
	H_CODENAME="$(to_lower "$(awk '/SOFTWARE LICENSE AGREEMENT FOR/' '/System/Library/CoreServices/Setup Assistant.app/Contents/Resources/en.lproj/OSXSoftwareLicense.rtf' | sed 's/macOS/OS X/' | awk -F 'OS X ' '{print $NF}' | awk '{print substr($0, 0, length($0)-1)}')")"
	export H_CODENAME
}


##
# Detect distribution of running system.
#
# **Usage:** detect_distro
#
# **Returns:** true if detection succeeds
#
# **Exports:** H_DISTRO
#
# .. code-block:: sh
#
#    detect_distro || die 'Distribution is not supported'
##
detect_distro() {
	if [ -n "$H_KERNEL" ]; then
		_kern="$H_KERNEL"
	else
		_kern="$(to_lower "$(detect_kernel; printf '%s' "$H_KERNEL")")"
	fi

	if command_present 'lsb_release'; then
		_distro_lsb && return 0
	fi;if [ -f '/etc/os-release' ]; then
		_distro_release && return 0
	fi;if command_present 'sw_vers'; then
		_distro_swvers && return 0
	fi;if [ "$_kern" = 'freebsd' ]; then
		_distro_freebsd && return 0
	fi

	log "$WARN" 'Unable to determine running distro.'
	return 1
}

# Detect release of Linux systems
_distro_lsb() {
	H_DISTRO="$(to_lower "$(lsb_release --short --id)")"
	export H_DISTRO
	return 0
}

# Detect release from /etc/*release* file
_distro_release() {
	if command_present 'awk'; then
		H_DISTRO="$(to_lower "$(awk -F '=' '/^ID=/{print $2}' /etc/os-release)")"
		if [ -n "$H_DISTRO" ]; then
			export H_DISTRO
			return 0
		fi
	fi;if command_present 'sed'; then
		H_DISTRO="$(to_lower "$(printf '%s' "$H_DISTRO" | sed 's/"//g')")"
		if [ -n "$H_DISTRO" ]; then
			export H_DISTRO
			return 0
		fi
	fi
	return 1
}

# Detect release of Mac systems
_distro_swvers() {
	export H_DISTRO='macosx'
	return 0
}

# Detect release of FreeBSD systems
_distro_freebsd() {
	export H_DISTRO='freebsd'
	return 0
}


##
# Detect init of running system.
#
# **Usage:** detect_init
#
# **Returns:** true if detection succeeds
#
# **Exports:** H_INIT
#
# .. code-block:: sh
#
#    detect_init || die 'Init detection failed'
##
detect_init() {
	if [ -n "$H_KERNEL" ]; then
		_kern="$H_KERNEL"
	else
		_kern="$(to_lower "$(detect_kernel; printf '%s' "$H_KERNEL")")"
	fi

	if [ "$_kern" = 'freebsd' ]; then
		export H_INIT='bsd-init'
		return 0
	elif [ "$_kern" = 'darwin' ]; then
		export H_INIT='launchd'
		return 0
	elif [ -f '/sbin/init' ]; then
		_init_sbin && return 0
	fi
	log "$WARN" 'Unable to determine running init.'
	return 1
}

# Try to grab init system from /sbin/init
_init_sbin() {
	if command_present 'grep'; then
		if strings /sbin/init | grep -q 'sysvinit'; then
			export H_INIT='sysvinit'
			return 0
		elif strings /sbin/init | grep -q '/lib/systemd'; then
			export H_INIT='systemd'
			return 0
		elif strings /sbin/init | grep -q 'upstart'; then
			export H_INIT='upstart'
			return 0
		fi
	fi;if command_present 'awk'; then
		_i="$(strings /sbin/init | awk '/(systemd|sysvinit|upstart)/ {print $0}')"
		if in_string 'sysvinit' "$_i"; then
			export H_INIT='sysvinit'
			return 0
		elif in_string 'systemd' "$_i"; then
			export H_INIT='systemd'
			return 0
		elif in_string 'upstart' "$_i"; then
			export H_INIT='upstart'
			return 0
		fi
	fi
}


##
# Detect kernel of running system.
#
# **Usage:** detect_kernel
#
# **Returns:** true if detection succeeds
#
# **Exports:** H_KERNEL
#
# .. code-block:: sh
#
#    detect_kernel || die 'Kernel is not supported'
##
detect_kernel() {
	if command_present 'uname'; then
		H_KERNEL="$(to_lower "$(uname -s)")"
		export H_KERNEL
		return 0
	fi

	return 1
}


##
# Detect distro release of running system.
#
# **Usage:** detect_release
#
# **Returns:** true if detection succeeds
#
# **Exports:** H_RELEASE
#
# .. code-block:: sh
#
#    detect_release || die 'Release is not supported'
##
detect_release() {
	if command_present 'lsb_release'; then
		_release_lsb && return 0
	fi;if [ -f '/etc/os-release' ]; then
		_release_release && return 0
	fi;if command_present 'sw_vers'; then
		_release_swvers && return 0
	fi;if command_present 'freebsd-version'; then
		_release_freebsd && return 0
	fi

	log "$WARN" 'Unable to determine distribution release.'
	return 1
}

# Detect release version using lsb_release
_release_lsb() {
	H_RELEASE="$(to_lower "$(lsb_release --short --release)")"
	export H_RELEASE
}

# Detect release from os-release
_release_release() {
	if command_present 'awk'; then
		H_RELEASE="$(to_lower "$(awk -F '=' '/^VERSION_ID=/{print $2}' /etc/os-release)")"
		H_RELEASE="$(printf '%s' "$H_RELEASE" | sed 's/"//g')"
		if [ -n "$H_RELEASE" ]; then
			export H_RELEASE
			return 0
		fi
	fi
}

# Detect release of Mac systems
_release_swvers() {
	H_RELEASE="$(to_lower "$(sw_vers -productVersion)")"
	export H_RELEASE
}

# Detect release of FreeBSD system
_release_freebsd() {
	H_RELEASE="$(to_lower "$(freebsd-version -k)")"
	export H_RELEASE
}


##
# Attempts to detect virtualization platform of running system
#
# **Usage:** detect_virtual
#
# **Exports:** H_VIRTUAL (H_VIRTUAL='' if no platform detected)
#
# .. code-block:: sh
#
#    detect_virtual
#    printf 'Virtualization Platform: %s\n' "$H_VIRTUAL"
##
detect_virtual() {
	if command_present 'dmidecode'; then
		_detect_virt_dmiawk && return 0
	else
		log "$INFO" 'dmidecode not found; H_VIRTUAL accuracy decreased'
	fi;if command_present 'lspci'; then
		_detect_virt_lspci && return 0
	else
		log "$INFO" 'lspci not found; H_VIRTUAL accuracy decreased'
	fi;if command_present 'pciconf'; then
		_detect_virt_pciconf && return 0
	fi

	log "$DEBUG" 'No virtualization platform detected; assuming physical'
	export H_VIRTUAL=''
}

# Detect virtualization using dmidecode + awk
# Note: Only returns true if virt platform found
_detect_virt_dmiawk() {
	if command_present 'awk'; then
		case "$(dmidecode | awk '/Vendor:/ {print $2}')" in
			('QEMU'|'Bochs'|'SeaBIOS')
				export H_VIRTUAL='kvm'
				return 0
				;;
		esac
		case "$(dmidecode | awk '/Manufacturer:/ {print $2}')" in
			('QEMU'|'Bochs'|'oVirt'|'Google')
				export H_VIRTUAL='kvm'
				return 0
				;;
		esac
		case "$(dmidecode | awk '/Product Name:/ {print $2}')" in
			('RHEV')
				export H_VIRTUAL='kvm'
				return 0
				;;
		esac
	fi
	case "$(dmidecode)" in
		# repeated from above, in case awk was not present
		(*'QEMU'*|*'Bochs'*|*'SeaBIOS'*|*'oVirt'*|*'Google'*|*'RHEV'*)
			export H_VIRTUAL='kvm'
			return 0
			;;
		(*'VirtualBox'*)
			export H_VIRTUAL='virtualbox'
			return 0
			;;
		(*'VMWare'*)
			export H_VIRTUAL='vmware'
			return 0
			;;
		(*': Microsoft'*)
			export H_VIRTUAL='virtualpc'
			return 0
			;;
		(*'Parallels'*)
			export H_VIRTUAL='parallels'
			return 0
			;;
	esac
	return 1
}

# Detect virtualization using lspci
# Note: Only returns true if virt platform found
_detect_virt_lspci() {
	case "$(to_lower "$(lspci)")" in
		(*'vmware'*)
			export H_VIRTUAL='vmware'
			return 0
			;;
		(*'virtualbox'*|*'innotek'*)
			export H_VIRTUAL='virtualbox'
			return 0
			;;
		(*'qemu'*|*'virtio'*)
			export H_VIRTUAL='kvm'
			return 0
			;;
	esac
	return 1
}

# Detect virtualization using pciconf
# Note: Only returns true if virt platform found
_detect_virt_pciconf() {
	case "$(to_lower "$(pciconf -lv)")" in
		(*'innotek'*)
			export H_VIRTUAL='kvm'
			return 0
			;;
	esac
	return 1
}


##
# Print a formatted (critical) message and exit with status.
#
# **Usage:** die [exit_status] message
#
# - exit_status: exit code to use with script termination (default: 1)
# - message: message to print before terminating script execution
#
# .. code-block:: sh
#
#    [ -n "$foo" ] || die 255 '$foo not defined'
##
die() {
	# If first argument was an integer, use as exit_status
	case "$1" in
		(*[!0123456789]*) _exit_status=1;;
		(*) _exit_status="$1"; shift;;
	esac

	printf '*** CRITICAL: %s ***\n' "$1"
	exit "$_exit_status"
}


##
# Check if string ends with another string
#
# **Usage:** ends_with key str
#
# - key: string to search for
# - str: ascii string to search
#
# **Returns:** true if str ends with key
#
# .. code-block:: sh
#
#    ends_with 'init' "$input" || die 'invalid input'
##
ends_with() {
	[ "$1" = "$2" ] && return 0
	case "$2" in
		(*"$1") return 0;;
		(*) return 1;;
	esac
}


##
# Return true if script version is between min/max ('dev' == git_HEAD).
#
# **Usage:** helper_version min [max]
#
# - min: minimum supported version
# - max: maximum supported version
#
# **Returns:** true if script version is between min and [optionally:max]
#
# .. code-block:: sh
#
#    helper_version '1.2' ||
#        die 'Helper version >= 1.2 required!'
##
helper_version() {
	# Check minimum version
	if [ "$SCRIPT_HELPER_VERSION" != 'dev' ]; then
		version_compare "$SCRIPT_HELPER_VERSION" 'lesser_than' "$1" && return 1
	fi

	# Check maximum version
	[ "${2:-dev}" = 'dev' ] && return 0
	[ "$SCRIPT_HELPER_VERSION" = 'dev' ] && return 1
	version_compare "$SCRIPT_HELPER_VERSION" 'greater_than' "$2" && return 1

	return 0
}


##
# Check if a value is present in a string.
#
# **Usage:** in_string needle haystack
#
# - needle: value to search for
# - haystack: string to be searched
#
# **Returns:** true if needle was found
#
# .. code-block:: sh
#
#    in_string 'fuz' 'abcfuz123' && echo 'found some fuz'
##
in_string() {
	case $2 in
		(*"$1"*) return 0;;
		(*) return 1;;
	esac
}


##
# A best-effort attempt to check if the internet is accepssible.
#
# **Usage:** internet_accessible
#
# **Defaults:**
#
# - env[PING_HOST]: google.com
# - env[PING_ADDR]: 8.8.8.8
#
# **Returns:** true if internet was probed
#
# .. code-block:: sh
#
#    internet_accessible || die 'Cannot reach the internet'
##
internet_reachable() {
	PING_HOST="${PING_HOST:-google.com}"
	PING_ADDR="${PING_ADDR:-8.8.8.8}"
	if command_present 'wget'; then
		wget -q --spider "http://$PING_HOST/" && return 0
	elif command_present 'ping'; then
		ping -qc 1 "$PING_ADDR" >/dev/null && return 0
	else
		log "$WARN" 'Unable to check internet connection.'
	fi
	return 1
}


##
# Evaluate if running arch matches provided argument(s).
#
# **Usage:** is_arch match [match..]
#
# - match: any string to test against (i386, x86_64, etc.)
#
# **Returns:** true if running arch matches a provided 'match'
#
# .. code-block:: sh
#
#    is_arch 'i386' 'x86_64' || die 'Architecture not supported'
##
is_arch() {
	if [ -n "$H_ARCH" ]; then
		_needle="$H_ARCH"
	else
		_needle="$(detect_arch; printf '%s' "$H_ARCH")"
	fi
	[ -n "$_needle" ] || die 7 'Could not detect distro.'
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}


##
# Evaluate if running codename matches provided argument(s).
#
# **Usage:** is_codename match [match..]
#
# - match: any string to test against (buster, catalina, etc.)
#
# **Returns:** true if running codename matches a provided 'match'
#
# .. code-block:: sh
#
#    is_codename 'buster' || die 'Only Debian buster is supported'
##
is_codename() {
	if [ -n "$H_CODENAME" ]; then
		_needle="$H_CODENAME"
	else
		_needle="$(detect_codename; printf '%s' "$H_CODENAME")"
	fi
	# Skipped because FreeBSD has no "codename"
	#[ -n "$_needle" ] || die 7 'Could not detect codename.'
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}


##
# Evaluate if running distribution matches provided argument(s).
#
# **Usage:** is_distro match [match..]
#
# - match: any string to test against (debian, ubuntu, etc.)
#
# **Returns:** true if running distro matches a provided 'match'
#
# .. code-block:: sh
#
#    is_distro 'debian' || die 'Only Debian is supported'
##
is_distro() {
	if [ -n "$H_DISTRO" ]; then
		_needle="$H_DISTRO"
	else
		_needle="$(detect_distro; printf '%s' "$H_DISTRO")"
	fi
	[ -n "$_needle" ] || die 7 'Could not detect distro.'
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}


##
# Evaluate if a given string is not true-like.
#
# **Usage:** is_false str
#
# - str: any string to test against
#
# **Returns:** true if ($str != 0) or (lower($str) != true)
#
# .. code-block:: sh
#
#    is_false 'lies' || die 'I am too gullible'
##
is_false() {
	is_true "$1" && return 1
	return 0
}


##
# Evaluate if running init matches provided argument(s).
#
# **Usage:** is_init match [match..]
#
# - match: any string to test against (sysv, systemd, etc.)
#
# **Returns:** true if running init matches a provided 'match'
#
# .. code-block:: sh
#
#    is_init 'sysv' || die 'Only sysv is supported'
##
is_init() {
	if [ -n "$H_INIT" ]; then
		_needle="$H_INIT"
	else
		_needle="$(detect_init; printf '%s' "$H_INIT")"
	fi
	[ -n "$_needle" ] || die 7 'Could not detect init.'
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}


##
# Evaluate if a given string is an integer.
#
# **Usage:** is_int str
#
# - str: any string to test against
#
# **Returns:** true if str is an integer
#
# .. code-block:: sh
#
#    is_int "$foo" || die 'Argument must be an integer.'
##
is_int() {
	_i="$1"
	[ "$(printf "%.1s" "$_i")" = '-' ] &&
		_i="$(printf '%s' "$1" | cut -c2-)"
	case "$_i" in
		('') return 1;;
		(*[!0123456789]*) return 1;;
		(*) return 0;;
	esac
}


##
# Evaluate if running kernel matches provided argument(s).
#
# **Usage:** is_kernel match [match..]
#
# - match: any string to test against (Linux, BSD, etc.)
#
# **Returns:** true if running kernel matches a provided 'match'
#
# .. code-block:: sh
#
#    is_kernel 'Linux' 'BSD' || die 'Only Linux/BSD are supported'
##
is_kernel() {
	if [ -n "$H_KERNEL" ]; then
		_needle="$H_KERNEL"
	else
		_needle="$(detect_kernel; printf '%s' "$H_KERNEL")"
	fi
	[ -n "$_needle" ] || die 7 'Could not detect kernel.'
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}


##
# Evaluate if running distro release matches provided argument.
#
# **Usage:** is_release match [match..]
#
# - match: any string to test against (12.04, 10.1, etc.)
#
# **Returns:** true if running release matches a provided 'match'
#
# .. code-block:: sh
#
#    is_release '14.04' '16.04' '18.04' '20.04' ||
#        die 'Only non-EOL LTS releases are supported'
##
is_release() {
	if [ -n "$H_RELEASE" ]; then
		_needle="$H_RELEASE"
	else
		_needle="$(detect_release; printf '%s' "$H_RELEASE")"
	fi
	[ -n "$_needle" ] || die 7 'Could not detect release.'
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}


##
# Evaluate if a given string is true-like (True, TrUE, true, 0).
#
# **Usage:** is_true str
#
# - str: any string to test against
#
# **Returns:** true if ($str is 0) or (lower($str) == true)
#
# .. code-block:: sh
#
#    is_true "$foo" || die "\$foo said it isn't so..."
##
is_true() {
	# Everything to lower-case (True|TRUE|trUe -> true)
	_str="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
	[ "$_str" = 'true' ] && return 0
	[ "$_str" = '' ] && return 1
	# False if number is non-zero.
	is_int "$_str" || return 1
	[ "$_str" -eq '0' ] 2>/dev/null && return 0

	return 1
}


##
# Evaluate if the current system is running on a virtualization platform.
#
# **Usage:** is_virt [type..]
#
# - type: if provided, check if virt platform matches at least one type
#
# **Returns:** true if virtual OR if H_VIRT==type
#
# .. code-block:: sh
#
#    is_virtual && die 'Must be run on physical hardware'
#    is_virtual 'kvm' || die 'Only KVM is supported'
##
is_virtual() {
	if [ -n "${H_VIRTUAL+physical}" ]; then
		_needle="$H_VIRTUAL"
	else
		_needle="$(detect_virtual; printf '%s' "$H_VIRTUAL")"
	fi
	[ -n "${_needle+phys}" ] || die 7 'Could not detect virtualization platform.'

	# If no [type] was provided]
	if [ -z "$1" ]; then
		[ -n "$_needle" ] && return 0
		return 1
	fi
	
	for _hay in "$@"; do
		[ "$_needle" = "$_hay" ] && return 0
	done

	return 1
}



##
# Manage a lock file.
#
# **Usage:** lock operation [key]
#
# - operation: acquire, destroy
# - key: any unique value to identify this script (default: $0)
#
# **Returns:** true if success
#
# .. code-block:: sh
#
#    lock acquire "$0" || die 'Unable to grab lock.'
#    [...]
#    lock destroy "$0"
##
lock() {
	_h="$(printf '%s' "${2:-$0}" | cksum | awk '{print $1}')"
	case "$1" in
		(acquire) _lock_acquire "/tmp/$_h.lock";;
		(destroy) rm -f "/tmp/$_h.lock";;
	esac
}

# Create a lock file and populate it with PID.
_lock_acquire() {
	# Check if running
	[ -e "$1" ] && kill -0 "$(cat "$1")" && return 1

	# make sure the lockfile is removed when we exit and then claim it
	# shellcheck disable=SC2064 #[we want this expanding now]
	trap "rm -f '$1'; exit" INT TERM EXIT
	echo $$ > "$1"

	return 0
}


##
# Print a formatted message if env[LOG_LEVEL] >= level.
#
# **Usage:** log level message
#
# - level: 0:debug, 1:info, \*2:warn, 3:error
# - message: any string of text to be sent to stdout
#
# **Defaults:**
#
# - env[LOG_LEVEL]: 2
#
#
# .. code-block:: sh
#
#    log "$INFO" 'Capturing quantum stabilizer'
#    capture_qs || die 'Capture failed!'
##
log() {
	if [ "${LOG_LEVEL:-2}" -le "$1" ]; then
		case "$1" in
			(0) _lvl='DEBUG';;
			(1) _lvl='INFO';;
			(2) _lvl='WARN';;
			(3) _lvl='ERROR';;
			(*) _lvl='UNKNOWN';;
		esac

		printf '*** %s: %s ***\n' "$_lvl" "$2"
	fi
}


##
# Find/replace substrings in a string.
#
# **Usage:** replace_substring input find repl
#
# - input: full string to be manipulated
# - find: key to search for
# - repl: what to replace "key" with
#
# **Prints:** modified string
#
# .. code-block:: sh
#
#    log "$E" "$(replace_substring "$err" "$secret" '****')"
##
replace_substring() {
	if ! in_string "$2" "$1"; then
		printf '%s' "$1"
		return 0
	fi
	if command_present 'awk'; then
		printf '%s' "$1" | awk -v f="$2" -v r="$3" 'gsub(f, r)'
	else
		die '7' 'Unable to replace_substring().'
	fi
}


##
# Check if string starts with another string
#
# **Usage:** starts_with key str
#
# - key: string to search for
# - str: ascii string to search
#
# **Returns:** true if str starts with key
#
# .. code-block:: sh
#
#    starts_with 'init' "$input" || die 'invalid input'
##
starts_with() {
	[ "$1" = "$2" ] && return 0
	case "$2" in
		("$1"*) return 0;;
		(*) return 1;;
	esac
}


##
# Convert string from [:upper:] to [:lower:].
#
# **Usage:** to_lower str
#
# - str: any ascii string to convert
#
# **Prints:** string in lower
#
# .. code-block:: sh
#
#    low="$(to_lower "$up")"
##
to_lower() {
	printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}


##
# Convert string from [:lower:] to [:upper:].
#
# **Usage:** to_upper str
#
# - str: any ascii string to convert
#
# **Prints:** string in uppercase
#
# .. code-block:: sh
#
#    up="$(to_upper "$low")"
##
to_upper() {
	printf '%s' "$1" | tr '[:lower:]' '[:upper:]'
}


##
# Compare two versions.
#
# **Usage:** version_compare version1 operator version2
#
# - operator:
#
#   + ``-lt``, ``<``, ``lesser_than``
#   + ``-le``, ``<=``, ``lesser_than_or_equal``
#   + ``-gt``, ``>``, ``greater_than``
#   + ``-ge``, ``>=``, ``greater_than_or_equal``
#   + ``-eq``, ``==``, ``equal``
#   + ``-ne``, ``!=``, ``not_equal``
#
# - version{1,2}: arbitrary version strings to compare
#
# **Version Format:** ``[0-9]+($VERSION_SEPARATOR[0-9]+)*`` (i.e. 90, 1.2.3.4)
#
# **Returns:** true if comparison statement is correct
#
# .. code-block:: sh
#
#    version_compare "$_version" '-lt' '1.0' ||
#        die 'Unexpected (pre-release) version found'
##
version_compare() {
	_largest_version "$1" "$3"; _cmp="$?"

	# Check for valid responses or bail early
	case "$_cmp" in
		(1|0|2) :;;     # Expected (valid) resturn values
		(*) die "$_cmp" 'version comparison failed';;
	esac

	# The easy part
	case "$2" in
		('lesser_than'|'-lt'|'<')
			[ "$_cmp" = '2' ] && return 0
			;;
		('lesser_or_equal'|'-le'|'<=')
			[ "$_cmp" = '0' ] && return 0
			[ "$_cmp" = '2' ] && return 0
			;;
		('greater_than'|'-gt'|'>')
			[ "$_cmp" = '1' ] && return 0
			;;
		('greater_or_equal'|'-ge'|'>=')
			[ "$_cmp" = '1' ] && return 0
			[ "$_cmp" = '0' ] && return 0
			;;
		('equal'|'-eq'|'==')
			[ "$_cmp" = '0' ] && return 0
			;;
		('not_equal'|'-ne'|'!=')
			[ "$_cmp" = '1' ] && return 0
			[ "$_cmp" = '2' ] && return 0
			;;
		(*) die 7 'Unknown operatoration called for version_compare().';;
	esac
	return 1
}

##
# Compare two versions.
# Check if one version is larger/smaller/equal than/to another.
#
# **Usage:** _largest_version ver1 ver2
#
# Returns: ($1 > $2): 1 ; ($1 = $2): 0 ; ($1 < $2): 2
# [IOW- 1 = $1 is largest; 0 = neither ; 2 = $2 is largest]
##
_largest_version() (
	# Value used to separate version components
	VERSION_SEPARATOR="${VERSION_SEPARATOR:-.}"

	for _p in "$1" "$2"; do
		[ "$(printf %.1s "$_p")" = "$VERSION_SEPARATOR" ] &&
			die 7 'invalid version pattern provided'
	done

	# Split versions on VER_SEP into int/sub
	_v="$1$2"
	_v1="$1"
	_s1="${1#*"$VERSION_SEPARATOR"}"
	if [ "$_v1" = "$_s1" ]; then
		_s1=''
		_m1="$_v1"
	else
		_m1="${1%%"$VERSION_SEPARATOR"*}"
	fi
	_v2="$2"
	_s2="${2#*"$VERSION_SEPARATOR"}"
	if [ "$_v2" = "$_s2" ]; then
		_s2=''
		_m2="$_v2"
	else
		_m2="${2%%"$VERSION_SEPARATOR"*}"
	fi

	# Both are equal
	[ "$_v1" = "$_v2" ] && return 0

	# Something is larger than nothing (30 < 30.0)
	if [ -n "$_v1" ] && [ -z "$_v2" ]; then
		return 1
	elif [ -z "$_v1" ] && [ -n "$_v2" ]; then
		return 2
	fi

	# Check for invalid
	is_int "$_m1$_m2" || die 7 'invalid version pattern provided'

	# If a ver_sep is present
	if in_string "$VERSION_SEPARATOR" "$_v"; then
		# Check for a larger "major" version number
		[ "$_m1" -lt "$_m2" ] && return 2
		[ "$_m1" -gt "$_m2" ] && return 1

		# Compare substring components
		_largest_version "$_s1" "$_s2"; return "$?"
	else
		# Only integers present; simple integer comparison
		[ "$_v1" -lt "$_v2" ] && return 2
		[ "$_v1" -gt "$_v2" ] && return 1
	fi
)
