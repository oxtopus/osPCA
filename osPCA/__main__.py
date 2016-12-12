import argparse
from . import osPCA, DEFAULT_MULTIPLIER


parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--multiplier", type=float, default=DEFAULT_MULTIPLIER)
parser.add_argument("--plot", action='store_true')
args = parser.parse_args()

osPCA(args.filename, args.multiplier, args.plot)








