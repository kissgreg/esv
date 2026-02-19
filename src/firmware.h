#ifndef FIRMWARE_H
#define FIRMWARE_H

#include <stdint.h>

// functions to handle registers and buffer

/**
 * @brief Writes a 32-bit value to the virtual data buffer.
 * @param index The buffer index (0-9).
 * @param value The integer value to store.
 */
void write_buffer(int index, int32_t value);

/**
 * @brief Reads a 32-bit value from the virtual data buffer.
 * @param index The buffer index (0-9).
 * @return The stored value or -1 if index is out of bounds.
 */
int32_t read_buffer(int index);

/**
 * @brief Returns the current 32-bit status register.
 * @return 32-bit unsigned integer representing device status bits.
 */
uint32_t get_status(void);

/**
 * @brief Resets the status register and clears the data buffer.
 */
void reset_device(void);

#endif // FIRMWARE_H