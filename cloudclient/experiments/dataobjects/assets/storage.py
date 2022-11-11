from energy import EnergyAsset, AmbientTempTypeEnum
from enum import Enum


class StorageAssetTypeEnum(Enum):
    electric_heavy_goods_vehicle = "ELECTRIC_HEAVY_GOODS_VEHICLE"
    electric_vehicle = "ELECTRIC_VEHICLE"
    storage_electric = "STORAGE_ELECTRIC"
    storage_heat = "STORAGE_HEAT"


class StorageAsset(EnergyAsset):
    asset_type: StorageAssetTypeEnum
    stateOfCharge_r: float


class HeatStorageAsset(StorageAsset):
    capacityHeat_kW: float
    stateOfCharge_r: float
    minTemp_degC: int
    maxTemp_degC: int
    setTemp_degC: int
    lossFactor_WpK: float
    heatCapacity_JpK: float
    ambientTempType: AmbientTempTypeEnum


class ElectricStorageAsset(StorageAsset):
    capacityElectricity_kW: float
    storageCapacity_kWh: float


class VehicleElectricStorageAsset(ElectricStorageAsset):
    pass


if __name__ == "__main__":

    dummy_data = {
        "alias": "XL windmill",
        "asset_type": "WINDMILL",
        "capacityElectricity_kW": 7000.0,
    }

    asset = ElectricStorageAsset(**dummy_data)
    import json

    print(json.dumps(json.loads(asset.json()), indent=4))

    # to generate the class diagram
    # pyreverse <filename> -o html
