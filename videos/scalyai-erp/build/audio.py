# Plan de tiempos + música + efectos para la promo de Scaly AI. Ejecutar desde la carpeta del proyecto.
import json, os, re, subprocess, wave
import numpy as np
SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "audio")
SCENES = [["s1"], ["s2"], ["s3"], ["s4"], ["s5"], ["s6"]]
LEAD = [0.6, 1.0, 1.0, 1.0, 1.0, 1.5]  # silencio antes de la voz en cada escena (deja ver la transición/entrada)
IN_GAP = 0.7
TAIL = 3.0
POST = [0.7, 0.9, 0.9, 0.9, 0.9, 0.15]  # silencio tras la voz de cada escena

def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True)
def dur(p): return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).stdout)
def speech(p, d):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "silencedetect=n=-35dB:d=0.22", "-f", "null", "-"], capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    out, cur = [], 0.0
    for a, b in zip(ss, se + [d] * (len(ss) - len(se))):
        if a - cur > 0.05: out.append([round(cur, 3), round(a, 3)])
        cur = b
    if d - cur > 0.05: out.append([round(cur, 3), round(d, 3)])
    return out

segs = {s["id"]: s for s in json.load(open(os.path.join(A, "segmentos.json")))}
t, scene_start, order = 0.0, [], []
for si, ids in enumerate(SCENES):
    scene_start.append(round(t, 3)); t += LEAD[si]
    for k_, i in enumerate(ids):
        if k_: t += IN_GAP
        p = os.path.join(A, "seg", i + ".wav"); d = dur(p)
        s = segs[i]; s["start"], s["dur"], s["speech"], s["scene"] = round(t, 3), round(d, 3), speech(p, d), si
        order.append(s); t += d
    t += POST[si]
T = round(t + TAIL, 2)
json.dump(order, open(os.path.join(A, "segmentos.json"), "w"), ensure_ascii=False, indent=1)
plan = {"S": scene_start, "V": {s["id"]: s["start"] for s in order}, "D": {s["id"]: s["dur"] for s in order}, "T": T}
json.dump(plan, open(os.path.join(ROOT, "build", "plan.json"), "w"), indent=1)
print("T", T, "scenes", scene_start)
if os.environ.get("PLAN_ONLY"): raise SystemExit

N = int(T * SR)
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(d * SR)) / SR
def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i < 0: return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += g * x
def smooth(x, k): return np.convolve(x, np.ones(k) / k, mode="same")
def env(d, a=0.01, r=None):
    x = tt(d); r = r or d * 0.6
    return np.minimum(1, x / a) * np.exp(-x / r * 3)
def pluck(f, d=0.9):
    x = tt(d); return np.exp(-x * 6) * (1 - np.exp(-x * 400)) * (np.sin(2 * np.pi * f * x) + 0.25 * np.sin(4 * np.pi * f * x) + 0.08 * np.sin(6 * np.pi * f * x))
def pad(fs, d, amp):
    x = tt(d); y = sum(np.sin(2 * np.pi * f * x) + 0.5 * np.sin(2 * np.pi * f * 1.003 * x) + 0.3 * np.sin(2 * np.pi * f * 0.997 * x) for f in fs)
    return amp * y * np.minimum(1, x / 0.8) * np.minimum(1, (d - x) / 0.8)
def sub(f, d):
    x = tt(d); return np.sin(2 * np.pi * f * x) * np.minimum(1, x / 0.02) * np.exp(-x * 2.2)
def kick():
    x = tt(0.35); return np.sin(2 * np.pi * (42 + 70 * np.exp(-x * 35)) * x) * np.exp(-x * 9)
def hat(d=0.05):
    return smooth(rng.uniform(-1, 1, int(d * SR)), 2) * np.exp(-tt(d) * 80)
def clap():
    return smooth(rng.uniform(-1, 1, int(0.18 * SR)), 3) * np.exp(-tt(0.18) * 28)

S = scene_start
# Lecho tranquilo y moderno: Fmaj9 – Am7 – Dm9 – Bbmaj7, 96 bpm. Noche (A): solo pad grave.
# Desde el problema (B): arpegio suave. Desde la marca (C): bombo, palmas y bajo. Cierre (H): se abre y descansa.
beat = 60 / 96; bar = 4 * beat
prog = [[87.31, 174.61, 220.0, 261.63, 392.0], [110.0, 164.81, 220.0, 261.63, 392.0], [73.42, 174.61, 220.0, 261.63, 329.63], [58.27, 174.61, 233.08, 293.66, 349.23]]
mus = np.zeros(N)
for b in range(int(T / bar) + 1):
    t0 = b * bar; ch = prog[b % 4]
    full = t0 >= S[1] - 0.05 and t0 < T - 2.5
    arp = t0 >= S[1] - bar * 0.5
    add(mus, pad(ch[1:], bar + 0.8, 0.022 if full else 0.03), t0)
    add(mus, sub(ch[0], bar), t0, 0.16 if full else 0.08)
    if arp:
        pat = [1, 3, 2, 4, 3, 2, 4, 3]
        for e in range(8):
            add(mus, pluck(ch[pat[e]] * 2, 0.7), t0 + e * beat / 2, 0.045 if e % 2 == 0 else 0.03)
    if full:
        for q in range(4):
            add(mus, kick(), t0 + q * beat, 0.32 if q in (0, 2) else 0.0)
            add(mus, hat(), t0 + q * beat + beat / 2, 0.03)
            if q in (1, 3): add(mus, clap(), t0 + q * beat, 0.05)
fi = int(2.0 * SR); mus[:fi] *= np.linspace(0, 1, fi)
fo = int(3.5 * SR); mus[-fo:] *= np.linspace(1, 0, fo) ** 1.5

fx = np.zeros(N)
def whoosh(d=0.9):
    x = tt(d); n = smooth(rng.uniform(-1, 1, len(x)), 10)
    return n * np.sin(np.pi * x / d) ** 2 * 2.2
def swish(d=0.5):
    x = tt(d); n = smooth(rng.uniform(-1, 1, len(x)), 22)
    return n * np.sin(np.pi * x / d) ** 3 * 2.0
def tick():
    x = tt(0.06); return np.sin(2 * np.pi * 1600 * x) * np.exp(-x * 90)
def ping():
    x = tt(0.9); return (np.sin(2 * np.pi * 1318.5 * x) + 0.6 * np.sin(2 * np.pi * 1760 * x) * (x > 0.09)) * np.exp(-x * 6)
def chime(b=880):
    x = tt(2.2); return sum(a * np.sin(2 * np.pi * b * m * x) for a, m in ((1, 1), (0.45, 1.5), (0.2, 2), (0.1, 3))) * np.exp(-x * 2.2)
ev = json.load(open(os.path.join(ROOT, "build", "events.json"))) if os.path.exists(os.path.join(ROOT, "build", "events.json")) else []
SND = {"whoosh": (whoosh, 0.45), "swish": (swish, 0.35), "tick": (tick, 0.22), "ping": (ping, 0.22), "chime": (lambda: chime(), 0.2), "chime2": (lambda: chime(1046.5), 0.18)}
for kind, at in ev:
    f, g = SND[kind]; add(fx, f(), at, g)

def save(path, x, peak):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    st = np.repeat((x * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
save(os.path.join(A, "musica-raw.wav"), mus, 0.6)
sh("ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(A, "musica-raw.wav"), "-af", "loudnorm=I=-24:TP=-3:LRA=9", "-ar", "44100", os.path.join(A, "musica.wav"))
os.remove(os.path.join(A, "musica-raw.wav"))
save(os.path.join(A, "efectos.wav"), fx, 0.7)
sh("python3", os.path.join(A, "ducking.py"), os.path.join(A, "musica.wav"), os.path.join(A, "musica-duck.wav"), os.path.join(A, "segmentos.json"), os.path.join(A, "seg"))
print("audio ok")
