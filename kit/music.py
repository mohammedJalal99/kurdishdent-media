"""Original royalty-free background music generator (no samples). make(dur, seed, path)."""
import numpy as np, wave

SR = 48000
PROGS = [  # (chords as MIDI notes, bass roots)
    ([[62, 66, 69, 73], [57, 61, 64, 69], [59, 62, 66, 69], [55, 59, 62, 66]], [38, 33, 35, 31]),   # D A Bm G
    ([[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]], [36, 33, 29, 31]),   # Cmaj7 Am F G
    ([[65, 69, 72, 76], [62, 65, 69, 72], [58, 62, 65, 69], [60, 64, 67, 70]], [41, 38, 34, 36]),   # F Dm Bb C
    ([[57, 60, 64, 67], [53, 57, 60, 64], [60, 64, 67, 71], [55, 59, 62, 67]], [33, 29, 36, 31]),   # Am F C G
]
MELS = [[78, 76, 74, 73, 74, 76, 78, 81, 76, 73, 71, 73, 76, 73, 69, 71],
        [76, 79, 81, 79, 76, 74, 72, 74, 76, 74, 72, 69, 72, 74, 76, 79],
        [81, 79, 77, 76, 77, 79, 81, 84, 79, 77, 76, 74, 77, 76, 72, 74],
        [76, 72, 74, 76, 79, 76, 74, 72, 71, 72, 74, 76, 74, 72, 69, 71]]


def make(dur, seed, path):
    rng = np.random.default_rng(seed)
    prog, roots = PROGS[seed % len(PROGS)]
    mel = MELS[(seed // len(PROGS)) % len(MELS)]
    bpm = [100, 104, 96, 110][(seed // 2) % 4]
    beat = 60 / bpm
    N = int(SR * (dur + 0.05)); L = np.zeros(N); R = np.zeros(N)

    def add(buf, sig, t, g=1.0):
        i = int(t * SR); j = min(N, i + len(sig))
        if 0 <= i < N: buf[i:j] += sig[:j - i] * g

    def both(sig, t, g=1.0, d=0.0): add(L, sig, t, g); add(R, sig, t + d, g)

    def env(n, a=0.005, d=0.4):
        t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)

    def epiano(f, d_, v):
        n = int(SR * d_); t = np.arange(n) / SR
        mod = np.sin(2 * np.pi * f * 2 * t) * 1.2 * np.exp(-t / 0.3)
        return (np.sin(2 * np.pi * f * t + mod) + 0.3 * np.sin(4 * np.pi * f * t)) * env(n, 0.004, 0.9) * v

    def pluck(f, d_=0.35, v=0.25):
        n = int(SR * d_); t = np.arange(n) / SR
        return (np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + np.sin(2 * np.pi * f * t)) * env(n, 0.002, 0.12) * v

    def kick():
        n = int(SR * 0.35); t = np.arange(n) / SR; f = 50 + 90 * np.exp(-t / 0.04)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12) * 0.9

    def hat(op=False):
        n = int(SR * (0.12 if op else 0.04)); x = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
        return x * np.exp(-np.arange(n) / SR / (0.04 if op else 0.012)) * 0.12

    def clap():
        n = int(SR * 0.2); x = rng.standard_normal(n); e = np.exp(-np.arange(n) / SR / 0.06)
        for k in (0.0, 0.012, 0.024):
            s = int(k * SR); e[s:] += 0.6 * np.exp(-np.arange(n - s) / SR / 0.01)
        return x * e * 0.18

    def bass(f, d_):
        n = int(SR * d_); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)) * env(n, 0.005, 0.5) * 0.45

    nt = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = 4 * beat; t = 0.0; b = 0
    while t < dur:
        for m in prog[b % 4]: both(epiano(nt(m), bar * 0.95, 0.11), t, 1.0, 0.006)
        both(bass(nt(roots[b % 4]), bar * 0.5), t); both(bass(nt(roots[b % 4]), bar * 0.45), t + 2 * beat)
        for k in range(4):
            bt = t + k * beat
            if b >= 1 or k >= 2:
                if k in (0, 2): both(kick(), bt)
                if k in (1, 3): both(clap(), bt)
            for h in range(2): both(hat(h == 1 and k == 3), bt + h * beat / 2, 0.9, 0.003)
        if b >= 1:
            for k in range(8):
                if (b * 8 + k) % 3 != 2: both(pluck(nt(mel[(b * 8 + k) % 16])), t + k * beat / 2, 0.75, 0.01)
        t += bar; b += 1

    def verb(x):
        y = x.copy()
        for dly, g in [(0.029, 0.35), (0.037, 0.3), (0.041, 0.28), (0.053, 0.22)]:
            d = int(dly * SR); z = np.zeros_like(x)
            for r in range(6):
                s = d * (r + 1)
                if s < len(x): z[s:] += x[:-s] * (g ** (r + 1))
            y += z * 0.5
        return y

    st = np.stack([verb(L), verb(R)], 1); st /= np.max(np.abs(st)) * 1.25
    tail = int(1.0 * SR); st[-tail:] *= np.linspace(1, 0, tail)[:, None]
    w = wave.open(path, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
