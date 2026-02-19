#include <stdint.h>
#include "firmware.h"

/* Internal device state */
static uint32_t status_reg = 0;
static int32_t data_buffer[10] = {0};

/* Status Bit Definitions */
#define BIT_DATA_READY     (1 << 0)
#define BIT_CRITICAL_ERROR (1 << 3)
#define BIT_GENERAL_ERROR  (1 << 7)

/* Magic number for edge-case simulation */
#define MAGIC_CRITICAL_VAL (int32_t)0xDEAD

void write_buffer(int index, int32_t value) {
    if (index >= 0 && index < 10) {
        data_buffer[index] = value;
        
        /* Set Data Ready bit */
        status_reg |= BIT_DATA_READY;
        
        /* Edge case: Trigger critical error if specific value is written */
        if (value == MAGIC_CRITICAL_VAL) {
            status_reg |= BIT_CRITICAL_ERROR;
        }
    } else {
        /* Set General Error bit if index is out of bounds */
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
    for (int i = 0; i < 10; i++) {
        data_buffer[i] = 0;
    }
}