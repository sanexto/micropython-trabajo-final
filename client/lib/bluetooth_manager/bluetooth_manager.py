import bluetooth
import struct
from micropython import const


_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_UUID16_COMPLETE = const(0x03)
_ADV_TYPE_UUID32_COMPLETE = const(0x05)
_ADV_TYPE_UUID128_COMPLETE = const(0x07)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_APPEARANCE = const(0x19)

_ADV_FLAGS_LE_ONLY = const(0x06)
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)

_ADV_INTERVAL_US = const(500_000)
_ADV_MAX_PAYLOAD = const(31)

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)


class BluetoothManager:
    FLAG_READ = const(0x0002)
    FLAG_NOTIFY = const(0x0010)

    is_on = False
    _ble = None
    _handles = {}
    _payload = None
    _connections = set()

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def on(cls, name, services):
        if cls.is_on:
            raise RuntimeError("Bluetooth is already on")
        cls._ble = bluetooth.BLE()
        cls._ble.active(True)
        cls._ble.irq(cls._irq)
        handles = cls._ble.gatts_register_services(services)
        cls._handles.clear()
        for service, service_handles in zip(services, handles):
            for characteristic, handle in zip(service[1], service_handles):
                cls._handles[str(characteristic[0])] = handle
        cls._payload = cls._build_payload(name, services)
        cls._advertise()
        cls.is_on = True

    @classmethod
    def off(cls):
        if not cls.is_on:
            raise RuntimeError("Bluetooth is not on")
        cls.is_on = False
        cls._ble.gap_advertise(None)
        for conn_handle in list(cls._connections):
            cls._ble.gap_disconnect(conn_handle)
        cls._connections.clear()
        cls._ble.active(False)
        cls._ble = None
        cls._handles.clear()
        cls._payload = None

    @classmethod
    def set(cls, uuid, value, notify=False):
        if not cls.is_on:
            raise RuntimeError("Bluetooth is not on")
        handle = cls._get_handle(uuid)
        if isinstance(value, bool):
            data = bytes((value,))
        elif isinstance(value, int):
            data = struct.pack("<i", value)
        elif isinstance(value, float):
            data = struct.pack("<f", value)
        elif isinstance(value, str):
            data = value.encode()
        else:
            raise TypeError(f"Unsupported value type: {type(value).__name__}")
        cls._ble.gatts_write(handle, data)
        if notify:
            for conn_handle in cls._connections:
                cls._ble.gatts_notify(conn_handle, handle)

    @staticmethod
    def uuid(value):
        return bluetooth.UUID(value)

    @classmethod
    def _build_payload(cls, name, services):
        payload = bytearray()

        def _append(adv_type, value):
            payload.extend(bytes((len(value) + 1, adv_type)))
            payload.extend(value)

        _append(_ADV_TYPE_FLAGS, bytes((_ADV_FLAGS_LE_ONLY,)))
        _append(_ADV_TYPE_APPEARANCE, _ADV_APPEARANCE_GENERIC_COMPUTER.to_bytes(2, "little"))
        _append(_ADV_TYPE_NAME, name.encode())

        for service in services:
            uuid = bytes(service[0])
            if len(uuid) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, uuid)
            elif len(uuid) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, uuid)
            elif len(uuid) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, uuid)

        if len(payload) > _ADV_MAX_PAYLOAD:
            raise ValueError("Advertising payload too large")

        return payload

    @classmethod
    def _advertise(cls):
        cls._ble.gap_advertise(_ADV_INTERVAL_US, cls._payload)

    @classmethod
    def _get_handle(cls, uuid):
        try:
            return cls._handles[str(cls.uuid(uuid))]
        except KeyError:
            raise ValueError(f"Unknown characteristic: {uuid}")

    @classmethod
    def _irq(cls, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            cls._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            cls._connections.discard(conn_handle)
            if cls.is_on:
                cls._advertise()
