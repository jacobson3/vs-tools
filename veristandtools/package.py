import subprocess
from pathlib import Path
import os
import shutil
from typing import List

NIPKG_PATH = r"C:\Program Files\National Instruments\NI Package Manager\nipkg.exe"
OUTPUT = r"C:\Users\MattJ\Desktop\nipkg_tests"


class PackageBuilder():

    def __init__(self):
        self._package_dir = ""
        self._vs_version = ""
        self._package_vs_dir = ""
        self._package_documents_dir = ""
        self._package_control_dir = ""

    def build_package(self, source_path: str, output_dir: str = None) -> None:
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

    def create_package(self, vs_version: str, project_paths: List[str] = None, output_dir: str = None) -> None:
        '''
        Creates NI package for distributing VeriStand projects.

        Args:
            vs_version: Year of VeriStand package is being created for (e.g. "2021")
            project_paths: Paths to any additional files/folders to include in the package
            output_dir: Directory where output will be build (default to pwd)
        '''
        # set default output directory if needed
        if output_dir is None:
            output_dir = os.getcwd()

        # make sure package_dir doesn't already exist
        package_dir = os.path.join(output_dir, "veristand_package")
        i = 1
        while os.path.exists(package_dir):
            package_dir = os.path.join(
                output_dir, f"veristand_package_{i}")
            i += 1

        self._vs_version = vs_version
        self._package_dir = package_dir

        self._create_package_layout()
        self._copy_custom_devices()
        # self._copy_slsc_plugins()
        # self._copy_project_files()
        # self._create_control_file()
        # self.build_package()

    def _create_package_layout(self) -> None:
        '''
        Creates basic folder/file layout for NI package build.
        '''
        # build paths
        self._package_documents_dir = os.path.join(
            self._package_dir, "data", "documents")
        self._package_vs_dir = os.path.join(self._package_documents_dir,
                                            "National Instruments", f"NI VeriStand {self._vs_version}")
        self._package_control_dir = os.path.join(self._package_dir, "control")

        # create layout
        os.makedirs(self._package_vs_dir)
        os.makedirs(self._package_control_dir)

        with open(os.path.join(self._package_dir, "debian-binary"), "w") as db_file:
            db_file.write("2.0")

    def _copy_custom_devices(self) -> None:
        '''
        Copies all custom devices into package build folder
        '''
        cd_folder = os.path.join(os.environ["PUBLIC"], "Documents", "National Instruments",
                                 f"NI VeriStand {self._vs_version}", "Custom Devices")

        if os.path.exists(cd_folder):
            shutil.copytree(cd_folder, os.path.join(
                self._package_vs_dir, "Custom Devices"))


if __name__ == "__main__":
    pb = PackageBuilder()
    pb.create_package("2021")
