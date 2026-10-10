import sys
sys.path.insert(0, '..')
import game as G, bots as B
tot = 0; diff = 0; big = 0; north = 0
class Cnt(B.Strategic):
    def rot_dir(self, st, i, q=None):
        global tot, diff, big, north
        if q is None:
            tot += 1
            a = G.rot_value(st, i, 1, False, self.w_north); b = G.rot_value(st, i, -1, False, self.w_north)
            if abs(a - b) > 1e-9: diff += 1
            if abs(a - b) > 1.0: big += 1
            a0 = G.rot_value(st, i, 1, False, 0); b0 = G.rot_value(st, i, -1, False, 0)
            if (a > b) != (a0 > b0) and abs(a - b) > 1e-9: north += 1
        return B.Strategic.rot_dir(self, st, i, q)
for k in range(300): G.play(G.Config(2, first=0), [Cnt(k), Cnt(k + 1)], 900000 + k)
print("rotation phases %d; directions differ in value %.1f%%; differ by >1 point %.1f%%; North term flips the choice %.1f%%" % (tot, 100 * diff / tot, 100 * big / tot, 100 * north / tot))
