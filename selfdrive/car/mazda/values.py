from dataclasses import dataclass, field
from typing import Dict, List, Union

from cereal import car
from selfdrive.car import dbc_dict
from selfdrive.car.docs_definitions import CarHarness, CarInfo, CarParts
from selfdrive.car.fw_query_definitions import FwQueryConfig, Request, StdQueries

Ecu = car.CarParams.Ecu

# Steer torque limits
class CarControllerParams:
  def __init__(self, CP):
    self.STEER_STEP = 1 # 100 Hz
    if CP.carFingerprint in GEN1:
      self.STEER_MAX = 800                # theoretical max_steer 2047
      self.STEER_DELTA_UP = 10             # torque increase per refresh
      self.STEER_DELTA_DOWN = 25           # torque decrease per refresh
      self.STEER_DRIVER_ALLOWANCE = 15     # allowed driver torque before start limiting
      self.STEER_DRIVER_MULTIPLIER = 1     # weight driver torque
      self.STEER_DRIVER_FACTOR = 1         # from dbc
      self.STEER_ERROR_MAX = 350           # max delta between torque cmd and torque motor
      
      self.TI_STEER_MAX = 600                # theoretical max_steer 2047
      self.TI_STEER_DELTA_UP = 6             # torque increase per refresh
      self.TI_STEER_DELTA_DOWN = 15           # torque decrease per refresh
      self.TI_STEER_DRIVER_ALLOWANCE = 5    # allowed driver torque before start limiting
      self.TI_STEER_DRIVER_MULTIPLIER = 40     # weight driver torque
      self.TI_STEER_DRIVER_FACTOR = 1         # from dbc
      self.TI_STEER_ERROR_MAX = 350           # max delta between torque cmd and torque motor
    if CP.carFingerprint in GEN2:
      self.STEER_MAX = 8000                 
      self.STEER_DELTA_UP = 45              # torque increase per refresh
      self.STEER_DELTA_DOWN = 80            # torque decrease per refresh
      self.STEER_DRIVER_ALLOWANCE = 1400     # allowed driver torque before start limiting
      self.STEER_DRIVER_MULTIPLIER = 5      # weight driver torque
      self.STEER_DRIVER_FACTOR = 1           # from dbc
      self.STEER_ERROR_MAX = 3500            # max delta between torque cmd and torque motor


class TI_STATE:
  DISCOVER = 0
  OFF = 1
  DRIVER_OVER = 2
  RUN = 3
  

class CAR:
  CX5 = "MAZDA CX-5"
  CX9 = "MAZDA CX-9"
  MAZDA3 = "MAZDA 3"
  MAZDA6 = "MAZDA 6"
  CX9_2021 = "MAZDA CX-9 2021"
  CX5_2022 = "MAZDA CX-5 2022"
  MAZDA3_2019 = "MAZDA 3 2019"
  CX_30 = "MAZDA CX-30"
  CX_50 = "MAZDA CX-50"
  CX_60 = "MAZDA CX-60"
  CX_70 = "MAZDA CX-70"
  CX_80 = "MAZDA CX-80"
  CX_90 = "MAZDA CX-90"


@dataclass
class MazdaCarInfo(CarInfo):
  package: str = "All"
  car_parts: CarParts = field(default_factory=CarParts.common([CarHarness.mazda]))


CAR_INFO: Dict[str, Union[MazdaCarInfo, List[MazdaCarInfo]]] = {
  CAR.CX5: MazdaCarInfo("Mazda CX-5 2017-21"),
  CAR.CX9: MazdaCarInfo("Mazda CX-9 2016-20"),
  CAR.MAZDA3: MazdaCarInfo("Mazda 3 2017-18"),
  CAR.MAZDA6: MazdaCarInfo("Mazda 6 2017-20"),
  CAR.CX9_2021: MazdaCarInfo("Mazda CX-9 2021-23", video_link="https://youtu.be/dA3duO4a0O4"),
  CAR.CX5_2022: MazdaCarInfo("Mazda CX-5 2022-23"),
  CAR.MAZDA3_2019: MazdaCarInfo("Mazda 3 2019-23"),
  CAR.CX_30: MazdaCarInfo("Mazda CX-30 2019-23"),
  CAR.CX_50: MazdaCarInfo("Mazda CX-50 2022-23"),
  CAR.CX_60: MazdaCarInfo("Mazda CX-60 unreleased"),
  CAR.CX_70: MazdaCarInfo("Mazda CX-70 unreleased"),
  CAR.CX_80: MazdaCarInfo("Mazda CX-80 unreleased"),
  CAR.CX_90: MazdaCarInfo("Mazda CX-90 2023"),
}


class LKAS_LIMITS:
  STEER_THRESHOLD = 15
  DISABLE_SPEED = 0    # kph
  ENABLE_SPEED = 0     # kph
  TI_STEER_THRESHOLD = 15
  TI_DISABLE_SPEED = 0    # kph
  TI_ENABLE_SPEED = 0     # kph



class Buttons:
  NONE = 0
  SET_PLUS = 1
  SET_MINUS = 2
  RESUME = 3
  CANCEL = 4
  TURN_ON = 5

FW_QUERY_CONFIG = FwQueryConfig(
  requests=[
    # Log responses on powertrain bus
    Request(
      [StdQueries.MANUFACTURER_SOFTWARE_VERSION_REQUEST],
      [StdQueries.MANUFACTURER_SOFTWARE_VERSION_RESPONSE],
      bus=0,
      logging=True,
    ),
    Request(
      [StdQueries.TESTER_PRESENT_REQUEST, StdQueries.MANUFACTURER_SOFTWARE_VERSION_REQUEST],
      [StdQueries.TESTER_PRESENT_RESPONSE, StdQueries.MANUFACTURER_SOFTWARE_VERSION_RESPONSE],
    ),
    Request(
      [StdQueries.TESTER_PRESENT_REQUEST, StdQueries.MANUFACTURER_SOFTWARE_VERSION_REQUEST],
      [StdQueries.TESTER_PRESENT_RESPONSE, StdQueries.MANUFACTURER_SOFTWARE_VERSION_RESPONSE],
    )
  ],
)

FW_VERSIONS = {
  CAR.CX5_2022: {
    (Ecu.eps, 0x730, None): [
      b'KSD5-3210X-C-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PX2G-188K2-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2H-188K2-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX85-188K2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'SH54-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXFG-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'K131-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'KSD5-437K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'GSH7-67XK2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-T\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PYB2-21PS1-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'SH51-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXDL-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXFG-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },
  CAR.CX5: {
    (Ecu.eps, 0x730, None): [
      b'K319-3210X-A-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KCB8-3210X-B-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KJ01-3210X-G-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KJ01-3210X-J-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KJ01-3210X-M-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PA53-188K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PAR4-188K2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFA-188K2-J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFC-188K2-J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFD-188K2-J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYNF-188K2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2F-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2G-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2H-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2H-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2H-188K2-G\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2K-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX38-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX42-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX68-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'SHKT-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'K123-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'K123-437K2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KBJ5-437K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KL2K-437K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KN0W-437K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'B61L-67XK2-R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-T\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-V\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-M\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-N\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PA66-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PA66-21PS1-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX39-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX39-21PS1-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX68-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB1-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB1-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB1-21PS1-G\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB2-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB2-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB2-21PS1-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB2-21PS1-G\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYB2-21PS1-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYNC-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'SH9T-21PS1-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },

  CAR.CX9 : {
    (Ecu.eps, 0x730, None): [
      b'K070-3210X-C-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KJ01-3210X-G-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KJ01-3210X-L-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PX23-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX24-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM4-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXN8-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXN8-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYD7-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYD8-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFM-188K2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFM-188K2-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'K123-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TK80-67XK2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TK80-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'TA0B-437K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TK79-437K2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TK79-437K2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TM53-437K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TN40-437K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'B61L-67XK2-P\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-V\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-J\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-K\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'TK80-67XK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
   ],
    (Ecu.transmission, 0x7e1, None): [
      b'PXM4-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM7-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM7-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFM-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYFM-21PS1-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYD5-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYD5-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYD6-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYD6-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },

  CAR.MAZDA3: {
    (Ecu.eps, 0x730, None): [
      b'BHN1-3210X-J-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K070-3210X-C-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'KR11-3210X-K-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',

    ],
    (Ecu.engine, 0x7e0, None): [
      b'P5JD-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PY2P-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYJW-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYKC-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYKE-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'B63C-67XK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GHP9-67Y10---41\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'B45A-437AS-0-08\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'B61L-67XK2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-P\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-Q\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-T\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PY2S-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'P52G-21PS1-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYKA-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYKE-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYKE-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },

  CAR.MAZDA6: {
    (Ecu.eps, 0x730, None): [
      b'GBEF-3210X-B-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GBEF-3210X-C-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GFBC-3210X-A-00\000\000\000\000\000\000\000\000\000',
      b'GFBC-3210X-A-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PA34-188K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX4F-188K2-D\000\000\000\000\000\000\000\000\000\000\000\000',
      b'PYH7-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYH7-188K2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PANX-188K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'K131-67XK2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-E\000\000\000\000\000\000\000\000\000\000\000\000',
      b'K131-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'GBVH-437K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GBVH-437K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GDDM-437K2-A\000\000\000\000\000\000\000\000\000\000\000\000',
      b'GDDM-437K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'B61L-67XK2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B61L-67XK2-T\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-P\000\000\000\000\000\000\000\000\000\000\000\000',
      b'GSH7-67XK2-T\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PA28-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PYH3-21PS1-D\000\000\000\000\000\000\000\000\000\000\000\000',
      b'PYH7-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PA28-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },

  CAR.CX9_2021 : {
    (Ecu.eps, 0x730, None): [
      b'TC3M-3210X-A-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PXGW-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM4-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM4-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM6-188K2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXGW-188K2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'K131-67XK2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'K131-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'TA0B-437K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'GSH7-67XK2-M\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-N\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-P\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'GSH7-67XK2-T\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PXM4-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXM6-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },
  
  CAR.MAZDA3_2019 : {
    (Ecu.eps, 0x730, None): [
      b'BDGF-3216X-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BCKA-3216X-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BCKA-3216X-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      #b'BDGF-3216X-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BCKA-3216X-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      #b'PX06-188K2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX06-188K2-N\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX08-188K2-L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX4W-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'BDTS-67XK2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BDTS-67XK2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      #b'B0N2-67XK2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B0N2-67XK2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'BFVV-4300F-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BHCB-4300F-\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BCKA-4300F-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      #b'BCKA-4300F-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BFVV-4300F-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'BDGF-67WK2-K\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BDGF-67WK2-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      #b'BDGF-67WK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'DFR5-67WK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      #b'PX01-21PS1-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX03-21PS1-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX4K-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },
  CAR.CX_30 : {
    (Ecu.eps, 0x730, None): [
      b'DFR5-3216X-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BDGF-3216X-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PX06-188K2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'BDTS-67XK2-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'B0N2-67XK2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'DEJW-4300F-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BCKA-4300F-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'BDGF-67WK2-K\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'BDGF-67WK2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PX01-21PS1-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },
  
  CAR.CX_50 : {
    (Ecu.eps, 0x730, None): [
      b'VA40-3216Y-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PX06-188K2-N\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX08-188K2-L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX4W-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'VA45-67XK2-\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.abs, 0x760, None): [
      b'VA40-4300F-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'VA40-67WK2-\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      #b'PX01-21PS1-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX03-21PS1-E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX4K-21PS1-B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },
}


DBC = {
  CAR.CX5: dbc_dict('mazda_2017', None),
  CAR.CX9: dbc_dict('mazda_2017', None),
  CAR.MAZDA3: dbc_dict('mazda_2017', None),
  CAR.MAZDA6: dbc_dict('mazda_2017', None),
  CAR.CX9_2021: dbc_dict('mazda_2017', None),
  CAR.CX5_2022: dbc_dict('mazda_2017', None),
  CAR.MAZDA3_2019: dbc_dict('mazda_2019', None),
  CAR.CX_30: dbc_dict('mazda_2019', None),
  CAR.CX_50: dbc_dict('mazda_2019', None),
  CAR.CX_60: dbc_dict('mazda_2019', None),
  CAR.CX_70: dbc_dict('mazda_2019', None),
  CAR.CX_80: dbc_dict('mazda_2019', None),
  CAR.CX_90: dbc_dict('mazda_2019', None),
}

# Gen 1 hardware: same CAN messages and same camera
GEN1 = {CAR.CX5, CAR.CX9, CAR.CX9_2021, CAR.MAZDA3, CAR.MAZDA6, CAR.CX5_2022}
GEN2 = {CAR.MAZDA3_2019, CAR.CX_30, CAR.CX_50, CAR.CX_60, CAR.CX_70, CAR.CX_80, CAR.CX_90}
