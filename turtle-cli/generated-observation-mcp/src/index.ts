import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { fleet_session_observer } from './tools/fleet_session_observer.js';
import { fleet_command_interceptor } from './tools/fleet_command_interceptor.js';
import { session_state_monitor } from './tools/session_state_monitor.js';

class GENERATED_MCP_SERVERServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "generated-mcp-server",
        version: "0.1.0",
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "fleet_session_observer",
            description: "Observe and log all Top Turtle interactions with fleet interface",
            inputSchema: {
              type: "object",
              properties: {
                session_id: {
                  type: "string",
                  description: "Unique identifier for interaction session"
                },
                log_level: {
                  type: "string",
                  description: "Verbosity level for observation logging"
                },
                real_time: {
                  type: "boolean",
                  description: "Enable real-time observation streaming"
                }
              },
              required: ["session_id"]
            },
          },
          {
            name: "fleet_command_interceptor",
            description: "Intercept and analyze Top Turtle commands before fleet execution",
            inputSchema: {
              type: "object",
              properties: {
                command: {
                  type: "string",
                  description: "Raw command input from Top Turtle"
                },
                context: {
                  type: "object",
                  description: "Current session and system context"
                }
              },
              required: ["command"]
            },
          },
          {
            name: "session_state_monitor",
            description: "Monitor complete session state for continuous observability",
            inputSchema: {
              type: "object",
              properties: {
                monitor_interval: {
                  type: "number",
                  description: "State check frequency in seconds"
                },
                state_depth: {
                  type: "string",
                  description: "Level of detail in state monitoring"
                }
              },
              required: []
            },
          }
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case "fleet_session_observer":
          return await fleet_session_observer(request.params.arguments ?? {});
        case "fleet_command_interceptor":
          return await fleet_command_interceptor(request.params.arguments ?? {});
        case "session_state_monitor":
          return await session_state_monitor(request.params.arguments ?? {});
        default:
          throw new Error(`Unknown tool: ${request.params.name}`);
      }
    });
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('generated-mcp-server MCP server running on stdio');
  }
}

const server = new GENERATED_MCP_SERVERServer();
server.run().catch(console.error);