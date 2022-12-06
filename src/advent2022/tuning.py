"""Tuning module.

Subroutine to detect start-of-packet markers.
"""

from collections import namedtuple

def datastream(lines):
    """Returns a datastream from a lines"""
    all_lines = list(lines)
    assert len(all_lines) == 1, f"Expecting 1 line, got {len(all_lines)}"
    return all_lines[0]


def all_different(stream):
    return len(stream) == len(set(stream))


class Chunk(namedtuple('Chunk', 'raw start')):

    @property
    def end(self):
        return self.start + len(self.raw)

    @property
    def all_different(self):
        return all_different(self.raw)

    def __len__(self):
        return len(self.raw)

    def __repr__(self):
        return f'Chunk("{self.raw}", [{self.start}:{self.end}])'



def chunks(stream, length=4):
    total_length = len(stream)
    assert length <= total_length, (
        f"Can't create chunks of length {length} from stream of length {total_length}"
    )
    cks = []
    for i in range(total_length - length + 1):
        cks.append(Chunk(stream[i:i+length], i))
    return cks

def first_different_chunk(cks):
    for ck in cks:
        if ck.all_different:
            return ck
    return None

def start_of_packet(lines):
    stream = datastream(lines)
    cks = chunks(stream)
    packet_start = first_different_chunk(cks)
    return packet_start.end

def start_of_marker(lines):
    stream = datastream(lines)
    cks = chunks(stream, length=14)
    marker_start = first_different_chunk(cks)
    return marker_start.end
