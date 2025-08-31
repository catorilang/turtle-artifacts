use anyhow::Result;
use std::io::{self, Write};
use turtle::dashboard::Dashboard;
use turtle::work;
use turtle::system;

#[tokio::main]
async fn main() -> Result<()> {
    println!("🐢 Turtle REPL - Conversational Mode");
    println!("Type 'help' for commands, 'exit' to quit");
    
    loop {
        print!("turtle> ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();
        
        match input {
            "exit" | "quit" => {
                println!("🐢 Goodbye!");
                break;
            }
            "help" => {
                println!("Available commands:");
                println!("  status     - Show quick status");
                println!("  work       - Work dashboard");
                println!("  dashboard  - Full dashboard");
                println!("  infra      - Infrastructure view");
                println!("  transition - State transition");
                println!("  focus      - Enter focus mode");
                println!("  tasks      - Show tasks");
                println!("  calendar   - Show calendar");
                println!("  help       - This help");
                println!("  exit       - Quit turtle");
            }
            "status" => {
                let mut dashboard = Dashboard::new().await?;
                dashboard.show_compact().await?;
            }
            "work" => {
                let mut dashboard = Dashboard::new().await?;
                dashboard.show_work_focused().await?;
            }
            "dashboard" => {
                let mut dashboard = Dashboard::new().await?;
                dashboard.show_expanded().await?;
            }
            "infra" => {
                let mut dashboard = Dashboard::new().await?;
                dashboard.show_infrastructure_focused().await?;
            }
            "transition" => {
                let state = system::get_turtle_state().await?;
                println!("Current state: {:?}", state);
                system::transition_to_standard().await?;
            }
            "focus" => {
                work::focus_mode(None).await?;
            }
            "tasks" => {
                work::show_tasks().await?;
            }
            "calendar" => {
                work::show_calendar().await?;
            }
            "" => {
                // Empty input, just show prompt again
            }
            _ => {
                println!("🤔 Unknown command: '{}'. Type 'help' for available commands.", input);
            }
        }
    }
    
    Ok(())
}