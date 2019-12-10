"""
Example unit tests.
"""
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path

import pydiner
from . import fixtures


def test_batcher(nseq=100, nbatch=23, joined=list):
    seq = joined(range(nseq))
    subseqs = [seq[i : i + nbatch] for i in range(0, nseq, nbatch)]
    batches = pydiner.batcher(seq, nbatch, joined=joined)

    assert joined(batches) == subseqs, "value mismatch"


def test_clockstr(maxerr=timedelta(seconds=1)):
    now = datetime.utcnow()
    stamped = datetime.fromisoformat(pydiner.clockstr())

    assert abs(stamped - now) < maxerr, f"timestamps off by more than {maxerr}"


def test_distinct(n=1000, seq="spam", joined="".join):
    seq = joined(seq)
    vals = pydiner.distinct(n * seq)

    assert joined(vals) == seq, "value mismatch"


def test_fullpath():
    absolute = "/spam"
    relative = "spam/eggs.txt"

    assert pydiner.fullpath(absolute) == Path(absolute), "bad absolute path"
    assert pydiner.fullpath(relative) == Path.cwd() / relative, "bad relative path"


@fixtures.cleartmp
def test_iterlines():
    folder = fixtures.TMPDIR

    lines = [f"{i} spam\n" for i in range(10)]
    paths = [folder / f"spam{i}.txt" for i in range(3)]
    for path in paths:
        with open(path, "w") as f:
            f.writelines(lines)

    lines = len(paths) * lines
    output = pydiner.iterlines(*paths)

    assert list(output) == lines, "value mismatch"


def test_loggers():
    inputs = ["How about a nice game of", __file__, "?"]
    outstr = " ".join(str(x) for x in inputs) + "\n"

    for meth in (pydiner.achtung, pydiner.echo):
        with StringIO() as stream:
            meth(*inputs, file=stream)
            assert stream.getvalue().endswith(outstr), "value mismatch"
