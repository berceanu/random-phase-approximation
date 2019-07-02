"""
Various utilities to manage the TALYS code.
"""
import logging
import pathlib
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Talys:
    input_fn = "input.txt"
    input_template_fn = "input.j2"
    energy_fn = "energy.in"
    output_fn = "output.txt"
    binary_fn = pathlib.PosixPath("~/bin/talys").expanduser()
    hfb_path = pathlib.PosixPath("~/src/talys/structure/gamma/hfb/").expanduser()
    stderr_fn = "stderr.txt"
    cross_section_fn = "xs000000.tot"
    cross_section_png_fn = "xsec.png"

    @property
    def run_command(self) -> str:
        """Construct the TALYS command to be ran."""
        assert self.binary_fn.is_file(), f"{self.binary_fn} not found!"

        return (
            f"{self.binary_fn} < {self.input_fn} > {self.output_fn} 2> {self.stderr_fn}"
        )


talys = Talys()

if __name__ == "__main__":
    print(talys.run_command)
