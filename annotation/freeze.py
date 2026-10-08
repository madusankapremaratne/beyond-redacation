"""Write annotation/freeze_manifest.json: the Phase 0 freeze record.

Records the frozen sample, the cluster-level development/test split, model digests, library
versions, seeds, the attacker prompt, and SHA-256 of every file the labels or results depend on.
Re-run only to *verify* (it refuses to overwrite a manifest whose hashes differ unless --force).
"""
import hashlib, json, random, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evaluation")); sys.path.insert(0, str(ROOT))
import pilot_reconstruction as pr  # noqa: E402

PK = ROOT / "annotation" / "packets"
OUTF = ROOT / "annotation" / "freeze_manifest.json"
SPLIT_SEED, N_CAL, N_DEV = 5, 5, 10


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def digests():
    tags = json.load(urllib.request.urlopen("http://localhost:11434/api/tags"))["models"]
    return {m["name"]: {"digest": m["digest"], "size": m["size"], "modified_at": m["modified_at"]}
            for m in tags if m["name"] in (pr.DEFENSE_MODEL, pr.ATTACK_MODEL)}


def main(force=False):
    groups = json.loads((PK / "groups.json").read_text())
    ids = list(range(len(groups)))
    random.Random(SPLIT_SEED).shuffle(ids)
    split = {"calibration": sorted(ids[:N_CAL]), "development": sorted(ids[N_CAL:N_CAL + N_DEV]),
             "test": sorted(ids[N_CAL + N_DEV:])}
    split["unit"] = "group (one custodian); resample groups, never messages"
    import spacy, en_core_web_sm
    files = [PK / "groups.json", PK / "documents.md", PK / "packet_A.csv", PK / "packet_B.csv", PK / "packet_C.csv",
             ROOT / "annotation/HOWTO.md",
             ROOT / "annotation/GUIDELINES.md", ROOT / "annotation/make_packets.py",
             ROOT / "annotation/agreement.py", ROOT / "evaluation/pilot_reconstruction.py",
             ROOT / "framework/extraction.py", ROOT / "framework/generalization.py",
             ROOT / "data/enron_mail.tar.gz"]
    m = {"frozen_on": "2026-10-08",
         "split": split, "split_seed": SPLIT_SEED, "sample_seed": 11,
         "attacker": {"model": pr.ATTACK_MODEL, "temperature": 0.0, "seed": 7, "num_predict": 700,
                      "repeat_penalty": 1.1, "prompt_sha256": hashlib.sha256(pr.ATTACK_PROMPT.encode()).hexdigest()},
         "defense_model": pr.DEFENSE_MODEL,
         "ollama_models": digests(),
         "ollama_version": subprocess.run(["ollama", "--version"], capture_output=True, text=True).stdout.strip(),
         "spacy": spacy.__version__, "en_core_web_sm": en_core_web_sm.__version__,
         "python": sys.version.split()[0],
         "files_sha256": {str(f.relative_to(ROOT)): sha(f) for f in files}}
    if OUTF.exists() and not force:
        old = json.loads(OUTF.read_text())
        if old != m:
            sys.exit("manifest differs from the frozen one; refusing to overwrite (use --force)")
        print("manifest verified: unchanged")
        return
    OUTF.write_text(json.dumps(m, indent=1))
    print("wrote", OUTF)
    print({k: len(v) for k, v in split.items() if isinstance(v, list)})


if __name__ == "__main__":
    main("--force" in sys.argv)
