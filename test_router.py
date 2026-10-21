"""Test de conectivitate, doar citire: nu modifică nimic pe router.

Folosește aceleași variabile de mediu ca server.py:
    python test_router.py
"""

import asyncio
import os

import aiohttp
from asusrouter import AsusData, AsusRouter


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        router = AsusRouter(
            hostname=os.environ.get("ROUTER_HOST", "192.168.50.1"),
            username=os.environ.get("ROUTER_USER", "admin"),
            password=os.environ["ROUTER_PASS"],
            use_ssl=os.environ.get("ROUTER_SSL", "false").lower() == "true",
            session=session,
        )
        await router.async_connect()
        identity = await router.async_get_identity()
        print(f"Conectat: {identity.model}, firmware {identity.firmware}")

        clients = await router.async_get_data(AsusData.CLIENTS, force=True)
        for mac, client in clients.items():
            conn, desc = client.connection, client.description
            if conn and conn.online:
                print(f"{mac}  {conn.ip_address or '-':15}  {desc.name if desc else '-'}")

        pc = await router.async_get_data(AsusData.PARENTAL_CONTROL, force=True)
        print(f"Parental Controls: {pc.get('state')}, reguli: {len(pc.get('rules') or {})}")
        await router.async_disconnect()


asyncio.run(main())
