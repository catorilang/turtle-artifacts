import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { window_launcher } from './tools/window_launcher.js';
import { window_controller } from './tools/window_controller.js';
import { monitor_detector } from './tools/monitor_detector.js';
import { workspace_organizer } from './tools/workspace_organizer.js';

class TURTLE_WINDOW_CONTROLServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "turtle-window-control",
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
            name: "window_launcher",
            description: "Launch applications with specific window positioning",
            inputSchema: {
              type: "object",
              properties: {
                application: {
                  type: "string",
                  description: "Application name or executable path"
                },
                monitor: {
                  type: "number",
                  description: "Target monitor number (0-based index)"
                },
                position: {
                  type: "string",
                  description: "Window position: top-third, bottom-third, left-half, right-half, maximize, minimize"
                },
                width_percent: {
                  type: "number",
                  description: "Window width as percentage of monitor"
                },
                height_percent: {
                  type: "number",
                  description: "Window height as percentage of monitor"
                },
                x_offset: {
                  type: "number",
                  description: "Horizontal pixel offset from calculated position"
                },
                y_offset: {
                  type: "number",
                  description: "Vertical pixel offset from calculated position"
                }
              },
              required: ["application"]
            },
          },
          {
            name: "window_controller",
            description: "Move, resize, and control existing windows",
            inputSchema: {
              type: "object",
              properties: {
                window_id: {
                  type: "string",
                  description: "Target window identifier"
                },
                application_name: {
                  type: "string",
                  description: "Find window by application name"
                },
                action: {
                  type: "string",
                  description: "move, resize, close, minimize, maximize, focus"
                },
                monitor: {
                  type: "number",
                  description: "Target monitor for move operations"
                },
                position: {
                  type: "string",
                  description: "New position specification"
                },
                width: {
                  type: "number",
                  description: "New window width in pixels"
                },
                height: {
                  type: "number",
                  description: "New window height in pixels"
                }
              },
              required: ["action"]
            },
          },
          {
            name: "monitor_detector",
            description: "Detect and analyze available monitors and their geometry",
            inputSchema: {
              type: "object",
              properties: {
                list_all: {
                  type: "boolean",
                  description: "List all available monitors"
                },
                monitor_id: {
                  type: "number",
                  description: "Get details for specific monitor"
                }
              },
              required: []
            },
          },
          {
            name: "workspace_organizer",
            description: "Organize multiple applications across monitors and positions",
            inputSchema: {
              type: "object",
              properties: {
                layout: {
                  type: "string",
                  description: "Predefined layout name or custom arrangement"
                },
                applications: {
                  type: "array",
                  description: "List of applications to organize"
                },
                save_layout: {
                  type: "boolean",
                  description: "Save this arrangement for future use"
                },
                restore_layout: {
                  type: "string",
                  description: "Restore previously saved layout"
                }
              },
              required: ["layout", "applications"]
            },
          }
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
        case "window_launcher":
          return await window_launcher(request.params.arguments ?? {});
        case "window_controller":
          return await window_controller(request.params.arguments ?? {});
        case "monitor_detector":
          return await monitor_detector(request.params.arguments ?? {});
        case "workspace_organizer":
          return await workspace_organizer(request.params.arguments ?? {});
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
    console.error('turtle-window-control MCP server running on stdio');
  }
}

const server = new TURTLE_WINDOW_CONTROLServer();
server.run().catch(console.error);