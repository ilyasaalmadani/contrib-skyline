# contrib-skyline

> Transform your GitHub contribution graph into a stunning isometric skyline.  
> Novel, customizable, and ready for your profile README.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Stars](https://img.shields.io/github/stars/ilyasaalmadani/contrib-skyline?style=social)](https://github.com/ilyasaalmadani/contrib-skyline)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ilyasaalmadani/contrib-skyline/pulls)

<div align="center">

**Your code. Your city. Your skyline.**

[Examples](#examples) · [Quick Start](#quick-start) · [Themes](#themes) · [Contribute](#contributing)

</div>

---

## Why contrib-skyline?

Most contribution visualizations are flat grids or simple charts.  
**contrib-skyline** turns your activity into a living isometric city — each week a building, each contribution a lit window.

- **Novel isometric rendering** with customizable height curves
- **Multiple professional themes** (Neon, Dark, Ocean, and more)
- **Zero-dependency SVG output** perfect for READMEs
- **Sample data generator** so you can preview instantly
- **Designed for GitHub profiles** — drop in and impress

## Examples

### Neon Theme
![Neon Skyline](examples/skyline-neon.svg)

### Dark Theme (GitHub-native)
![Dark Skyline](examples/skyline-dark.svg)

### Ocean Theme
![Ocean Skyline](examples/skyline-ocean.svg)

## Quick Start

```bash
# Clone and generate samples
git clone https://github.com/ilyasaalmadani/contrib-skyline.git
cd contrib-skyline
python3 src/generate_skyline.py
```

The script generates three themed SVGs in `examples/`.

### Embed in your README

```markdown
![My Skyline](https://raw.githubusercontent.com/ilyasaalmadani/contrib-skyline/main/examples/skyline-neon.svg)
```

Or use the generated files from your own fork after connecting real data.

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| Isometric Skyline | ✅ | Week-based buildings with window density |
| Multiple Themes | ✅ | Neon, Dark, Ocean (more coming) |
| SVG Output | ✅ | Scalable, lightweight, GitHub-friendly |
| Sample Generator | ✅ | Realistic activity simulation |
| GitHub Action | 🚧 | Auto-update your skyline daily |
| Real Data Fetch | 🚧 | GraphQL integration planned |
| Custom Themes | 🚧 | User-defined color palettes |

## How It Works

1. Contribution data is grouped into weekly totals
2. Building height scales with activity (logarithmic for balance)
3. Windows are rendered proportional to daily intensity
4. Isometric projection creates the 3D skyline effect
5. Themes control colors, glow, and atmosphere

## Roadmap

- [ ] Real GitHub GraphQL data fetching
- [ ] GitHub Action for automatic daily updates
- [ ] More themes (Synthwave, Matrix, Sakura)
- [ ] Interactive web demo
- [ ] Stats overlay (streaks, total, busiest week)
- [ ] Multi-year comparison

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork the repo
2. Create a feature branch
3. Add your theme or improvement
4. Open a PR

## License

MIT © [Ilyas Akbar Almadani](https://github.com/ilyasaalmadani)

---

<div align="center">

**Built with care by a senior engineer who believes visualizations should make data beautiful.**

⭐ Star this repo if you like the skyline — it helps it grow taller.

</div>
