import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { terminal_observer } from './tools/terminal_observer.js';
import { terminal_commander } from './tools/terminal_commander.js';
import { terminal_manager } from './tools/terminal_manager.js';

class TURTLE_TERMINAL_CONTROLServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "turtle-terminal-control",
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
            name: "terminal_observer",
            description: "Observe running processes in terminals and capture output",
            inputSchema: {
              type: "object",
              properties: {
                terminal_id: {
                  type: "string",
                  description: "Identifier for specific terminal session"
                },
                filter_pattern: {
                  type: "string",
                  description: "Regex pattern to filter output lines"
                },
                follow: {
                  type: "boolean",
                  description: "Continuously monitor new output"
                }
              },
              required: ["terminal_id"]
            },
          },
          {
            name: "terminal_commander",
            description: "Send commands to specific terminal sessions",
            inputSchema: {
              type: "object",
              properties: {
                terminal_id: {
                  type: "string",
                  description: "Target terminal identifier"
                },
                command: {
                  type: "string",
                  description: "Command to execute"
                },
                wait_for_completion: {
                  type: "boolean",
                  description: "Block until command finishes"
                },
                timeout_ms: {
                  type: "number",
                  description: "Maximum wait time in milliseconds"
                }
              },
              required: ["terminal_id", "command"]
            },
          },
          {
            name: "terminal_manager",
            description: "Create, list, and manage terminal sessions",
            inputSchema: {
              type: "object",
              properties: {
                action: {
                  type: "string",
                  description: "create/list/close/switch"
                },
                terminal_id: {
                  type: "string",
                  description: "Target terminal for close/switch actions"
                },
                working_directory: {
                  type: "string",
                  description: "Initial directory for new terminals"
                },
                shell: {
                  type: "string",
                  description: "Shell type (bash/zsh/fish) for new terminals"
                }
              },
              required: ["action"]
            },
          }
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case "terminal_observer":
          return await terminal_observer(request.params.arguments ?? {});
        case "terminal_commander":
          return await terminal_commander(request.params.arguments ?? {});
        case "terminal_manager":
          return await terminal_manager(request.params.arguments ?? {});
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
    console.error('turtle-terminal-control MCP server running on stdio');
  }
}

const server = new TURTLE_TERMINAL_CONTROLServer();
server.run().catch(console.error);