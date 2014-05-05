import tempfile
import shutil
from unittest import TestCase, main

import atm


class BaseTestCase(TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._notes_path_orig = atm.NOTES_PATH
        atm.NOTES_PATH = '{}/db'.format(self.tmpdir)

    def tearDown(self):
        atm.NOTES_PATH = self._notes_path_orig
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

if __name__ == '__main__':
    main()
