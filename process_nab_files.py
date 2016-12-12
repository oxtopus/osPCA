import argparse
import glob
import os
from osPCA import osPCA


parser = argparse.ArgumentParser()
parser.add_argument("nabroot")
parser.add_argument("resultsDir")

if __name__ == "__main__":
  args = parser.parse_args()
  pth=os.path.abspath(os.path.join(os.path.expanduser(args.nabroot), "data"))

  for filename in glob.glob(os.path.join(pth, "*", "*.csv")):
    targetDir = os.path.join(os.path.abspath(os.path.expanduser(args.resultsDir)), "ospca", os.path.basename(os.path.dirname(filename)))
    targetResultsFilename = os.path.join(targetDir, "ospca_" + os.path.basename(filename))

    try:
      os.makedirs(targetDir)
    except os.error:
      if not os.path.isdir(targetDir):
        raise

    with open(targetResultsFilename, "r+") as outp:
      print filename, "->", targetResultsFilename
      osPCA(filename, outp=outp)


