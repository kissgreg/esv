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

/**
 * @brief Registers a callback function to simulate hardware sensor readings.
 * * This allows the test environment to inject mock sensor data into the firmware
 * logic without requiring physical hardware.
 * * @param callback Pointer to a function that returns a 16-bit signed integer.
 */
void mock_register_sensor_callback(int16_t (*callback)(void));

/**
 * @brief Evaluates the current temperature from the registered sensor.
 * * Reads the value from the mocked sensor. If the value exceeds 50 degrees,
 * it sets the 'Overheat Alarm' bit (bit 4) in the status register.
 * * @return 1 if alarm is triggered, 0 if safe, -1 if no sensor is registered.
 */
int check_temperature_alarm(void);

#endif // FIRMWARE_H