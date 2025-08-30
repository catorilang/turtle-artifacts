use anyhow::Result;
use clap::{Parser, Subcommand};
use std::time::Duration;
use tokio::time::sleep;

mod dashboard;
mod work;
mod system;
mod types;

use dashboard::Dashboard;
use types::*;

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
            // Default behavior - transform: pre-boot→standard or standard→secure_enclave
            turtle_mode_transition().await?;
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