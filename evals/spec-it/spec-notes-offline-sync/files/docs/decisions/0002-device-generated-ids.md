# Device-generated note ids

Notes get UUIDs created on the device, so two replicas never hand out the same id. Server-assigned integers were rejected because an offline replica cannot get one.
