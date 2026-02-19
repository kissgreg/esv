import pytest

def test_initial_state(device):
    """Verify that the device starts in a clean state (status 0)."""
    assert device.status.read_raw() == 0, "Device status should be 0 after reset"

def test_successful_write(device):
    """Test a valid write operation and check the Data Ready bit."""
    device.memory.write(index=0, value=100)
    assert device.status.is_ready is True
    assert device.memory.read(index=0) == 100

def test_buffer_integrity(device):
    """Dedicated test for component-based memory access."""
    test_data = {0: 0xAAAA, 5: 0x5555, 9: 0xFFFF}
    for idx, val in test_data.items():
        device.memory.write(idx, val)
        assert device.memory.read(idx) == val

@pytest.mark.parametrize("invalid_index", [-1, 10, 99])
def test_out_of_bounds_write(device, invalid_index):
    """Boundary testing: Verify that invalid indices trigger the General Error bit."""
    device.memory.write(index=invalid_index, value=50)
    # Bit 7 a General Error
    assert bool(device.status.read_raw() & (1 << 7)) is True
    assert device.status.is_ready is False

def test_critical_value_edge_case(device):
    """Verify that writing the magic value 0xDEAD triggers the Critical Error bit."""
    magic_value = 0xDEAD
    device.memory.write(index=5, value=magic_value)
    assert bool(device.status.read_raw() & (1 << 3)) is True

def test_overheat_logic(device):
    """Dedicated test for the overheating component logic."""
    # 1. Set initial state with data (READY bit enabled)
    device.memory.write(0, 123)
    assert device.status.is_ready is True
    
    # 2. Setup mock sensor
    device.setup_mock_sensor(lambda: 60) # 60 fok
    
    # 3. Trigger C logic
    device.run_alarm_check()
    
    # 4. Check if overheat bit has been set and ready bit is still enabled
    assert device.status.is_overheating is True
    assert device.status.is_ready is True, "Ready bit should persist after alarm check"

def test_temperature_alarm_trigger(device):
    """Verify that the alarm bit is set when the sensor exceeds 50 degrees."""
    def mock_hot_sensor():
        return 55
        
    device.setup_mock_sensor(mock_hot_sensor)
    result = device.run_alarm_check()
    
    assert result == 1
    assert device.status.is_overheating is True

def test_temperature_no_alarm(device):
    """Verify no alarm when temperature is safe."""
    def mock_cold_sensor():
        return 20
        
    device.setup_mock_sensor(mock_cold_sensor)
    assert device.run_alarm_check() == 0
    assert device.status.is_overheating is False