import pytest
from src.bridge import FirmwareBridge

@pytest.fixture(scope="function")
def device():
    """
    Fixture to provide a clean virtual device instance for each test.
    Ensures the device is reset before the test starts and cleaned up after.
    """
    # Setup: Initialize the bridge and reset the C-state
    bridge = FirmwareBridge()
    bridge.reset()
    
    yield bridge
    
    # Teardown: Final reset to ensure no side effects for the next test
    bridge.reset()