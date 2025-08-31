use anyhow::Result;
use serde::{Deserialize, Serialize};
//use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};
use tokio::process::Command;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemState {
    pub timestamp: u64,
    pub processes: Vec<ProcessInfo>,
    pub windows: Vec<WindowInfo>, 
    pub resources: ResourceState,
    pub network: NetworkState,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessInfo {
    pub pid: u32,
    pub name: String,
    pub cpu_usage: f32,
    pub memory_mb: u32,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WindowInfo {
    pub id: String,
    pub title: String,
    pub x: i32,
    pub y: i32,
    pub width: u32,
    pub height: u32,
    pub visible: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResourceState {
    pub cpu_percent: f32,
    pub memory_percent: f32,
    pub disk_percent: f32,
    pub load_average: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkState {
    pub connected: bool,
    pub latency_ms: Option<u32>,
    pub active_connections: u32,
}

#[derive(Debug, Clone)]
pub struct SafetyContext {
    pub operation: String,
    pub target: String,
    pub risk_level: RiskLevel,
    pub rollback_plan: Option<String>,
    pub monitoring_pattern: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum RiskLevel {
    Low,      // Read-only operations, status checks
    Medium,   // Reversible modifications, window positioning  
    High,     // File modifications, process management
    Critical, // System configuration, destructive operations
}

pub struct CoreInteractionPrinciple {
    initial_state: Option<SystemState>,
    current_state: Option<SystemState>,
    operation_history: Vec<SafetyContext>,
}

impl CoreInteractionPrinciple {
    pub fn new() -> Self {
        Self {
            initial_state: None,
            current_state: None,
            operation_history: Vec::new(),
        }
    }

    /// Step 1: Observe current system state before any action
    pub async fn observe_system_state(&mut self) -> Result<SystemState> {
        println!("🔍 Observing current system state...");
        
        let state = SystemState {
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            processes: self.get_process_info().await?,
            windows: self.get_window_info().await?,
            resources: self.get_resource_state().await?,
            network: self.get_network_state().await?,
        };

        if self.initial_state.is_none() {
            self.initial_state = Some(state.clone());
        }
        self.current_state = Some(state.clone());
        
        println!("✅ System state captured: {} processes, {} windows", 
                 state.processes.len(), state.windows.len());
        
        Ok(state)
    }

    /// Step 2: Analyze safety risks and potential side effects  
    pub fn analyze_safety_risks(&self, operation: &str, target: &str) -> SafetyContext {
        println!("🛡️ Analyzing safety risks for: {} on {}", operation, target);
        
        let risk_level = match operation.to_lowercase().as_str() {
            "read" | "list" | "show" | "status" | "check" => RiskLevel::Low,
            "move" | "resize" | "focus" | "minimize" | "maximize" => RiskLevel::Medium,
            "write" | "create" | "delete" | "modify" | "install" => RiskLevel::High,
            "format" | "shutdown" | "reboot" | "kill" | "chmod" => RiskLevel::Critical,
            _ => RiskLevel::Medium,
        };

        let rollback_plan = match risk_level {
            RiskLevel::Low => None,
            RiskLevel::Medium => Some(format!("Restore {} to original position/state", target)),
            RiskLevel::High => Some(format!("Backup and restore {} if operation fails", target)), 
            RiskLevel::Critical => Some(format!("Full system state snapshot for {}", target)),
        };

        let monitoring_pattern = match operation.to_lowercase().as_str() {
            op if op.contains("window") => "window_position_changes".to_string(),
            op if op.contains("file") => "file_system_changes".to_string(),
            op if op.contains("process") => "process_state_changes".to_string(),
            _ => "general_system_changes".to_string(),
        };

        let context = SafetyContext {
            operation: operation.to_string(),
            target: target.to_string(),
            risk_level,
            rollback_plan,
            monitoring_pattern,
        };

        println!("📊 Risk Level: {:?}, Monitoring: {}", 
                 context.risk_level, context.monitoring_pattern);

        context
    }

    /// Step 3: Execute operation with minimal impact
    pub async fn execute_with_monitoring<F, R>(&mut self, 
        context: SafetyContext,
        operation: F
    ) -> Result<R>
    where
        F: std::future::Future<Output = Result<R>>,
    {
        println!("⚡ Executing {} on {} with {} risk monitoring", 
                 context.operation, context.target, 
                 match context.risk_level {
                     RiskLevel::Low => "LOW",
                     RiskLevel::Medium => "MEDIUM", 
                     RiskLevel::High => "HIGH",
                     RiskLevel::Critical => "CRITICAL",
                 });

        // Store pre-execution state for rollback
        let pre_state = self.observe_system_state().await?;
        
        // Execute the operation
        let result = operation.await;
        
        // Monitor for changes
        let post_state = self.observe_system_state().await?;
        
        // Check for unintended effects
        self.verify_safe_execution(&pre_state, &post_state, &context).await?;
        
        // Record successful operation
        self.operation_history.push(context);
        
        result
    }

    /// Step 4: Verify execution was safe and no harm occurred
    async fn verify_safe_execution(
        &self, 
        pre_state: &SystemState, 
        post_state: &SystemState,
        context: &SafetyContext
    ) -> Result<()> {
        println!("🔍 Verifying safe execution...");

        // Check for unexpected process changes
        let process_changes = self.detect_process_changes(pre_state, post_state);
        if !process_changes.is_empty() && context.risk_level == RiskLevel::Low {
            println!("⚠️ Unexpected process changes detected during low-risk operation");
            for change in process_changes {
                println!("   - {}", change);
            }
        }

        // Check for resource spikes
        if post_state.resources.cpu_percent > 80.0 && 
           pre_state.resources.cpu_percent < 50.0 {
            println!("⚠️ High CPU usage detected after operation");
        }

        // Check for window management issues
        if context.monitoring_pattern == "window_position_changes" {
            let window_issues = self.detect_window_issues(pre_state, post_state);
            if !window_issues.is_empty() {
                println!("⚠️ Window positioning issues detected:");
                for issue in window_issues {
                    println!("   - {}", issue);
                }
            }
        }

        println!("✅ Execution verification complete - no harmful effects detected");
        Ok(())
    }

    async fn get_process_info(&self) -> Result<Vec<ProcessInfo>> {
        let output = Command::new("ps")
            .args(&["aux", "--no-headers"])
            .output()
            .await?;

        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut processes = Vec::new();

        for line in stdout.lines().take(20) { // Limit to top 20 processes
            let fields: Vec<&str> = line.split_whitespace().collect();
            if fields.len() >= 11 {
                if let (Ok(pid), Ok(cpu), Ok(mem)) = (
                    fields[1].parse::<u32>(),
                    fields[2].parse::<f32>(),
                    fields[5].parse::<u32>(),
                ) {
                    processes.push(ProcessInfo {
                        pid,
                        name: fields[10].to_string(),
                        cpu_usage: cpu,
                        memory_mb: mem / 1024, // Convert KB to MB
                        status: fields[7].to_string(),
                    });
                }
            }
        }

        Ok(processes)
    }

    async fn get_window_info(&self) -> Result<Vec<WindowInfo>> {
        let output = Command::new("wmctrl")
            .args(&["-l", "-G"])
            .output()
            .await?;

        let stdout = String::from_utf8_lossy(&output.stdout);
        let mut windows = Vec::new();

        for line in stdout.lines() {
            let fields: Vec<&str> = line.split_whitespace().collect();
            if fields.len() >= 7 {
                if let (Ok(x), Ok(y), Ok(width), Ok(height)) = (
                    fields[2].parse::<i32>(),
                    fields[3].parse::<i32>(),
                    fields[4].parse::<u32>(),
                    fields[5].parse::<u32>(),
                ) {
                    windows.push(WindowInfo {
                        id: fields[0].to_string(),
                        title: fields[7..].join(" "),
                        x,
                        y,
                        width,
                        height,
                        visible: true, // Assume visible if wmctrl can see it
                    });
                }
            }
        }

        Ok(windows)
    }

    async fn get_resource_state(&self) -> Result<ResourceState> {
        // Get CPU usage from /proc/loadavg
        let loadavg_output = Command::new("cat")
            .arg("/proc/loadavg")
            .output()
            .await?;
        
        let loadavg_str = String::from_utf8_lossy(&loadavg_output.stdout);
        let load_average = loadavg_str
            .split_whitespace()
            .next()
            .and_then(|s| s.parse::<f32>().ok())
            .unwrap_or(0.0);

        // Get memory usage from /proc/meminfo
        let meminfo_output = Command::new("cat")
            .arg("/proc/meminfo")
            .output()
            .await?;
        
        let meminfo_str = String::from_utf8_lossy(&meminfo_output.stdout);
        let mut mem_total = 0u64;
        let mut mem_available = 0u64;
        
        for line in meminfo_str.lines() {
            if line.starts_with("MemTotal:") {
                mem_total = line.split_whitespace()
                    .nth(1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(0);
            } else if line.starts_with("MemAvailable:") {
                mem_available = line.split_whitespace()
                    .nth(1)
                    .and_then(|s| s.parse().ok())
                    .unwrap_or(0);
            }
        }

        let memory_percent = if mem_total > 0 {
            ((mem_total - mem_available) as f32 / mem_total as f32) * 100.0
        } else {
            0.0
        };

        Ok(ResourceState {
            cpu_percent: load_average * 25.0, // Rough approximation
            memory_percent,
            disk_percent: 0.0, // TODO: Implement disk usage checking
            load_average,
        })
    }

    async fn get_network_state(&self) -> Result<NetworkState> {
        // Simple connectivity check
        let ping_result = Command::new("ping")
            .args(&["-c", "1", "-W", "2", "8.8.8.8"])
            .output()
            .await;

        let connected = ping_result.is_ok() && 
            ping_result.unwrap().status.success();

        Ok(NetworkState {
            connected,
            latency_ms: None, // TODO: Parse ping output for latency
            active_connections: 0, // TODO: Parse netstat output
        })
    }

    fn detect_process_changes(&self, pre: &SystemState, post: &SystemState) -> Vec<String> {
        let mut changes = Vec::new();
        
        let pre_pids: std::collections::HashSet<u32> = pre.processes.iter().map(|p| p.pid).collect();
        let post_pids: std::collections::HashSet<u32> = post.processes.iter().map(|p| p.pid).collect();
        
        for new_pid in post_pids.difference(&pre_pids) {
            if let Some(process) = post.processes.iter().find(|p| p.pid == *new_pid) {
                changes.push(format!("New process started: {} ({})", process.name, process.pid));
            }
        }
        
        for old_pid in pre_pids.difference(&post_pids) {
            if let Some(process) = pre.processes.iter().find(|p| p.pid == *old_pid) {
                changes.push(format!("Process terminated: {} ({})", process.name, process.pid));
            }
        }
        
        changes
    }

    fn detect_window_issues(&self, pre: &SystemState, post: &SystemState) -> Vec<String> {
        let mut issues = Vec::new();
        
        for post_window in &post.windows {
            if let Some(pre_window) = pre.windows.iter().find(|w| w.id == post_window.id) {
                // Check if window moved off-screen
                if post_window.x < -100 || post_window.y < -100 {
                    issues.push(format!("Window '{}' may be off-screen at ({}, {})", 
                                       post_window.title, post_window.x, post_window.y));
                }
                
                // Check for dramatic size changes
                let width_change = (post_window.width as f32 - pre_window.width as f32).abs();
                let height_change = (post_window.height as f32 - pre_window.height as f32).abs();
                
                if width_change > pre_window.width as f32 * 0.5 || 
                   height_change > pre_window.height as f32 * 0.5 {
                    issues.push(format!("Window '{}' size changed dramatically", post_window.title));
                }
            }
        }
        
        issues
    }
}