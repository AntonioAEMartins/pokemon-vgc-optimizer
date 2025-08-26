### Title
Pokemon VGC Optimizer

### Goal
Primary objective: predict the match winner from two six-Pokémon teams using tournament-style logs from Pokémon Showdown (Regulation E). The dataset `data/output/matches.csv` contains ~14k battles (13 columns: `winner` ∈ {1,2} and 12 team slots: `pokemon1_p1`…`pokemon6_p2`). An auxiliary list of allowed Pokémon (`data/output/pokemon_regE.txt`) is produced by the scraper.

Core libraries and tooling: TensorFlow/Keras, scikit-learn, pandas, BeautifulSoup (bs4), Selenium (Windows), and PyGAD (genetic optimization).

Training techniques used (from `02_pre_processing.ipynb`):
- Data splits: `train_test_split` (80/20, `random_state=42`) and `StratifiedShuffleSplit` (stratified on `winner`) to build `model` and `model_stratified`.
- Vocabulary/encoding: build vocabulary from all 12 team columns (~392 tokens). `keras.layers.StringLookup(vocabulary=..., mask_token=None)` maps names→indices; inverse `StringLookup(..., invert=True)` decodes indices→names.
- Architecture: `judge` is `keras.Sequential([StringLookup → Embedding(input_dim=len(vocabulary)+1, output_dim=256, input_length=6) → GlobalAveragePooling1D → Dense(16, relu, kernel_regularizer=l2(0.001)) → Dropout(0.1) → Dense(1)])`. Two inputs `t1`,`t2` (`dtype='string'`) pass through `judge` to `s1`,`s2`, then combined via `keras.layers.Subtract()` to yield the match logit.
- Training: `optimizer="adam"`, `loss=BinaryCrossentropy(from_logits=True)`, `metrics=['accuracy']`, `epochs=100`, `batch_size=64`, `validation_split=0.2`. Test accuracy: stratified ≈ 0.599 vs non‑stratified ≈ 0.559.
- GA usage: `pygad` treats the trained `judge` as a fitness function; gene space from `vocabulary`, individuals are 6‑token teams; `lookup_layer`/inverse handle encode/decode.

### Project Structure
- `01_web_scraper.ipynb` — scrape allowed Pokémon from `data/input/links.txt` → `data/output/pokemon_regE.txt`.
- `02_pre_processing.ipynb` — load `matches.csv`, encode teams, split data, and train a baseline classifier for `winner`.
- `data/input/test_log.txt` — example Pokémon Showdown battle log.
- `data/output/matches.csv` — battle dataset (~14k rows).
- `data/output/pokemon_regE.txt` — allowed Pokémon names (Regulation E).
- `docs/vgc-basics.md` — VGC format primer.
- `requirements_macos.txt` / `requirements_windows.txt` — environment dependencies.

### Deployment
No API/UI is included yet; run locally via notebooks.

To run:
```bash
# macOS
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements_macos.txt
jupyter lab

# Windows
py -m venv .venv && .venv\Scripts\activate
pip install -r requirements_windows.txt
jupyter lab
```

Optional:
- Run `01_web_scraper.ipynb` to regenerate `data/output/pokemon_regE.txt`.
- Use `02_pre_processing.ipynb` for modeling experiments on `data/output/matches.csv`.

Future API/CLI: TBD.

