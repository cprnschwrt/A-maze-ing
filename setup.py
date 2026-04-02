
def build_package() -> None:
    from setuptools import setup
    dependencies = None
    with open("requirements.txt") as f:
        dependencies = f.read().splitlines()
    setup(
        name="mazegen",
        version="0.0.1",
        description="a maze generator and solver with visualizer.",
        author="bgix, cschwart",
        install_requires=dependencies,
    )


if __name__ == "__main__":
    build_package()
