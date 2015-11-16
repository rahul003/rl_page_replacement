#!/usr/bin/env python

import argparse
import random

class FrameTable(object):
    """Abstract base class implementing some behaviour for a frame table. 
    Will be made Master
    """

    def __init__(self, size):
        """Create a frame table.
        Arguments:
        size -- The number of frames to keep track of.
        output -- The output object to keep track of the frame contents for
        printing.
        """
        self.frames = [None for x in xrange(size)]
        self.faults = 0
        # self.output = output
        self.time = 0

        #for fifo
        self.insert_times = [None for x in xrange(size)]

        #for LRU
        self.access_times = {} 


    def access(self, page):
        """Attempt to access a given page."""
        if page not in self.frames:
            self.insert(page)

        # self.output.append(self.frames, page)
    def insert_time(self, frame):
        self.insert_times[frame] = self.time
        self.time +=1


    def insert(self, page):
        """Insert a page into the frame table."""
        self.faults += 1
        try:
            empty_frame = self.frames.index(None)
            self.frames[empty_frame] = page
            insert_time(empty_frame)
        except ValueError:
            frame = self.eject()
            self.frames[frame] = page
            insert_time(frame)

    def eject(self):
        """Eject a frame from the frame table according to an algorithm."""
        # override
        pass

    def dump(self):
        """Print the access table."""
        print self.faults
        # self.output.output(self.faults)


class Rand(FrameTable):
    """Frame table implementation which randomly ejects pages when there is a
    page fault."""

    def eject(self):
        return random.randint(0, len(self.frames) - 1)


class FIFO(FrameTable):
    """Frame table implementation which ejects pages according to the order in
    which they were inserted."""

    def eject(self):
        
        return (self.faults - 1) % len(self.frames)


class LRU(FrameTable):
    """Frame table implementation which ejects pages which have been the
    least recently used."""

    def __init__(self, size):
        FrameTable.__init__(self, size)
        self.time = 0

    def access(self, page):
        self.time += 1
        self.access_times[page] = self.time
        FrameTable.access(self, page)

    def eject(self):
        ejected_page = min(self.access_times, key=self.access_times.get)
        del self.access_times[ejected_page]
        return self.frames.index(ejected_page)


class Clock(FrameTable):
    """Frame table implementation which ejects pages according to the clock
    algorithm."""

    def __init__(self, size):
        FrameTable.__init__(self, size)
        self.clock = 0
        self.reference_bits = dict((key, 0) for key in self.frames)

    def access(self, page):
        self.reference_bits[page] = 1
        FrameTable.access(self, page)

    def eject(self):
        while self.reference_bits[self.frames[self.clock]] == 1:
            self.reference_bits[self.frames[self.clock]] = 0
            self.clock = (self.clock + 1) % len(self.frames)

        del self.reference_bits[self.frames[self.clock]]
        return self.clock


class Optimal(FrameTable):
    """Frame table implementation which looks into the future in order to
    implement the optimal page replacement algorithm."""

    def __init__(self, size):
        FrameTable.__init__(self, size)
        self.pages = []
        self.page = 0

    def access(self, page):
        self.pages.append(page)
        
    def eject(self):
        maximum = 0
        ejected_page = '0'
        for frame in self.frames:
            try:
                if self.pages[self.page:].index(frame) > maximum:
                    ejected_page = frame
                    maximum = self.pages.index(frame)
            except ValueError:
                return (self.faults - 1) % len(self.frames)

        print('Ejecting: ' + ejected_page + ' which was ' + str(maximum) + 'away from the page at page no ' + str(self.page))
        return self.frames.index(ejected_page)

    def _run(self):
        for page in self.pages:
            if page not in self.frames:
                self.insert(page)
            # self.output.append(self.frames, page)
            self.page += 1

    def dump(self):
        self._run()
        FrameTable.dump(self)


class NFU(FrameTable):
    """Frame table implementation which ejects pages according to the not
    frequently used algorithm."""

    def __init__(self, size):
        FrameTable.__init__(self, size)
        self.accesses = {}

    def access(self, page):
        FrameTable.access(self, page)

        if page in self.accesses:
            self.accesses[page] += 1
        else:
            self.accesses[page] = 1

    def eject(self):
        ejected_page = min(self.accesses, key=self.accesses.get)
        del self.accesses[ejected_page]
        return self.frames.index(ejected_page)


class Output(object):
    """Keeps track of the frame state after each page access in order to
    print a pretty table."""

    def __init__(self, frames, algorithm, filename):
        self.info = 'frames: ' + str(frames) + ', algorithm: ' + algorithm + ', filename: ' + filename
        self.heading = []
        self.table = [[] for x in xrange(frames)]

    def append(self, frames, page):
        self.heading.append(page)

        for i, f in enumerate(frames):
            if str(f) == self._get_previous(self.table[i]):
                self.table[i].append('=')
            else:
                self.table[i].append(str(f))

    def output(self, faults):
        # Print run info
        print(self.info)

        # Print table heading
        heading = 'ref : ' + ' : '.join(self.heading)
        print(heading)

        # Print table separator
        print(''.join(['=' for c in heading]))

        # Print table rows
        for row in self.table:
            print('    : ' + ' : '.join(row))

        # Print no. of page faults
        print('page faults: ' + str(faults))

    def _get_previous(self, row):
        if len(row) == 0:
            return '='
        if row[-1] != '=':
            return row[-1]
        else:
            return self._get_previous(row[:-1])


if __name__ == '__main__':
    algorithms = {
        '0': {'name': 'RANDOM', 'impl': Rand},
        '1': {'name': 'FIFO', 'impl': FIFO},
        '2': {'name': 'LRU', 'impl': LRU},
        '3': {'name': 'CLOCK', 'impl': Clock},
        '4': {'name': 'OPTIMAL', 'impl': Optimal},
        '5': {'name': 'NFU', 'impl': NFU},
    }

    random.seed()

    parser = argparse.ArgumentParser(description='Simulates a number of different virtual memory page replacement algorithms.')
    parser.add_argument('frames', type=int, help='The number of frames to simulate.')
    # parser.add_argument('algorithm', help='The paging algorithm to use. <0: Random> <1: FIFO> <2: LRU> <3: Clock> <4: Optimal> <5: Custom>')
    parser.add_argument('source', help='File containing a string of integers representing pages to be accessed.')

    args = parser.parse_args()

    
    for k in algorithms.keys():
    # out = Output(args.frames, algorithms[args.algorithm]['name'], args.source)
        frame_table = algorithms[k]['impl'](args.frames)

        with open(args.source) as f:
            # count = 0
            for line in f:
                if line.strip():
                    # count+=1
                    # if not count%100:
                        # print count, line.strip()
                    frame_table.access(line.strip())
        print algorithms[k]['name']
        frame_table.dump()