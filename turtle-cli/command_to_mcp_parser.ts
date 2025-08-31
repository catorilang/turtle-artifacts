#!/usr/bin/env node

/**
 * Command to MCP Parser
 * Transforms natural language commands into MCP tool calls
 * Example: "open slack on the top third of my second monitor" → MCP call
 */

interface MCPToolCall {
  tool: string;
  server: string;
  parameters: Record<string, any>;
}

interface CommandPattern {
  pattern: RegExp;
  handler: (matches: RegExpMatchArray) => MCPToolCall;
}

class CommandToMCPParser {
  private patterns: CommandPattern[] = [];

  constructor() {
    this.initializePatterns();
  }

  private initializePatterns(): void {
    // Window management patterns
    this.addPattern(
      /open\s+(\w+)\s+on\s+(?:the\s+)?(\w+(?:-\w+)?)\s+of\s+(?:my\s+)?(\w+)\s+monitor/i,
      (matches) => ({
        tool: "window_launcher",
        server: "turtle-window-control",
        parameters: {
          application: matches[1].toLowerCase(),
          position: matches[2].toLowerCase(),
          monitor: this.parseMonitorReference(matches[3])
        }
      })
    );

    this.addPattern(
      /move\s+(\w+)\s+to\s+(\w+(?:\s+\w+)?)\s+(?:of\s+)?(?:monitor\s+)?(\d+)?/i,
      (matches) => ({
        tool: "window_controller", 
        server: "turtle-window-control",
        parameters: {
          application_name: matches[1].toLowerCase(),
          action: "move",
          position: matches[2].toLowerCase().replace(/\s+/g, '-'),
          monitor: matches[3] ? parseInt(matches[3]) : undefined
        }
      })
    );

    this.addPattern(
      /show\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?monitors?/i,
      () => ({
        tool: "monitor_detector",
        server: "turtle-window-control", 
        parameters: {
          list_all: true
        }
      })
    );

    this.addPattern(
      /(?:arrange|setup|organize)\s+(\w+)\s+layout/i,
      (matches) => ({
        tool: "workspace_organizer",
        server: "turtle-window-control",
        parameters: {
          layout: matches[1].toLowerCase(),
          applications: [] // Will be populated by workspace organizer
        }
      })
    );

    // Terminal control patterns
    this.addPattern(
      /(?:watch|monitor|observe)\s+terminal\s+(\w+)/i,
      (matches) => ({
        tool: "terminal_observer",
        server: "turtle-terminal-control",
        parameters: {
          terminal_id: matches[1],
          follow: true
        }
      })
    );

    this.addPattern(
      /run\s+(.+)\s+in\s+terminal\s+(\w+)/i,
      (matches) => ({
        tool: "terminal_commander", 
        server: "turtle-terminal-control",
        parameters: {
          terminal_id: matches[2],
          command: matches[1].trim(),
          wait_for_completion: false
        }
      })
    );

    // Generic application launching
    this.addPattern(
      /(?:open|launch|start)\s+(\w+)/i,
      (matches) => ({
        tool: "window_launcher",
        server: "turtle-window-control", 
        parameters: {
          application: matches[1].toLowerCase()
        }
      })
    );
  }

  private addPattern(pattern: RegExp, handler: (matches: RegExpMatchArray) => MCPToolCall): void {
    this.patterns.push({ pattern, handler });
  }

  private parseMonitorReference(ref: string): number {
    const lowerRef = ref.toLowerCase();
    switch (lowerRef) {
      case 'first':
      case 'primary':
      case 'main':
        return 0;
      case 'second':
      case 'secondary':
        return 1;
      case 'third':
        return 2;
      case 'fourth':
        return 3;
      default:
        // Try to parse as number
        const num = parseInt(ref);
        return isNaN(num) ? 0 : Math.max(0, num - 1); // Convert 1-based to 0-based
    }
  }

  parseCommand(command: string): MCPToolCall | null {
    const cleanCommand = command.trim();
    
    for (const { pattern, handler } of this.patterns) {
      const matches = cleanCommand.match(pattern);
      if (matches) {
        console.log(\`🎯 Matched pattern: \${pattern}\`);
        console.log(\`📝 Command: "\${cleanCommand}"\`);
        
        const toolCall = handler(matches);
        console.log(\`🔧 Generated MCP call:\`, JSON.stringify(toolCall, null, 2));
        
        return toolCall;
      }
    }
    
    console.log(\`❓ No pattern matched for: "\${cleanCommand}"\`);
    return null;
  }

  async executeMCPCall(toolCall: MCPToolCall): Promise<any> {
    console.log(\`🚀 Executing MCP call to \${toolCall.server}.\${toolCall.tool}\`);
    
    // In a real implementation, this would:
    // 1. Connect to the MCP server
    // 2. Call the tool with parameters
    // 3. Return the result
    
    // For demonstration, return a mock result
    return {
      success: true,
      tool: toolCall.tool,
      server: toolCall.server,
      parameters: toolCall.parameters,
      result: \`Mock execution of \${toolCall.tool} with params: \${JSON.stringify(toolCall.parameters)}\`
    };
  }

  async processCommand(command: string): Promise<any> {
    console.log(\`\\n🐢 Processing command: "\${command}"\`);
    
    const toolCall = this.parseCommand(command);
    if (!toolCall) {
      return { error: "Could not parse command into MCP tool call" };
    }
    
    return await this.executeMCPCall(toolCall);
  }
}

// CLI interface and testing
if (import.meta.url === \`file://\${process.argv[1]}\`) {
  const parser = new CommandToMCPParser();
  
  // Test commands
  const testCommands = [
    "open slack on the top third of my second monitor",
    "move terminal to left half of monitor 1", 
    "show me all my monitors",
    "arrange development layout",
    "watch terminal main",
    "run npm start in terminal dev",
    "open firefox"
  ];
  
  console.log("🧪 Testing Command to MCP Parser\\n");
  
  for (const command of testCommands) {
    const result = await parser.processCommand(command);
    console.log(\`✅ Result:\`, result);
    console.log("".repeat(50));
  }
}

export { CommandToMCPParser };