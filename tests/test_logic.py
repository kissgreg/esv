import pytest

def test_initial_state(device):
    """Verify that the device starts in a clean state (status 0)."""
    assert device.get_raw_status() == 0, "Device status should be 0 after reset"

def test_successful_write(device):
    """Test a valid write operation and check the Data Ready bit."""
    device.write(index=0, value=100)
    assert device.is_data_ready is True
    assert device.read(index=0) == 100
    assert device.has_general_error is False

@pytest.mark.parametrize("invalid_index", [-1, 10, 99])
def test_out_of_bounds_write(device, invalid_index):
    """
    Boundary testing: Verify that invalid indices trigger the General Error bit.
    Indices 0-9 are valid, anything else is out of bounds.
    """
    device.write(index=invalid_index, value=50)
    assert device.has_general_error is True
    assert device.is_data_ready is False

def test_critical_value_edge_case(device):
    """
    Edge case testing: Verify that writing the magic value 0xDEAD 
    triggers the Critical Error bit (bit 3).
    """
    # 0xDEAD is 57005 in decimal
    magic_value = 0xDEAD
    device.write(index=5, value=magic_value)
    
    assert device.is_data_ready is True
    assert device.is_critical_error is True
    assert device.has_general_error is False

def test_temperature_alarm_trigger(device):
    """Verify that the alarm bit is set when the sensor exceeds 50 degrees."""
    
    # Define what the mock hardware should return
    def mock_hot_sensor():
        return 55  # 55 degrees Celsius
        
    device.setup_mock_sensor(mock_hot_sensor)
    
    # Trigger the logic in C
    result = device.lib.check_temperature_alarm()
    
    assert result == 1
    assert (device.get_raw_status() & (1 << 4)) != 0  # Alarm bit set

def test_temperature_no_alarm(device):
    """Verify no alarm when temperature is safe."""
    
    def mock_cold_sensor():
        return 20
        
    device.setup_mock_sensor(mock_cold_sensor)
    assert device.lib.check_temperature_alarm() == 0
    assert (device.get_raw_status() & (1 << 4)) == 0