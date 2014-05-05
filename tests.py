import tempfile
import shutil
from unittest import TestCase, main

from mock import patch, Mock

import atm
import cli


class BaseTestCase(TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.patcher = patch.multiple(
            '__main__.atm', NOTES_PATH='{}/db'.format(self.tmpdir))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop
        shutil.rmtree(self.tmpdir)


class NoteStoreTests(BaseTestCase):

    def test_init(self):
        notes = atm.NotesStore()
        data = {20: 3, 50: 2}
        notes.init(data)
        self.assertEqual(notes.get_notes(), data)

    def test_init_persistance(self):
        notes = atm.NotesStore()
        data = {20: 3, 50: 2}
        notes.init(data)
        notes = atm.NotesStore()
        self.assertEqual(notes.get_notes(), data)

    def test_get_count(self):
        notes = atm.NotesStore()
        notes.init({20: 3, 50: 2})
        self.assertEqual(notes.get_count(20), 3)

    def test_dec_count(self):
        notes = atm.NotesStore()
        notes.init({20: 3, 50: 2})
        notes.dec_count(20)
        self.assertEqual(notes.get_count(20), 2)

    def test_inc_count(self):
        notes = atm.NotesStore()
        notes.init({20: 3, 50: 2})
        notes.inc_count(50)
        self.assertEqual(notes.get_count(50), 3)


class AtmTests(BaseTestCase):

    def test_dispense(self):
        a = atm.Atm()
        a.notes.init({20: 3, 50: 3})

        self.assertEqual(a.dispense(100), [50, 50])
        self.assertEqual(a.notes.get_notes(), {20: 3, 50: 1})

    def test_dispense_persistance(self):
        a = atm.Atm()
        a.notes.init({20: 3, 50: 2})
        a.dispense(100)

        a = atm.Atm()
        self.assertEqual(a.notes.get_notes(), {20: 3, 50: 0})

    def test_dispense_does_not_exists(self):
        a = atm.Atm()
        a.notes.init({20: 5, 50: 5})

        self.assertEqual(a.dispense(111), None)
        self.assertEqual(a.notes.get_notes(), {20: 5, 50: 5})

    def test_dispense_no_notes(self):
        a = atm.Atm()
        a.notes.init({20: 3, 50: 1})

        self.assertEqual(a.dispense(110), [50, 20, 20, 20])
        self.assertEqual(a.notes.get_notes(), {20: 0, 50: 0})

        self.assertEqual(a.dispense(100), None)


class TestCLI(TestCase):

    def setUp(self):
        self.patcher = patch('cli.Atm')
        mock = self.patcher.start()
        self.atm_mock = mock.return_value = Mock()

    def tearDown(self):
        self.patcher.stop()

    def test_init(self):
        cmd = cli.InitCommand()
        cmd.handle(['50=1,30=2'])
        self.atm_mock.notes.init.assert_called_once_with({50: 1, 30: 2})

    @patch('__builtin__.print')
    def test_status(self, print_mock):
        self.atm_mock.notes.get_notes.return_value = {20: 10}
        cmd = cli.StatusCommand()
        cmd.handle([])
        self.atm_mock.notes.get_notes.assert_called_once_with()
        print_mock.assert_called_once_with('$20: 10')

    @patch('__builtin__.print')
    def test_dispense(self, print_mock):
        self.atm_mock.dispense.return_value = [5, 5]
        cmd = cli.DispenseCommand()
        cmd.handle(["10"])
        self.atm_mock.dispense.assert_called_once_with(10)
        print_mock.assert_called_once_with(
            'Dispensed successfully in following notes: $5, $5')

if __name__ == '__main__':
    main()
