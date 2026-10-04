import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import statistics as S, collections
import game as g, bots as B
def mirror(label, n=2000, mk=lambda s: (B.Strategic(s), B.Strategic(s + 7919))):
    w = 0; lc = []; ends = collections.Counter(); el = eln = 0
    for i in range(n):
        r = g.play(mk(i), 50000 + i); w += r["winner"] == 0; ends[r["end"]] += 1
        h = r["st"].history; sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
        lc.append(sum(1 for a, b in zip(sg, sg[1:]) if a != b))
        if len(h) > 3 and h[2]: eln += 1; el += ((h[2] < 0) == (r["winner"] == 0))
    print("%-34s T%.3f lc %.2f early %.3f ends %s" % (label, w / n, S.mean(lc), el / max(1, eln), {k: round(v / n, 2) for k, v in ends.items()}))
mirror("baseline")
mirror("both lead-first (no last word)", mk=lambda s: (B.Strategic(s, last_word=False), B.Strategic(s + 1, last_word=False)))
mirror("T last-word, W lead", mk=lambda s: (B.Strategic(s, last_word=True), B.Strategic(s + 1, last_word=False)))
mirror("T lead, W last-word", mk=lambda s: (B.Strategic(s, last_word=False), B.Strategic(s + 1, last_word=True)))
g.KNOB["need"] = {3: 3}; mirror("no margin-2 rule at pos2")
g.KNOB["need"] = {2: 2, 3: 3}; g.KNOB["double_at"] = 4; mirror("double move at margin 4")
g.KNOB["need"] = {}; g.KNOB["double_at"] = 4; mirror("no margin rules + double at 4")
