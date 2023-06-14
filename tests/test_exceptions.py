import unittest
from ._compat import patch

from telegram_upload.exceptions import dxdmgchUploadError, catch


class TestdxdmgchUploadError(unittest.TestCase):
    def test_exception(self):
        self.assertEqual(str(dxdmgchUploadError()), 'dxdmgchUploadError')

    def test_body(self):
        error = dxdmgchUploadError()
        error.body = 'body'
        self.assertEqual(str(error), 'dxdmgchUploadError: body')

    def test_extra_body(self):
        self.assertEqual(str(dxdmgchUploadError('extra_body')), 'dxdmgchUploadError: extra_body')

    def test_all(self):
        error = dxdmgchUploadError('extra_body')
        error.body = 'body'
        self.assertEqual(str(error), 'dxdmgchUploadError: body. extra_body')


class TestCatch(unittest.TestCase):
    def test_call(self):
        self.assertEqual(catch(lambda: 'foo')(), 'foo')

    @patch('telegram_upload.exceptions.sys.stderr.write')
    def test_raise(self, m):
        def raise_error():
            raise dxdmgchUploadError('Error')
        with self.assertRaises(SystemExit):
            catch(raise_error)()
        m.assert_called_once()
