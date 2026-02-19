import ctypes
import os
import sys
import logging

# Centralized logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StatusRegister:
    """Encapsulates status bit logic (Abstraction & Encapsulation)."""
    def __init__(self, lib):
        self._lib = lib
        self._BITS = {
            "READY": (1 << 0),
            "CRITICAL": (1 << 3),
            "OVERHEAT": (1 << 4),
            "ERROR": (1 << 7)
        }

    def read_raw(self):
        return self._lib.get_status()

    @property
    def is_overheating(self):
        status = self.read_raw()
        is_set = bool(status & self._BITS["OVERHEAT"])
        if is_set:
            logger.critical("!!! OVERHEAT DETECTED !!!")
        return is_set

    @property
    def is_ready(self):
        return bool(self.read_raw() & self._BITS["READY"])

class MemoryInterface:
    """Encapsulates buffer operations (Abstraction)."""
    def __init__(self, lib):
        self._lib = lib

    def write(self, index, value):
        logger.info(f"MEM_WRITE: [{index}] = 0x{value:08X}")
        self._lib.write_buffer(ctypes.c_int(index), ctypes.c_int32(value))

    def read(self, index):
        val = self._lib.read_buffer(ctypes.c_int(index))
        logger.info(f"MEM_READ: [{index}] -> 0x{val:08X}")
        return val

class FirmwareBridge:
    """The main 'Device' class using Composition over Inheritance."""
    def __init__(self):
        lib_name = "libfirmware.so" if not sys.platform.startswith("win") else "firmware.dll"
        lib_path = os.path.join(os.path.dirname(__file__), lib_name)
        
        try:
            self._lib = ctypes.CDLL(lib_path)
            # Configure C function signatures
            self._lib.get_status.restype = ctypes.c_uint32
            self._lib.read_buffer.restype = ctypes.c_int32
            
            # COMPOSITION: The bridge HAS-A status monitor and a memory interface
            self.status = StatusRegister(self._lib)
            self.memory = MemoryInterface(self._lib)
            
            logger.info("Hardware Bridge initialized with component-based mapping.")
        except OSError as e:
            logger.error(f"Library load failed: {e}")
            raise

    def reset(self):
        """Orchestrates reset across components."""
        logger.warning("System-wide reset initiated.")
        self._lib.reset_device()

    def setup_mock_sensor(self, callback):
        """Polymorphism: Injecting Python behavior into C."""
        CALLBACK_TYPE = ctypes.CFUNCTYPE(ctypes.c_int16)
        self._sensor_cb = CALLBACK_TYPE(callback)
        self._lib.mock_register_sensor_callback(self._sensor_cb)
        logger.info("Mock sensor driver registered.")

    def run_alarm_check(self):
        """Triggers the firmware's internal logic."""
        return self._lib.check_temperature_alarm()