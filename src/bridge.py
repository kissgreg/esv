import ctypes
import os
import sys

class FirmwareBridge:
    def __init__(self):
        lib_name = "libfirmware.so" if not sys.platform.startswith("win") else "firmware.dll"
        # library is in the same directory
        lib_path = os.path.join(os.path.dirname(__file__), lib_name)
        
        try:
            self.lib = ctypes.CDLL(lib_path)
            # Explicitly define return types for safety
            self.lib.get_status.restype = ctypes.c_uint32
            self.lib.read_buffer.restype = ctypes.c_int32
        except OSError as e:
            raise RuntimeError(f"Failed to load shared library: {e}")

    def reset(self):
        """Reset the virtual device to its initial state."""
        self.lib.reset_device()

    def write(self, index: int, value: int):
        """Write a 32-bit integer to the buffer at a specific index."""
        self.lib.write_buffer(ctypes.c_int(index), ctypes.c_int32(value))

    def read(self, index: int) -> int:
        """Read a 32-bit integer from the buffer."""
        return self.lib.read_buffer(ctypes.c_int(index))

    def get_raw_status(self) -> int:
        """Get the full 32-bit status register."""
        return self.lib.get_status()

    # property-based status bits

    @property
    def is_data_ready(self) -> bool:
        """Check if bit 0 (Data Ready) is set."""
        return bool(self.get_raw_status() & (1 << 0))

    @property
    def is_critical_error(self) -> bool:
        """Check if bit 3 (Critical Error) is set."""
        return bool(self.get_raw_status() & (1 << 3))

    @property
    def has_general_error(self) -> bool:
        """Check if bit 7 (General Error) is set."""
        return bool(self.get_raw_status() & (1 << 7))