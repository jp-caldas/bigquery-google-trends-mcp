from unittest.mock import patch

from mcp_google_trends.server import mcp


class TestServer:
    def test_server_instance_is_created(self):
        assert mcp.name == "Google Trends"

    def test_tools_are_registered(self):
        tools = mcp._tool_manager.list_tools()
        tool_names = {t.name for t in tools}
        assert "buscar_termos_em_alta_tool" in tool_names
        assert "buscar_termos_emergentes_tool" in tool_names
        assert "comparar_termo_tool" in tool_names

    @patch("mcp_google_trends.server.config.validate")
    @patch("mcp_google_trends.server.create_client")
    def test_lifespan_creates_client(self, mock_create_client, mock_validate):
        from mcp_google_trends.server import lifespan

        async def run():
            async with lifespan(mcp) as _:
                mock_create_client.assert_called_once()

        import asyncio

        asyncio.run(run())
