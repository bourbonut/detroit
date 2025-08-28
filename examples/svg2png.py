"""
Useful script for transforming `.svg` files into `.png`
"""
from pathlib import Path
import cairosvg
from concurrent.futures import ProcessPoolExecutor

def svg2png(file: Path):
    cairosvg.svg2png(url=str(file), write_to=f"{file.stem}.png")

with ProcessPoolExecutor() as pool:
    for _ in pool.map(svg2png, Path().glob("*.svg")):
        pass
