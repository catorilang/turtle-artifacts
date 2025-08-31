use anyhow::Result;
use clap::{Parser, Subcommand};
use std::io::{self, Write};
use chrono::Timelike;
use tokio::io::{AsyncBufReadExt, BufReader};

pub mod dashboard;
pub mod work;
pub mod system;
pub mod types;
pub mod claude;
pub mod safety;
pub mod command_parser;
pub mod cnl_config;

use dashboard::Dashboard;
use types::*;
// use safety::{CoreInteractionPrinciple, SafetyContext, RiskLevel};
use command_parser::CNLCommandParser;
use cnl_config::{CNLConfigLoader, TurtleFleetConfig};

#[derive(Parser)]
#[command(name = "turtle")]
#[command(about = "🐢 Turtle: Distributed productivity and infrastructure management")]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// Show work dashboard
    Work {
        #[command(subcommand)]
        work_command: Option<WorkCommands>,
    },
    /// Quick status view
    #[clap(alias = "w")]
    Status,
    /// Infrastructure monitoring
    Infra,
    /// Show full dashboard
    Dashboard,
}

#[derive(Subcommand)]
enum WorkCommands {
    /// Focus mode
    Focus { duration: Option<String> },
    /// Calendar view
    Calendar,
    /// Task management
    Tasks,
    /// Communications hub
    Comms,
    /// Infrastructure monitoring
    Infra,
    /// Meeting preparation
    #[clap(alias = "prep")]
    Meeting,
    /// End of day summary
    Eod,
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Some(Commands::Work { work_command }) => {
            handle_work_commands(work_command).await?;
        }
        Some(Commands::Status) => {
            show_quick_status().await?;
        }
        Some(Commands::Infra) => {
            show_infrastructure_status().await?;
        }
        Some(Commands::Dashboard) => {
            show_full_dashboard().await?;
        }
        None => {
            // Default behavior - conversational REPL mode
            repl_mode().await?;
        }
    }

    Ok(())
}

async fn handle_work_commands(work_command: Option<WorkCommands>) -> Result<()> {
    match work_command {
        Some(WorkCommands::Focus { duration }) => {
            work::focus_mode(duration).await?;
        }
        Some(WorkCommands::Calendar) => {
            work::show_calendar().await?;
        }
        Some(WorkCommands::Tasks) => {
            work::show_tasks().await?;
        }
        Some(WorkCommands::Comms) => {
            work::show_communications().await?;
        }
        Some(WorkCommands::Infra) => {
            work::show_infrastructure().await?;
        }
        Some(WorkCommands::Meeting) => {
            work::meeting_prep().await?;
        }
        Some(WorkCommands::Eod) => {
            work::end_of_day().await?;
        }
        None => {
            show_work_dashboard().await?;
        }
    }
    Ok(())
}

async fn show_quick_status() -> Result<()> {
    let mut dashboard = Dashboard::new().await?;
    dashboard.show_compact().await?;
    Ok(())
}

async fn show_work_dashboard() -> Result<()> {
    let mut dashboard = Dashboard::new().await?;
    dashboard.show_work_focused().await?;
    Ok(())
}

async fn show_full_dashboard() -> Result<()> {
    let mut dashboard = Dashboard::new().await?;
    dashboard.show_expanded().await?;
    Ok(())
}

async fn show_infrastructure_status() -> Result<()> {
    let mut dashboard = Dashboard::new().await?;
    dashboard.show_infrastructure_focused().await?;
    Ok(())
}

async fn repl_mode() -> Result<()> {
    // Initialize enhanced command parser with Core Interaction Principle
    let mut command_parser = CNLCommandParser::new();
    
    // Detect Claude availability
    let claude_client = claude::Claude::new();
    let has_claude = claude_client.is_some();
    
    println!("🐢 Smart Turtle Fleet Interface - Top Turtle Interactive Session");
    if has_claude {
        println!("🤖 Claude integration active - Fleet intelligence enhanced");
    } else {
        println!("💡 Tip: Set ANTHROPIC_API_KEY for full fleet intelligence");
    }
    println!("🛡️ All operations protected by Core Interaction Principle");
    println!("🌐 Connecting to turtle fleet infrastructure...");
    
    // Fleet discovery and connection
    let fleet_status = discover_turtle_fleet().await?;
    println!("📡 Fleet Status: {}", fleet_status);
    
    // Smart startup: auto-detect what's needed with safety observation
    let startup_context = detect_startup_context().await?;
    match startup_context {
        StartupContext::WorkTime => {
            println!("🎯 Good morning! Starting work mode...");
            show_work_dashboard().await?;
        }
        StartupContext::InfraIssues => {
            println!("⚠️ Infrastructure issues detected. Showing infra status...");
            show_infrastructure_status().await?;
        }
        StartupContext::General => {
            println!("📊 Starting with status overview...");
            show_quick_status().await?;
        }
    }
    
    if has_claude {
        println!("\n💬 Smart Turtle Fleet at your service, Top Turtle! 28 turtles ready for your commands!");
        println!("   Try: 'coordinate fleet status', 'deploy across DCs', or any complex operation");
    } else {
        println!("\n💬 Smart Turtle Fleet ready - local intelligence active!");
        println!("   Try: 'fleet status', 'help', or describe what you want the fleet to do");
    }
    
    let stdin = tokio::io::stdin();
    let mut reader = BufReader::new(stdin);
    
    loop {
        print!("🐢 ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        match reader.read_line(&mut input).await {
            Ok(0) => {
                // EOF reached
                println!("🐢 See you later!");
                break;
            }
            Ok(_) => {},
            Err(e) => {
                println!("Error reading input: {}", e);
                continue;
            }
        }
        let input = input.trim();
        
        match input {
            "" => continue,
            input if is_exit_command(input) => {
                println!("🐢 See you later!");
                break;
            }
            input => {
                // Parse command using CNL patterns with Core Interaction Principle
                match command_parser.parse_command(input).await {
                    Ok(parsed_command) => {
                        match command_parser.execute_command(parsed_command).await {
                            Ok(response) => println!("🐢 {}", response),
                            Err(e) => println!("❌ Error: {}", e),
                        }
                    }
                    Err(e) => {
                        println!("🤔 Could not parse command: {}", e);
                        // Fallback to Claude or smart input handling
                        if let Some(ref claude) = claude_client {
                            handle_claude_input(input, claude).await?;
                        } else {
                            handle_smart_input(input).await?;
                        }
                    }
                }
            }
        }
    }
    
    Ok(())
}

#[derive(Debug)]
enum StartupContext {
    WorkTime,
    InfraIssues, 
    General,
}

async fn detect_startup_context() -> Result<StartupContext> {
    use chrono::Local;
    let hour = Local::now().hour();
    
    // Work hours: 8 AM to 6 PM
    if hour >= 8 && hour < 18 {
        Ok(StartupContext::WorkTime)
    } else {
        Ok(StartupContext::General)
    }
}

fn is_exit_command(input: &str) -> bool {
    matches!(input.to_lowercase().as_str(), 
        "exit" | "quit" | "bye" | "goodbye" | "done")
}

async fn handle_smart_input(input: &str) -> Result<()> {
    let lower_input = input.to_lowercase();
    
    // Smart pattern matching for natural language
    if lower_input.contains("status") || lower_input.contains("how") || lower_input.contains("what's") {
        show_quick_status().await?;
    } else if lower_input.contains("work") || lower_input.contains("task") || lower_input.contains("todo") {
        show_work_dashboard().await?;
    } else if lower_input.contains("dashboard") || lower_input.contains("full") || lower_input.contains("everything") {
        show_full_dashboard().await?;
    } else if lower_input.contains("infra") || lower_input.contains("server") || lower_input.contains("deploy") {
        show_infrastructure_status().await?;
    } else if lower_input.contains("focus") || lower_input.contains("concentrate") {
        work::focus_mode(None).await?;
    } else if lower_input.contains("calendar") || lower_input.contains("schedule") || lower_input.contains("meeting") {
        work::show_calendar().await?;
    } else if lower_input.contains("transition") || lower_input.contains("change") || lower_input.contains("switch") {
        turtle_mode_transition().await?;
    } else if lower_input.contains("help") {
        show_smart_help();
    } else {
        // Intelligent response for unrecognized input
        println!("🤔 I understand you want: '{}'", input);
        println!("💡 Let me suggest what might help:");
        
        if lower_input.len() < 4 {
            show_quick_status().await?;
        } else if lower_input.contains("show") || lower_input.contains("see") {
            show_work_dashboard().await?;
        } else {
            println!("   - Try: 'status', 'work', 'dashboard', or 'help'");
            println!("   - Or just describe what you want to do");
        }
    }
    
    Ok(())
}

async fn handle_claude_input(input: &str, claude: &claude::Claude) -> Result<()> {
    // Try Claude first, fallback to built-in commands if Claude fails
    let context = get_current_context().await;
    
    match claude.chat(input, &context).await {
        Ok(response) => {
            println!("🤖 {}", response);
            
            // Check if Claude suggested an action we should take
            if should_execute_command(&response) {
                execute_suggested_command(&response).await?;
            }
        }
        Err(e) => {
            println!("⚠️ Claude unavailable: {}", e);
            println!("🔄 Falling back to built-in commands...");
            handle_smart_input(input).await?;
        }
    }
    
    Ok(())
}

async fn get_current_context() -> String {
    let hour = chrono::Local::now().hour();
    let time_context = if hour >= 8 && hour < 18 { "work hours" } else { "after hours" };
    
    format!(
        "Current time context: {}. \
        Available turtle functions: status dashboard, work dashboard, infrastructure monitoring, \
        focus mode, calendar, tasks. \
        The user has turtle fleet management and DC deployment capabilities.",
        time_context
    )
}

fn should_execute_command(response: &str) -> bool {
    response.to_lowercase().contains("showing") || 
    response.to_lowercase().contains("here's") ||
    response.to_lowercase().contains("let me show")
}

async fn execute_suggested_command(response: &str) -> Result<()> {
    let lower_response = response.to_lowercase();
    
    if lower_response.contains("status") {
        show_quick_status().await?;
    } else if lower_response.contains("work") {
        show_work_dashboard().await?;
    } else if lower_response.contains("dashboard") {
        show_full_dashboard().await?;
    } else if lower_response.contains("infrastructure") || lower_response.contains("infra") {
        show_infrastructure_status().await?;
    }
    
    Ok(())
}

fn show_smart_help() {
    println!("🐢 Smart Turtle Help - Just tell me what you want:");
    println!("   💬 Natural language:");
    println!("      'How are things?' → status");
    println!("      'Show me work stuff' → work dashboard"); 
    println!("      'What's the full picture?' → full dashboard");
    println!("      'How are the servers?' → infrastructure");
    println!("      'I need to focus' → focus mode");
    println!("   ⚡ Quick commands: status, work, dashboard, infra, focus, calendar");
    println!("   🚪 Exit: bye, exit, quit, done");
}

async fn discover_turtle_fleet() -> Result<String> {
    // Discover shared turtle infrastructure
    println!("🔍 Scanning for turtle fleet infrastructure...");
    
    let mut fleet_info = Vec::new();
    
    // Check for existing turtle processes
    if let Ok(output) = tokio::process::Command::new("pgrep")
        .args(&["-f", "turtle"])
        .output()
        .await 
    {
        let turtle_processes = String::from_utf8_lossy(&output.stdout)
            .lines()
            .count();
        if turtle_processes > 1 {
            fleet_info.push(format!("{} turtle processes discovered", turtle_processes));
        }
    }
    
    // Check for turtle infrastructure directories
    let infra_paths = [
        "/home/tupshin/turtle",
        "/home/tupshin/turtle-rust-private", 
        "/home/tupshin/turtle-ts-private",
        "/home/tupshin/.turtle"
    ];
    
    for path in infra_paths.iter() {
        if tokio::fs::metadata(path).await.is_ok() {
            fleet_info.push(format!("Turtle infrastructure: {}", path));
        }
    }
    
    // Check for network turtle services (common ports)
    // This could be expanded based on actual turtle fleet configuration
    
    if fleet_info.is_empty() {
        Ok("Fleet discovery in progress - smart turtle ready for coordination".to_string())
    } else {
        Ok(format!("🐢 {} - Ready for fleet coordination", fleet_info.join(" | ")))
    }
}

async fn turtle_mode_transition() -> Result<()> {
    println!("🐢 TURTLE MODE TRANSITION");
    println!("Transforming: pre-boot→standard or standard→secure_enclave");
    
    // Check current state and transition appropriately
    let current_state = system::get_turtle_state().await?;
    
    match current_state {
        TurtleState::PreBoot => {
            println!("🔄 Pre-boot → Standard mode transition");
            system::transition_to_standard().await?;
            show_quick_status().await?;
        }
        TurtleState::Standard => {
            println!("🔒 Standard → Secure enclave transition");
            system::transition_to_secure_enclave().await?;
            show_infrastructure_status().await?;
        }
        TurtleState::SecureEnclave => {
            println!("🛡️ Already in secure enclave mode");
            show_full_dashboard().await?;
        }
    }
    
    Ok(())
}