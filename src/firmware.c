#include <stdint.h>
#include <stddef.h>
#include "firmware.h"

/* Status Bit Definitions */
#define BIT_DATA_READY     (1 << 0)
#define BIT_CRITICAL_ERROR (1 << 3)
#define BIT_OVERHEAT_ALARM (1 << 4)
#define BIT_GENERAL_ERROR  (1 << 7)

/* Magic number for edge-case simulation */
#define MAGIC_CRITICAL_VAL (int32_t)0xDEAD

/* --- Hardware Mocking Section --- */

// Function pointer for the sensor read operation
static int16_t (*read_hw_sensor)(void) = NULL;

// Register a mock sensor callback from the test suite
void mock_register_sensor_callback(int16_t (*callback)(void)) {
    read_hw_sensor = callback;
}

/* --- Internal device state --- */
static uint32_t status_reg = 0;
static int32_t data_buffer[10] = {0};

int check_temperature_alarm(void) {
    if (read_hw_sensor == NULL) return -1;

    int16_t temp = read_hw_sensor();
    
    if (temp > 50) {
        status_reg |= BIT_OVERHEAT_ALARM;
        return 1;
    }
    return 0;
}

void write_buffer(int index, int32_t value) {
    if (index >= 0 && index < 10) {
        data_buffer[index] = value;
        status_reg |= BIT_DATA_READY;
        
        if (value == MAGIC_CRITICAL_VAL) {
            status_reg |= BIT_CRITICAL_ERROR;
        }
    } else {
        status_reg |= BIT_GENERAL_ERROR;
    }
}

int32_t read_buffer(int index) {
    if (index >= 0 && index < 10) {
        return data_buffer[index];
    }
    return -1; 
}

uint32_t get_status(void) {
    return status_reg;
}

void reset_device(void) {
    status_reg = 0;
    read_hw_sensor = NULL; /* Clear the mock callback as well */
    for (int i = 0; i < 10; i++) {
        data_buffer[i] = 0;
    }
}