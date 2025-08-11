import argparse
from fluxion.api import Scene, Circle, Text, render_to_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="Path to a script that builds and returns a Scene object (python file)")
    parser.add_argument("-o", "--out", default="out.mp4", help="Output video path")
    args = parser.parse_args()

    # Simple runner: script should define a function `build_scene()` returning a Scene
    ns = {}
    with open(args.script, "r") as f:
        code = f.read()
    exec(code, ns)
    if "build_scene" not in ns:
        raise RuntimeError("example script must define build_scene() returning a Scene")
    scene = ns["build_scene"]()
    render_to_file(scene, args.out)
    print("Saved:", args.out)

if __name__ == "__main__":
    main()
