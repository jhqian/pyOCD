# pyOCD debugger
# Copyright (c) 2015-2020 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple

from .ap import AccessPort
from .cortex_m import CortexM
from .cortex_m_v8m import CortexM_v8M
from .fpb import FPB
from .dwt import (DWT, DWTv2)
from .itm import ITM
from .tpiu import TPIU
from .gpr import GPR

# Component classes.
ROM_TABLE_CLASS = 0x1
CORESIGHT_CLASS = 0x9
GENERIC_CLASS = 0xe
SYSTEM_CLASS = 0xf # CoreLink, PrimeCell, or other system component with no standard register layout.

#  [11:8] continuation
#  [6:0]  ID
ARM_ID = 0x43b
FSL_ID = 0x00e

# CoreSight devtype
#  Major Type [3:0]
#  Minor Type [7:4]
#
# CoreSight Major Types
#  0 = Miscellaneous
#  1 = Trace Sink
#  2 = Trace Link
#  3 = Trace Source
#  4 = Debug Control
#  5 = Debug Logic
#
# Known devtype values
#  0x11 = TPIU
#  0x21 = ETB
#  0x12 = Trace funnel (CSFT)
#  0x13 = CPU trace source (ETM, MTB?)
#  0x16 = PMU
#  0x43 = ITM
#  0x14 = ECT/CTI/CTM
#  0x31 = MTB
#  0x32 = TMC
#  0x34 = Granular Power Requestor

## Pairs a component name with a factory method.
CmpInfo = namedtuple('CmpInfo', 'name factory')

## Map from (designer, class, part, devtype, archid) to component name and class.
COMPONENT_MAP = {
  # Designer|Component Class |Part  |Type |Archid
    (ARM_ID, CORESIGHT_CLASS, 0x193, 0x00, 0x0a57) : CmpInfo('CS-600 TSGEN',            None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x906, 0x14, 0)      : CmpInfo('CTI',       None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x907, 0x21, 0)      : CmpInfo('ETB',       None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x908, 0x12, 0)      : CmpInfo('CSTF',      None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x912, 0x11, 0)      : CmpInfo('TPIU',      TPIU.factory    ),
    (ARM_ID, CORESIGHT_CLASS, 0x923, 0x11, 0)      : CmpInfo('TPIU-M3',   TPIU.factory    ),
    (ARM_ID, CORESIGHT_CLASS, 0x924, 0x13, 0)      : CmpInfo('ETM-M3',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x925, 0x13, 0)      : CmpInfo('ETM-M4',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x932, 0x31, 0x0a31) : CmpInfo('MTB-M0+',   None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x950, 0x13, 0)      : CmpInfo('PTM-A9',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x961, 0x32, 0)      : CmpInfo('TMC ETF',   None            ), # Trace Memory Controller
    (ARM_ID, CORESIGHT_CLASS, 0x975, 0x13, 0x4a13) : CmpInfo('ETM-M7',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x9a0, 0x16, 0)      : CmpInfo('PMU-A9',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x9a1, 0x11, 0)      : CmpInfo('TPIU-M4',   TPIU.factory    ),
    (ARM_ID, CORESIGHT_CLASS, 0x9a3, 0x13, 0x0)    : CmpInfo('MTB-M0',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x9a4, 0x34, 0x0a34) : CmpInfo('GPR',       GPR.factory     ), # Granular Power Requestor
    (ARM_ID, CORESIGHT_CLASS, 0x9a6, 0x14, 0x1a14) : CmpInfo('CTI',       None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e2, 0x00, 0x0a17) : CmpInfo('CS-600 APB-AP',           AccessPort.create   ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e3, 0x00, 0x0a17) : CmpInfo('CS-600 AHB-AP',           AccessPort.create   ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e4, 0x00, 0x0a17) : CmpInfo('CS-600 AXI-AP',           AccessPort.create   ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e5, 0x00, 0x0a47) : CmpInfo('CS-600 APv1 Adapter',     AccessPort.create   ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e6, 0x00, 0x0a27) : CmpInfo('CS-600 JTAG-AP',          AccessPort.create   ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e7, 0x11, 0)      : CmpInfo('CS-600 TPIU',             TPIU.factory        ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e8, 0x21, 0)      : CmpInfo('CS-600 TMC ETR',          None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9e9, 0x21, 0)      : CmpInfo('CS-600 TMC ETB',          None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9ea, 0x32, 0)      : CmpInfo('CS-600 TMC ETF',          None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9eb, 0x12, 0)      : CmpInfo('CS-600 ATB Funnel',       None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9ec, 0x22, 0)      : CmpInfo('CS-600 ATB Replicator',   None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9ed, 0x14, 0x1a14) : CmpInfo('CS-600 CTI',              None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9ee, 0x00, 0)      : CmpInfo('CS-600 CATU',             None                ),
    (ARM_ID, CORESIGHT_CLASS, 0x9ef, 0x00, 0x0a57) : CmpInfo('CS-600 SDC-600',          None                ),
    (ARM_ID, CORESIGHT_CLASS, 0xc05, 0x15, 0)      : CmpInfo('CPU-A5',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xc07, 0x15, 0)      : CmpInfo('CPU-A7',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xc08, 0x15, 0)      : CmpInfo('CPU-A8',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xc09, 0x15, 0)      : CmpInfo('CPU-A9',    None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xc0d, 0x15, 0)      : CmpInfo('CPU-A12',   None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xc0e, 0x15, 0)      : CmpInfo('CPU-A17',   None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xc0f, 0x15, 0)      : CmpInfo('CPU-A15',   None            ),
    (ARM_ID, CORESIGHT_CLASS, 0x9a9, 0x11, 0)      : CmpInfo('TPIU-M7',   TPIU.factory    ),
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x11, 0)      : CmpInfo('TPIU-M23',  TPIU.factory    ),
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x13, 0)      : CmpInfo('ETM-M23',   None            ),
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x31, 0x0a31) : CmpInfo('MTB-M23',   None            ), # M23
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x00, 0x1a02) : CmpInfo('DWT',       DWTv2.factory   ), # M23
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x00, 0x1a03) : CmpInfo('BPU',       FPB.factory     ), # M23
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x14, 0x1a14) : CmpInfo('CTI',       None            ), # M23
    (ARM_ID, CORESIGHT_CLASS, 0xd20, 0x00, 0x2a04) : CmpInfo('SCS-M23',   CortexM_v8M.factory ), # M23
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x31, 0x0a31) : CmpInfo('MTB-M33',   None            ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x43, 0x1a01) : CmpInfo('ITM',       ITM.factory     ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x00, 0x1a02) : CmpInfo('DWT',       DWTv2.factory   ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x00, 0x1a03) : CmpInfo('BPU',       FPB.factory     ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x14, 0x1a14) : CmpInfo('CTI',       None            ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x00, 0x2a04) : CmpInfo('SCS-M33',   CortexM_v8M.factory ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x13, 0x4a13) : CmpInfo('ETM-M33',   None            ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd21, 0x11, 0)      : CmpInfo('TPIU-M33',  TPIU.factory    ), # M33
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x31, 0x0a31) : CmpInfo('MTB-M35P',  None            ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x43, 0x1a01) : CmpInfo('ITM-M35P',  ITM.factory     ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x00, 0x1a02) : CmpInfo('DWT-M35P',  DWTv2.factory   ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x00, 0x1a03) : CmpInfo('BPU-M35P',  FPB.factory     ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x14, 0x1a14) : CmpInfo('CTI-M35P',  None            ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x00, 0x2a04) : CmpInfo('SCS-M35P',  CortexM_v8M.factory ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x13, 0x4a13) : CmpInfo('ETM-M35P',  None            ), # M35P
    (ARM_ID, CORESIGHT_CLASS, 0xd31, 0x11, 0)      : CmpInfo('TPIU-M35P', TPIU.factory    ), # M35P
    (ARM_ID, GENERIC_CLASS,   0x000, 0x00, 0)      : CmpInfo('SCS-M3',    CortexM.factory ),
    (ARM_ID, GENERIC_CLASS,   0x001, 0x00, 0)      : CmpInfo('ITM',       ITM.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x002, 0x00, 0)      : CmpInfo('DWT',       DWT.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x003, 0x00, 0)      : CmpInfo('FPB',       FPB.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x004, 0x00, 0)      : CmpInfo('SCS-SC300', CortexM.factory ),
    (ARM_ID, GENERIC_CLASS,   0x005, 0x00, 0)      : CmpInfo('ITM',       ITM.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x006, 0x00, 0)      : CmpInfo('DWT',       DWT.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x007, 0x00, 0)      : CmpInfo('FPB',       FPB.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x008, 0x00, 0)      : CmpInfo('SCS-M0+',   CortexM.factory ),
    (ARM_ID, GENERIC_CLASS,   0x00a, 0x00, 0)      : CmpInfo('DWT-M0+',   DWT.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x00b, 0x00, 0)      : CmpInfo('BPU',       FPB.factory     ),
    (ARM_ID, GENERIC_CLASS,   0x00c, 0x00, 0)      : CmpInfo('SCS-M4',    CortexM.factory ),
    (ARM_ID, GENERIC_CLASS,   0x00d, 0x00, 0)      : CmpInfo('SCS-SC000', CortexM.factory ),
    (ARM_ID, GENERIC_CLASS,   0x00e, 0x00, 0)      : CmpInfo('FPB',       FPB.factory     ),
    (ARM_ID, SYSTEM_CLASS,    0x101, 0x00, 0)      : CmpInfo('TSGEN',     None            ), # Timestamp Generator
    (FSL_ID, CORESIGHT_CLASS, 0x000, 0x04, 0)      : CmpInfo('MTBDWT',    None            ),
    }

