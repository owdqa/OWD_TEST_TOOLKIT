from singleton import Singleton


class AssertionManager(object):

    __metaclass__ = Singleton

    def __init__(self):
        self._passed = 0
        self._failed = 0
        self._total = 0
        self._accum_passed = 0
        self._accum_failed = 0
        self._accum_total = 0

    def reset(self):
        self._passed = 0
        self._failed = 0
        self._total = 0
        self._accum_passed = 0
        self._accum_failed = 0
        self._accum_total = 0

    def reset_test(self):
        self._passed = 0
        self._failed = 0
        self._total = 0

    def get_passed(self):
        return self._passed

    def inc_passed(self):
        self._passed = self._passed + 1
        self.inc_accum_passed()

    def set_passed(self, value):
        self._passed = value

    def get_failed(self):
        return self._failed

    def inc_failed(self):
        self._failed = self._failed + 1
        self.inc_accum_failed()

    def set_failed(self, value):
        self._failed = value

    def get_total(self):
        return self._passed + self._failed

    def set_total(self, value):
        self._total = value

    def get_accum_passed(self):
        return self._accum_passed

    def set_accum_passed(self, value):
        self._accum_passed = value

    def get_accum_failed(self):
        return self._accum_failed

    def set_accum_failed(self, value):
        self._accum_failed = value

    def get_accum_total(self):
        return self._accum_passed + self._accum_failed

    def set_accum_total(self, value):
        self._accum_total = value

    def inc_accum_passed(self):
        self._accum_passed = self._accum_passed + 1

    def inc_accum_failed(self):
        self._accum_failed = self._accum_failed + 1

    passed = property(get_passed, set_passed)
    failed = property(get_failed, set_failed)
    total = property(get_total, set_total)
    accum_passed = property(get_accum_passed, set_accum_failed)
    accum_failed = property(get_accum_failed, set_accum_failed)
    accum_total = property(get_accum_total, set_accum_total)
