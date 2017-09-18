
import unittest

if __name__ == '__main__':

    print('\nRunning Graphh Test suite !!\n\n')

    verbosity = 2

    import test_shapes
    import test_io

    # Engage, captain Jean-Luc Picard !
    suite = unittest.TestLoader().loadTestsFromModule(test_shapes)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)

    suite = unittest.TestLoader().loadTestsFromModule(test_io)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)

    print('\n\nGraphh Test suite finished !!\n')

# Eof()
