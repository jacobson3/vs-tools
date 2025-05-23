import subprocess
from pathlib import Path

NIPKG_PATH = r"C:\Program Files\National Instruments\NI Package Manager\nipkg.exe"
SOURCE = r"C:\Users\MattJ\Desktop\nipkg_tests\test_package"
OUTPUT = r"C:\Users\MattJ\Desktop\nipkg_tests"


def build_package(source_path: str, output_dir: str = None) -> None:
    '''
    Builds directory indicated by source_path into NIPKG

    Args:
        source_path: Path to directory to build
    '''
    # check output directory
    if output_dir is None:
        output_dir = Path(source_path).parent

    # create command
    command = NIPKG_PATH + " pack " + \
        f"\"{source_path}\"" + f" \"{output_dir}\""
    print(command)

    # run build command
    try:
        result = subprocess.run(command, check=True)
        print(f"NIPKG Build STDOUT: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print("An error occurred building the NIPKG: ", e)


if __name__ == "__main__":
    build_package(SOURCE)
