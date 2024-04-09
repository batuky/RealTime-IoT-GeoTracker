class DeviceNotFoundError(Exception):
    """Exception raised when a device is not found in the database."""
    
    def __init__(self, device_id, message="Device with id {} not found."):
        self.device_id = device_id
        self.message = message.format(device_id)
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (Device ID: {self.device_id})"