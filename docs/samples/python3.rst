.. _samples_python3:

Python3 Samples
===============

Basic Py3 Skeleton
------------------

.. code-block:: python

    #!/usr/bin/env python3
    '''
    Some imaginary description
    '''
    import sys

    # A hacky but simple way of loading py3helpers
    sys.path.append('/path/to/lib')  # do not include 'py3helpers.py'
    import py3helpers


    def main():
        '''
        Main processing logic
        '''
	for list_item in sys.argv[1:]:
	    log = py3helpers.get_logger()
	    log.info(py3helpers.collapse_integers(list_item))


    if __name__ == '__main__':
        main()
