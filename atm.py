import os
import pickle


NOTES_PATH = '_notes'


class PersistentDict(dict):

    def __init__(self, path):
        self._path = path
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                self.update(pickle.load(f))

    def sync(self):
        with open(self._path, 'w') as f:
            pickle.dump(dict(self), f)


class NotesStore(object):

    def __init__(self):
        self._notes = PersistentDict(NOTES_PATH)
        self.denomitations = self._mk_denomitations()

    def _mk_denomitations(self):
        return sorted(self._notes.keys(), reverse=True)

    def init(self, notes):
        """
        Initialize store with notes

        * notes - dict with note counts, indexed by note denomination
        """
        self._notes.clear()
        self._notes.update(notes)
        self._notes.sync()
        self.denomitations = self._mk_denomitations()

    def get_count(self, note):
        """Get count for provided note"""
        return self._notes[note]

    def inc_count(self, note, inc=1):
        """Increase note count"""
        self._notes[note] += inc

    def dec_count(self, note, dec=1):
        """Decrease note count"""
        self._notes[note] -= dec

    def get_notes(self):
        """Return dict with note counts"""
        return dict(self._notes)

    def sync(self):
        """Sync counts to file"""
        self._notes.sync()


class Atm(object):

    def __init__(self):
        self.notes = NotesStore()

    def _dispense(self, remaining, result, pos=0):
        if remaining == 0 and result:
            return True
        elif remaining > 0:
            curr_note = self.notes.denomitations[pos]
            if remaining >= curr_note and self.notes.get_count(curr_note) > 0:
                result.append(curr_note)
                self.notes.dec_count(curr_note)
                if self._dispense(remaining - curr_note, result, pos):
                    return result
                result.pop()
                self.notes.inc_count(curr_note)

            if pos + 1 < len(self.notes.denomitations):
                if self._dispense(remaining, result, pos + 1):
                    return result

    def dispense(self, amount):
        """Dispense money from ATM"""
        result = self._dispense(amount, [])
        self.notes.sync()
        return result
