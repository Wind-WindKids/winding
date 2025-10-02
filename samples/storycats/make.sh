rm export/*
python ../../src/illuminate.py --outdir ./ --bleed 0.125 --dry-run winding.md --copy  --trim 8.5x6
mkdir tmp
python ../../src/outpainting.py export/*.png --pixelate
rm -rf pdf
python ../../src/illuminate.py --outdir ./ --bleed 0.125 --dry-run winding.md --export-pdf  --trim 8.5x6
