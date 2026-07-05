import asyncio, json

from microdot import Microdot, Response
from microdot.utemplate import Template
from microdot.websocket import with_websocket

import config
from db_manager import DBManager
from mqtt import MQTTManager, MQTTMessage


class Main:
    _mqtt = None
    _app = None
    _clients = set()

    _fan_on = False

    def __init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated")

    @classmethod
    def run(cls):
        cls._setup_mqtt()
        cls._setup_web()
        asyncio.run(cls._loop())

    @classmethod
    def _setup_mqtt(cls):
        cls._mqtt = MQTTManager.get_client(config.MQTT_MANAGER_CLIENT_ID)
        cls._mqtt.set_callback(cls._on_message)

        print("MQTT: Connecting...")
        cls._mqtt.connect()
        print("MQTT: Connected")

        print("MQTT: Subscribing...")
        cls._mqtt.subscribe(config.MQTT_MANAGER_SUBSCRIBE_TOPIC)
        print("MQTT: Subscribed")

    @classmethod
    def _setup_web(cls):
        cls._app = Microdot()
        Response.default_content_type = "text/html"

        @cls._app.route("/")
        async def index(req):
            return Template("dashboard.html").render()

        @cls._app.route("/logs")
        async def logs(req):
            return Template("logs.html").render()

        @cls._app.route("/static/<path:path>")
        async def static(req, path):
            if ".." in path:
                return "Not found", 404
            return Response.send_file(f"static/{path}")

        @cls._app.route("/api/logs")
        async def api_logs(req):
            logs = DBManager.get().get_table_rows("log")
            logs.sort(key=lambda log: log["id"], reverse=True)
            return logs

        @cls._app.route("/api/readings")
        async def api_readings(req):
            return {
                "limit": config.READING_HISTORY_LIMIT,
                "readings": DBManager.get().get_table_rows("reading"),
            }

        @cls._app.route("/ws")
        @with_websocket
        async def ws(req, socket):
            cls._clients.add(socket)
            try:
                while True:
                    await socket.receive()
            finally:
                cls._clients.discard(socket)

    @classmethod
    async def _loop(cls):
        await asyncio.gather(
            cls._main_loop(),
            cls._ping_loop(),
            cls._app.start_server(host="0.0.0.0", port=80),
        )

    @classmethod
    async def _main_loop(cls):
        while True:
            cls._mqtt.check_msg()
            await asyncio.sleep_ms(config.MAIN_LOOP_SLEEP)

    @classmethod
    async def _ping_loop(cls):
        while True:
            await asyncio.sleep_ms(config.MQTT_MANAGER_PING_INTERVAL)
            cls._mqtt.ping()

    @classmethod
    def _on_message(cls, _, msg):
        message = MQTTMessage.from_dict(msg)
        if message.action == "publish_status":
            cls._handle_publish_status(message.data)
        else:
            print(f"Unknown action: {message.action}")

    @classmethod
    def _handle_publish_status(cls, data):
        if not data:
            return

        timestamp = DBManager.get().get_date_time()

        DBManager.get().write_row("reading", "id", {
            "id": DBManager.generate_id(),
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "gas_value": data.get("gas_value"),
            "fan_on": data.get("fan_on"),
            "timestamp": timestamp,
        })
        keys = DBManager.get().get_table_keys("reading")
        for key in keys[:max(0, len(keys) - config.READING_HISTORY_LIMIT)]:
            DBManager.get().delete_row("reading", key)

        fan_on = data.get("fan_on")
        if fan_on and not cls._fan_on:
            DBManager.get().write_row("log", "id", {
                "id": DBManager.generate_id(),
                "temperature": data.get("temperature"),
                "humidity": data.get("humidity"),
                "gas_value": data.get("gas_value"),
                "timestamp": timestamp,
            })
        cls._fan_on = fan_on

        DBManager.get().commit()

        async def broadcast():
            message = json.dumps(data)
            for socket in list(cls._clients):
                try:
                    await socket.send(message)
                except Exception:
                    cls._clients.discard(socket)
        asyncio.create_task(broadcast())


if __name__ == "__main__":
    Main.run()
