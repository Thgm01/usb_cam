# Copyright 2023 usb_cam Authors
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the usb_cam Authors nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from typing import List, Optional, Tuple
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from pydantic import BaseModel, Field, field_validator, model_validator

USB_CAM_DIR = get_package_share_directory('usb_cam')


class CameraConfig(BaseModel):
    name: str = 'camera1'
    param_path: Path = Field(default_factory=lambda: Path(USB_CAM_DIR, 'config', 'params_1.yaml'))
    remappings: Optional[List[Tuple[str, str]]] = None
    namespace: Optional[str] = None

    @field_validator('param_path')
    @classmethod
    def validate_param_path(cls, value: Path) -> Path:
        if value and not value.exists():
            raise FileNotFoundError(f'Could not find parameter file: {value}')
        return value

    @model_validator(mode='after')
    def validate_root(self) -> 'CameraConfig':
        if self.name and not self.remappings:
            self.remappings = [
                ('image_raw', f'{self.name}/image_raw'),
                ('image_raw/compressed', f'{self.name}/image_compressed'),
                ('image_raw/compressedDepth', f'{self.name}/compressedDepth'),
                ('image_raw/theora', f'{self.name}/image_raw/theora'),
                ('camera_info', f'{self.name}/camera_info'),
            ]
        return self