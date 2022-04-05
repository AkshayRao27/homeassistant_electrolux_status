from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import ElectroluxStatusDataUpdateCoordinator
from .api import Appliance, ApplianceEntity

from .const import DOMAIN


class ElectroluxStatusEntity(CoordinatorEntity):
    def __init__(self, coordinator: ElectroluxStatusDataUpdateCoordinator, config_entry, pnc_id, entity_type, entity_attr, entity_source):
        super().__init__(coordinator)
        self.api = coordinator.api
        self.entity_attr = entity_attr
        self.entity_type = entity_type
        self.entity_source = entity_source
        self.config_entry = config_entry
        self.pnc_id = pnc_id
        self.entity_id = ENTITY_ID_FORMAT.format(f"{self.get_appliance.brand}_{self.get_appliance.name}_{self.entity_source}_{self.entity_attr}")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.get_entity.name

    @property
    def get_entity(self) -> ApplianceEntity:
        return self.get_appliance.get_entity(self.entity_type, self.entity_attr, self.entity_source)

    @property
    def get_appliance(self) -> Appliance:
        return self.coordinator.data['appliances'].get_appliance(self.pnc_id)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}-{self.entity_attr}-{self.entity_source}-{self.pnc_id}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.get_appliance.name)},
            "name": self.get_appliance.name,
            "model": self.get_appliance.model,
            "manufacturer": self.get_appliance.brand,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "integration": DOMAIN,
        }

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self.get_entity.device_class

    @property
    def entity_category(self):
        """Return the entity category of the sensor."""
        return self.get_entity.entity_category
