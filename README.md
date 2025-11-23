# Science Ops CLI

A terminal-based **Swiss army knife for scientists, engineers, students, and data nerds**.

Think of it as a tiny multi-discipline lab that lives in your shell:
- Physical constants at your fingertips
- Unit conversions with dimensional sanity
- Basic statistics and probability tools
- Waveform generation and ASCII plotting
- A lab notebook that logs your commands and results
- Science modules (astronomy, chemistry, mechanics, optics, electromagnetism, relativity, biology)
- Quick CSV/TSV exploration and histograms

This is designed to be **extensible**: new scientific domains can be added as `tools/` modules with their own subcommands.

---

## Features

### ✅ Constants
Search a curated set of physical constants with proper units and references.

```bash
ops constants list
ops constants get c
ops constants get "planck"
```

### ✅ Units

Convert between common units using a small dimensional-analysis engine.

```bash
ops units convert 5.2 m/s mph
ops units convert 1 atm Pa
ops units list-dimensions
```

### ✅ Stats

Quick descriptive statistics and normal distribution helpers.

```bash
ops stats describe 1 2 3 4 5 6
ops stats normal-pdf 0 --mu 0 --sigma 1
ops stats normal-cdf 1.96 --mu 0 --sigma 1
```

### ✅ Waves

Generate simple waveforms and display them as ASCII plots.

```bash
ops waves sine --freq 1.0 --samples 40
ops waves square --freq 2.0 --samples 40
```

### ✅ Lab Notebook

Append timestamped notes and results to a Markdown file.

```bash
ops notebook log "Measured resistance: 4.7 kΩ ± 0.1 kΩ"
ops notebook show
```

### ✅ Mechanics (`ops mech ...`)
- `ops mech projectile v0 angle` – range, time of flight, max height
- `ops mech work F d --angle θ` – mechanical work
- `ops mech pendulum L` – small-angle period
- `ops mech orbit-period a` – Keplerian orbital period
- Use `--body earth|moon|mars|jupiter|sun` to pull preset gravity/μ.

### 🔭 Astro (preview)

Astronomy helpers: local sidereal time and coordinate transforms.

```bash
ops astro lst --lon -122.3 --datetime "2024-06-01T10:00:00Z"
ops astro altaz --ra "10h12m45s" --dec "-12d30m00s" --lat 37.8 --lon -122.3 --datetime "2024-06-01T10:00:00Z"
```

### ⚗️ Chem (preview)

Common lab calculations: molarity and dilution.

```bash
ops chem molarity --moles 0.25 --volume-l 0.5
ops chem dilute --c1 2.0 --v1 10 --c2 0.5
```

### ✅ Relativity (`ops relativity ...`)
- `ops relativity gamma v`
- `ops relativity time-dilation Δτ v`
- `ops relativity energy m v`
- `ops relativity grav-dilation --body earth --altitude 0` (or custom mass/r)

### ✅ Biology (`ops bio ...`)
- `ops bio hardy-weinberg --aa --ab --bb`
- `ops bio punnett Aa aa`
- `ops bio gc-content SEQUENCE`
- `ops bio translate SEQUENCE`
- `ops bio find-orfs SEQUENCE --min-aa 50 --frames 1,2,3`

### ✅ Body presets
Use named bodies anywhere `--body` is supported:

```bash
ops mech projectile 20 45 --body moon
ops relativity grav-dilation --body jupiter --altitude 100000
```

Current presets: Earth, Venus, Moon, Mars, Jupiter, Saturn, Sun.

### 📈 Data (`ops data ...`)
- `ops data summarize file.csv` – stats for numeric columns
- `ops data head file.csv --rows N` – preview rows
- `ops data hist file.csv col --bins 10` – ASCII histogram

### 🔦 Optics (`ops optics ...`)
- `ops optics snell n1 n2 theta1` – refraction / total internal reflection
- `ops optics thin-lens f d_o` – image distance and magnification

### ⚡ Electromagnetism (`ops em ...`)
- `ops em coulomb q1 q2 r` – Coulomb force magnitude and interaction type
- `ops em reactance freq --L H --C F` – reactive impedance for inductors/capacitors

### ⚙️ Config (`ops config ...`)
- `ops config show` – view current config (notebook path, default body, color)
- `ops config set KEY VALUE` – change config values

### 🧭 Command index
- `ops help-all` – list all subcommands with their short descriptions

---

## Installation

From PyPI (recommended):

```bash
pip install -U science-ops-cli
```

Dev install from source:

```bash
git clone https://github.com/thatkidtk/science-ops-cli.git
cd science-ops-cli
pip install -e .
```

Either way you get a console script called `ops`.

---

## Usage

General help:

```
ops --help
ops constants --help
ops units --help
ops stats --help
ops waves --help
ops data --help
ops optics --help
ops em --help
ops config --help
ops help-all
ops notebook --help
ops astro --help
ops chem --help
ops mech --help
ops relativity --help
ops bio --help
```

Example:

```bash
# Convert 10 m/s to km/h
ops units convert 10 m/s km/h

# Look up Planck's constant
ops constants get planck

# Describe a dataset
ops stats describe 2.3 4.1 5.9 3.3 4.8

# Log an experiment step
ops notebook log "Ran titration trial 3, overshoot by ~0.2 mL"
```

---

## Project Structure

```
science_ops/
  cli.py        # Typer app entrypoint
  config.py     # Config handling (paths, defaults)
  tools/        # Individual scientific tool modules
  utils/        # Shared helpers (IO, math, display, etc.)
```

Each module under `tools/` exposes a `typer.Typer()` app that gets mounted under the main `ops` CLI.

---

## Roadmap

See `ROADMAP.md` for what’s next (Phase 2/3) or open issues for ideas and bugs.

---

## Contributing
1. Add a new module under `science_ops/tools/yourtool.py`
2. Make a `typer.Typer()` instance in that file
3. Mount it in `cli.py` via `app.add_typer(...)`
4. Add tests in `tests/`
5. Open a PR

---

## License

MIT, because science should spread.
