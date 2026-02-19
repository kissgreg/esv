import ctypes
import os
import sys
import logging

# Configure logging to show timestamps and severity levels
# This is crucial for debugging embedded systems
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FirmwareBridge:
    def __init__(self):
        lib_name = "libfirmware.so" if not sys.platform.startswith("win") else "firmware.dll"
        # library is in the same directory
        lib_path = os.path.join(os.path.dirname(__file__), lib_name)
        
        logger.info(f"Initializing bridge: loading library from {lib_path}")
        
        try:
            self.lib = ctypes.CDLL(lib_path)
            # Explicitly define return types for safety
            self.lib.get_status.restype = ctypes.c_uint32
            self.lib.read_buffer.restype = ctypes.c_int32
            logger.info("Shared library loaded successfully")
        except OSError as e:
            logger.error(f"Failed to load shared library: {e}")
            raise RuntimeError(f"Failed to load shared library: {e}")

    def reset(self):
        """Reset the virtual device to its initial state."""
        logger.warning("Device RESET triggered")
        self.lib.reset_device()

    def write(self, index: int, value: int):
        """Write a 32-bit integer to the buffer at a specific index."""
        logger.info(f"WRITE operation: index={index}, value=0x{value:08X} ({value})")
        self.lib.write_buffer(ctypes.c_int(index), ctypes.c_int32(value))

    def read(self, index: int) -> int:
        """Read a 32-bit integer from the buffer."""
        val = self.lib.read_buffer(ctypes.c_int(index))
        logger.info(f"READ operation: index={index}, returned_value=0x{val:08X}")
        return val

    def get_raw_status(self) -> int:
        """Get the full 32-bit status register."""
        status = self.lib.get_status()
        # Log status only if it's non-zero to keep logs clean
        if status != 0:
            logger.debug(f"Status register read: 0x{status:08X}")
        return status

    # Property-based status bits

    @property
    def is_data_ready(self) -> bool:
        """Check if bit 0 (Data Ready) is set."""
        ready = bool(self.get_raw_status() & (1 << 0))
        if ready:
            logger.debug("Data Ready bit detected")
        return ready

    @property
    def is_critical_error(self) -> bool:
        """Check if bit 3 (Critical Error) is set."""
        error = bool(self.get_raw_status() & (1 << 3))
        if error:
            logger.critical("CRITICAL ERROR bit detected in status register!")
        return error

    @property
    def has_general_error(self) -> bool:
        """Check if bit 7 (General Error) is set."""
        error = bool(self.get_raw_status() & (1 << 7))
        if error:
            logger.error("General Error bit detected")
        return error