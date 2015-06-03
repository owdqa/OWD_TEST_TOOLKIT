''' Copyright (c) 2011, Ben Firshman
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.
        * The names of its contributors may not be used to endorse or promote products
        derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import subprocess
import os

from PIL import Image
from OWDTestToolkit.utils.engines.base import EngineBase


class Engine(EngineBase):

    perceptualdiff_path = 'perceptualdiff'
    perceptualdiff_output_png = True

    def assertSameFiles(self, output_file, baseline_file, threshold):
        # Calculate threshold value as a pixel number instead of percentage.
        width, height = Image.open(output_file).size
        threshold = int(width * height * threshold)

        diff_ppm = output_file.replace(".png", ".diff.ppm")
        cmd = "%s -threshold %d -output %s %s %s" % (
            self.perceptualdiff_path, threshold, diff_ppm, baseline_file, output_file)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        perceptualdiff_stdout, _ = process.communicate()

        if process.returncode == 0:
            # No differences found
            return
        else:
            if os.path.exists(diff_ppm):
                if self.perceptualdiff_output_png:
                    # Convert the .ppm output to .png
                    diff_png = diff_ppm.replace("diff.ppm", "diff.png")
                    Image.open(diff_ppm).save(diff_png)
                    os.remove(diff_ppm)
                    diff_file_msg = ' (See %s)' % diff_png
                else:
                    diff_file_msg = ' (See %s)' % diff_ppm
            else:
                diff_file_msg = ''
            raise AssertionError("The new screenshot '%s' did not match "
                                 "the baseline '%s'%s:\n%s"
                                 % (output_file, baseline_file, diff_file_msg, perceptualdiff_stdout))
