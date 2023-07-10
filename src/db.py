class SetsInMemoryDb:

    def __init__(self):
        self.storage = {}

    def add_sets(self, sets):
        for s in sets:
            self.storage[s.id] = s

    @staticmethod
    def apply_filter(s, upset_filter):
        fulfills_min_upset_factor = s.upset_factor >= upset_filter.get('min_upset_factor', -float('inf'))
        fulfills_not_dq = not s.is_dq()
        return all([
            fulfills_min_upset_factor,
            fulfills_not_dq,
        ])

    def get_upset_thread(self, upset_filter=None):
        if upset_filter is None:
            upset_filter = {}
        thread = {
            'winners': [],
            'losers': [],
            'notables': [],
            'dqs': [],
            'other': [],
        }

        for s in self.storage.values():
            if s.is_winners_bracket() and self.apply_filter(s, upset_filter):
                thread['winners'].append(s)
            elif not s.is_winners_bracket() and self.apply_filter(s, upset_filter):
                thread['losers'].append(s)
            elif s.is_dq_and_out():
                thread['dqs'].append(s)
            else:
                thread['other'].append(s)

        return thread
