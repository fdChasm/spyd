def assertThrowsDeferred(test_suite, deferred, exception_class=None):
    errs, calls = [], []
    deferred.addCallbacks(calls.append, errs.append)
    test_suite.assertEqual(len(calls), 0, "Expected no callbacks, got {}".format(len(calls)))
    test_suite.assertEqual(len(errs), 1, "Expected exactly one errback, got {}".format(len(errs)))
    test_suite.assertRaises(exception_class or Exception, errs[0].raiseException)
