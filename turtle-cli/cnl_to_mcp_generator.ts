#!/usr/bin/env node

/**
 * CNL to MCP Generator
 * Transforms CNL specifications into functional MCP servers
 * Core protocol for universal observability
 */

import * as fs from 'node:fs';
import * as path from 'node:path';

interface ToolParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array';
  required: boolean;
  description: string;
}

interface ToolReturn {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'array';
  description: string;
}

interface ToolSpec {
  name: string;
  description: string;
  parameters: ToolParameter[];
  returns: ToolReturn[];
  implementationPattern: string;
}

interface MCPServerConfig {
  name: string;
  version: string;
  transport: string;
  capabilities: string[];
  tools: ToolSpec[];
}

class CNLToMCPGenerator {
  
  parseCNLFile(filePath: string): MCPServerConfig {
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // Parse TOOL_SPECIFICATION blocks
    const toolSpecs: ToolSpec[] = [];
    const toolMatches = content.matchAll(/TOOL_SPECIFICATION\s+(\w+):(.*?)(?=TOOL_SPECIFICATION|MCP_SERVER_CONFIGURATION|$)/gs);
    
    for (const match of toolMatches) {
      const toolName = match[1];
      const toolContent = match[2];
      
      const descMatch = toolContent.match(/DESCRIPTION:\s*"([^"]+)"/);
      const description = descMatch ? descMatch[1] : '';
      
      const parameters = this.parseParameters(toolContent);
      const returns = this.parseReturns(toolContent);
      const implMatch = toolContent.match(/IMPLEMENTATION_PATTERN:\s*"([^"]+)"/);
      const implementationPattern = implMatch ? implMatch[1] : '';
      
      toolSpecs.push({
        name: toolName,
        description,
        parameters,
        returns,
        implementationPattern
      });
    }
    
    // Parse MCP_SERVER_CONFIGURATION
    const configMatch = content.match(/MCP_SERVER_CONFIGURATION:(.*?)(?=GENERATION_RULES|$)/s);
    const configContent = configMatch ? configMatch[1] : '';
    
    const nameMatch = configContent.match(/NAME:\s*"([^"]+)"/);
    const versionMatch = configContent.match(/VERSION:\s*"([^"]+)"/);
    const transportMatch = configContent.match(/TRANSPORT:\s*"([^"]+)"/);
    
    return {
      name: nameMatch ? nameMatch[1] : 'generated-mcp-server',
      version: versionMatch ? versionMatch[1] : '0.1.0',
      transport: transportMatch ? transportMatch[1] : 'stdio',
      capabilities: ['tools', 'resources'],
      tools: toolSpecs
    };
  }
  
  private parseParameters(toolContent: string): ToolParameter[] {
    const parameters: ToolParameter[] = [];
    const paramSection = toolContent.match(/PARAMETERS:(.*?)RETURNS:/s);
    if (!paramSection) return parameters;
    
    const paramLines = paramSection[1].match(/- (\w+): (\w+) \((\w+)\) "([^"]+)"/g);
    if (!paramLines) return parameters;
    
    for (const line of paramLines) {
      const match = line.match(/- (\w+): (\w+) \((\w+)\) "([^"]+)"/);
      if (match) {
        parameters.push({
          name: match[1],
          type: match[2] as any,
          required: match[3] === 'required',
          description: match[4]
        });
      }
    }
    
    return parameters;
  }
  
  private parseReturns(toolContent: string): ToolReturn[] {
    const returns: ToolReturn[] = [];
    const returnSection = toolContent.match(/RETURNS:(.*?)IMPLEMENTATION_PATTERN:/s);
    if (!returnSection) return returns;
    
    const returnLines = returnSection[1].match(/- (\w+): (\w+) "([^"]+)"/g);
    if (!returnLines) return returns;
    
    for (const line of returnLines) {
      const match = line.match(/- (\w+): (\w+) "([^"]+)"/);
      if (match) {
        returns.push({
          name: match[1],
          type: match[2] as any,
          description: match[3]
        });
      }
    }
    
    return returns;
  }
  
  generateMCPServer(config: MCPServerConfig, outputDir: string): void {
    // Generate package.json
    this.generatePackageJson(config, outputDir);
    
    // Generate TypeScript server
    this.generateServerTypeScript(config, outputDir);
    
    // Generate tool implementations
    this.generateToolImplementations(config, outputDir);
    
    console.log(`🎯 Generated MCP server '${config.name}' in ${outputDir}`);
    console.log(`📦 Tools: ${config.tools.map(t => t.name).join(', ')}`);
  }
  
  private generatePackageJson(config: MCPServerConfig, outputDir: string): void {
    const packageJson = {
      name: config.name,
      version: config.version,
      description: `MCP server generated from CNL specification`,
      main: "dist/index.js",
      type: "module",
      scripts: {
        build: "tsc",
        start: "node dist/index.js",
        dev: "tsc --watch"
      },
      dependencies: {
        "@modelcontextprotocol/sdk": "^0.4.0"
      },
      devDependencies: {
        "@types/node": "^18.0.0",
        "typescript": "^5.0.0"
      }
    };
    
    fs.writeFileSync(
      path.join(outputDir, 'package.json'),
      JSON.stringify(packageJson, null, 2)
    );
  }
  
  private generateServerTypeScript(config: MCPServerConfig, outputDir: String): void {
    const serverCode = `
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

${config.tools.map(tool => `import { ${tool.name} } from './tools/${tool.name}.js';`).join('\n')}

class ${config.name.replace(/-/g, '_').toUpperCase()}Server {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "${config.name}",
        version: "${config.version}",
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
${config.tools.map(tool => `          {
            name: "${tool.name}",
            description: "${tool.description}",
            inputSchema: {
              type: "object",
              properties: {
${tool.parameters.map(param => `                ${param.name}: {
                  type: "${param.type}",
                  description: "${param.description}"
                }`).join(',\n')}
              },
              required: [${tool.parameters.filter(p => p.required).map(p => `"${p.name}"`).join(', ')}]
            },
          }`).join(',\n')}
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      switch (request.params.name) {
${config.tools.map(tool => `        case "${tool.name}":
          return await ${tool.name}(request.params.arguments ?? {});`).join('\n')}
        default:
          throw new Error(\`Unknown tool: \${request.params.name}\`);
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
    console.error('${config.name} MCP server running on stdio');
  }
}

const server = new ${config.name.replace(/-/g, '_').toUpperCase()}Server();
server.run().catch(console.error);
`;

    const srcDir = path.join(outputDir, 'src');
    if (!fs.existsSync(srcDir)) {
      fs.mkdirSync(srcDir, { recursive: true });
    }
    
    fs.writeFileSync(path.join(srcDir, 'index.ts'), serverCode.trim());
  }
  
  private generateToolImplementations(config: MCPServerConfig, outputDir: string): void {
    const toolsDir = path.join(outputDir, 'src', 'tools');
    if (!fs.existsSync(toolsDir)) {
      fs.mkdirSync(toolsDir, { recursive: true });
    }
    
    for (const tool of config.tools) {
      const toolCode = `
/**
 * ${tool.name} - ${tool.description}
 * Implementation Pattern: ${tool.implementationPattern}
 */

interface ${tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}Args {
${tool.parameters.map(param => `  ${param.name}${param.required ? '' : '?'}: ${param.type};`).join('\n')}
}

interface ${tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}Result {
${tool.returns.map(ret => `  ${ret.name}: ${ret.type};`).join('\n')}
}

export async function ${tool.name}(args: ${tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}Args): Promise<{ content: Array<{ type: 'text'; text: string }> }> {
  try {
    // TODO: Implement ${tool.implementationPattern}
    console.error(\`[${tool.name}] Called with args:, JSON.stringify(args, null, 2)\`);
    
    // Placeholder implementation
    const result: ${tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}Result = {
${tool.returns.map(ret => {
        switch (ret.type) {
          case 'string': return `      ${ret.name}: "placeholder_${ret.name}"`;
          case 'number': return `      ${ret.name}: 0`;
          case 'boolean': return `      ${ret.name}: false`;
          case 'array': return `      ${ret.name}: []`;
          default: return `      ${ret.name}: null`;
        }
      }).join(',\n')}
    };
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }
      ]
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: \`Error in ${tool.name}: \${error}\`
        }
      ]
    };
  }
}
`;
      
      fs.writeFileSync(path.join(toolsDir, `${tool.name}.ts`), toolCode.trim());
    }
  }
  
  generateTSConfig(outputDir: string): void {
    const tsConfig = {
      compilerOptions: {
        target: "ES2022",
        module: "ESNext",
        moduleResolution: "Node",
        outDir: "./dist",
        rootDir: "./src",
        strict: true,
        esModuleInterop: true,
        skipLibCheck: true,
        forceConsistentCasingInFileNames: true,
        declaration: true,
        declarationMap: true,
        sourceMap: true
      },
      include: ["src/**/*"],
      exclude: ["node_modules", "dist"]
    };
    
    fs.writeFileSync(
      path.join(outputDir, 'tsconfig.json'),
      JSON.stringify(tsConfig, null, 2)
    );
  }
}

// CLI interface
if (import.meta.url === `file://${process.argv[1]}`) {
  const [,, cnlFile, outputDir] = process.argv;
  
  if (!cnlFile || !outputDir) {
    console.error('Usage: node cnl_to_mcp_generator.js <cnl-file> <output-directory>');
    process.exit(1);
  }
  
  const generator = new CNLToMCPGenerator();
  
  try {
    console.log('🔧 Parsing CNL specification...');
    const config = generator.parseCNLFile(cnlFile);
    
    console.log('🏗️ Generating MCP server...');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    generator.generateMCPServer(config, outputDir);
    generator.generateTSConfig(outputDir);
    
    console.log('✅ CNL to MCP generation complete!');
    console.log('📋 Next steps:');
    console.log(`   cd ${outputDir}`);
    console.log('   npm install');
    console.log('   npm run build');
    console.log(`   claude mcp add ${config.name} node dist/index.js`);
    
  } catch (error) {
    console.error('❌ Generation failed:', error);
    process.exit(1);
  }
}

export { CNLToMCPGenerator };