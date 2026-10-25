# Kitchen node

Firmware for a battery sensor node that measures temperature and humidity and reports them to a home broker.

## Language

**Sample**:
One reading of temperature and humidity taken from the sensor.
_Avoid_: Measurement, reading, datapoint

**Report**:
One delivery of one or more samples to the broker.
_Avoid_: Message, upload, publish

**Cycle**:
One wake-up in which the node takes a sample, tries to report it, and goes back to sleep.
_Avoid_: Loop, tick
