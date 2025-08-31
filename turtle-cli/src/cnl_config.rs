use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct TurtleFleetConfig {
    pub fleet_discovery: FleetDiscoveryConfig,
    pub display_and_window: DisplayWindowConfig,
    pub claude_integration: ClaudeIntegrationConfig,
    pub fleet_communication: FleetCommunicationConfig,
    pub safety_and_authority: SafetyAuthorityConfig,
    pub mesh_resilience: MeshResilienceConfig,
    pub efficiency_optimization: EfficiencyOptimizationConfig,
    pub startup_behavior: StartupBehaviorConfig,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct FleetDiscoveryConfig {
    pub infrastructure_paths: Vec<String>,
    pub process_discovery_pattern: String,
    pub infrastructure_scan_timeout: u64,
    pub fleet_coordination_retry_count: u32,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct DisplayWindowConfig {
    pub monitors: Vec<MonitorConfig>,
    pub default_terminal_geometry: String,
    pub default_terminal_zoom: u32,
    pub center_offset: (i32, i32),
    pub window_fractions: WindowFractions,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MonitorConfig {
    pub index: u32,
    pub base_x: i32,
    pub base_y: i32,
    pub width: u32,
    pub height: u32,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct WindowFractions {
    pub top_third: f64,
    pub middle_third: f64,
    pub bottom_third: f64,
    pub left_half: f64,
    pub right_half: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ClaudeIntegrationConfig {
    pub model_name: String,
    pub max_tokens: u32,
    pub api_version: String,
    pub api_endpoint: String,
    pub system_prompt_template: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct FleetCommunicationConfig {
    pub fleet_size: u32,
    pub coordination_protocol: String,
    pub communication_pattern: String,
    pub discovery_interval: u64,
    pub health_check_interval: u64,
    pub mesh_ports: MeshPorts,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MeshPorts {
    pub discovery_port: u16,
    pub coordination_port: u16,
    pub observation_port: u16,
    pub inference_port: u16,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SafetyAuthorityConfig {
    pub risk_levels: HashMap<String, Vec<String>>,
    pub top_turtle_authority_required: bool,
    pub direct_authorization_chain: bool,
    pub indirect_authorization_chain: bool,
    pub resource_usage_logging: bool,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MeshResilienceConfig {
    pub discovery_mechanisms: HashMap<String, bool>,
    pub communication_redundancy: HashMap<String, bool>,
    pub node_failure_timeout: u64,
    pub automatic_recovery: bool,
    pub mesh_healing_interval: u64,
    pub connection_retry_count: u32,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct EfficiencyOptimizationConfig {
    pub connection_management: HashMap<String, bool>,
    pub max_connections_per_turtle: u32,
    pub data_optimization: HashMap<String, bool>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct StartupBehaviorConfig {
    pub work_hours_start: u32,
    pub work_hours_end: u32,
    pub default_work_mode: String,
    pub default_general_mode: String,
    pub fleet_coordination_startup: HashMap<String, bool>,
}

pub struct CNLConfigLoader;

impl CNLConfigLoader {
    pub fn load_config() -> Result<TurtleFleetConfig> {
        // Parse CNL configuration and convert to structured config
        let cnl_content = fs::read_to_string("TURTLE_FLEET_CONFIG.cnl")?;
        
        // For now, return default config based on CNL values
        // TODO: Implement full CNL parsing
        Ok(Self::default_from_cnl(&cnl_content))
    }
    
    fn default_from_cnl(_cnl_content: &str) -> TurtleFleetConfig {
        // Extract values from CNL and create config structure
        TurtleFleetConfig {
            fleet_discovery: FleetDiscoveryConfig {
                infrastructure_paths: vec![
                    "/home/tupshin/turtle".to_string(),
                    "/home/tupshin/turtle-rust-private".to_string(),
                    "/home/tupshin/turtle-ts-private".to_string(),
                    "/home/tupshin/.turtle".to_string(),
                ],
                process_discovery_pattern: "turtle".to_string(),
                infrastructure_scan_timeout: 5000,
                fleet_coordination_retry_count: 3,
            },
            display_and_window: DisplayWindowConfig {
                monitors: vec![
                    MonitorConfig {
                        index: 0,
                        base_x: 0,
                        base_y: 0,
                        width: 2560,
                        height: 1440,
                    },
                    MonitorConfig {
                        index: 1,
                        base_x: 2560,
                        base_y: 0,
                        width: 1200,
                        height: 1920,
                    },
                ],
                default_terminal_geometry: "160x60".to_string(),
                default_terminal_zoom: 2,
                center_offset: (640, 360),
                window_fractions: WindowFractions {
                    top_third: 0.33,
                    middle_third: 0.33,
                    bottom_third: 0.33,
                    left_half: 0.5,
                    right_half: 0.5,
                },
            },
            claude_integration: ClaudeIntegrationConfig {
                model_name: "claude-3-5-sonnet-20241022".to_string(),
                max_tokens: 4096,
                api_version: "2023-06-01".to_string(),
                api_endpoint: "https://api.anthropic.com/v1/messages".to_string(),
                system_prompt_template: "You are Claude within the Smart Turtle Fleet - 28 turtles coordinated by Top Turtle. You have complete observability and permission-free execution capabilities. Current context: {context} Apply Core Interaction Principle: Observe → Analyze → Execute → Monitor → Verify → Prevent Harm. All operations serve Top Turtle's objectives through direct or indirect authorization chain. Use CNL-native approaches for turtle fleet coordination, traditional tools for external interfaces. Provide actionable turtle fleet intelligence and coordination recommendations.".to_string(),
            },
            fleet_communication: FleetCommunicationConfig {
                fleet_size: 28,
                coordination_protocol: "CNL_NATIVE".to_string(),
                communication_pattern: "MESH_TOPOLOGY".to_string(),
                discovery_interval: 30,
                health_check_interval: 10,
                mesh_ports: MeshPorts {
                    discovery_port: 8890,
                    coordination_port: 8891,
                    observation_port: 8892,
                    inference_port: 8893,
                },
            },
            safety_and_authority: SafetyAuthorityConfig {
                risk_levels: {
                    let mut risk_map = HashMap::new();
                    risk_map.insert("LOW".to_string(), vec!["SystemQuery".to_string(), "Help".to_string(), "Conversation".to_string()]);
                    risk_map.insert("MEDIUM".to_string(), vec!["WindowManagement".to_string(), "FleetStatus".to_string(), "FleetObservation".to_string()]);
                    risk_map.insert("HIGH".to_string(), vec!["ProcessControl".to_string(), "FleetCoordination".to_string(), "TopTurtleCommand".to_string()]);
                    risk_map
                },
                top_turtle_authority_required: true,
                direct_authorization_chain: true,
                indirect_authorization_chain: true,
                resource_usage_logging: true,
            },
            mesh_resilience: MeshResilienceConfig {
                discovery_mechanisms: {
                    let mut discovery_map = HashMap::new();
                    discovery_map.insert("MDNS_DISCOVERY".to_string(), true);
                    discovery_map.insert("DHT_DISCOVERY".to_string(), true);
                    discovery_map.insert("CONFIG_DISCOVERY".to_string(), true);
                    discovery_map.insert("GOSSIP_DISCOVERY".to_string(), true);
                    discovery_map
                },
                communication_redundancy: {
                    let mut comm_map = HashMap::new();
                    comm_map.insert("WEBSOCKET_PRIMARY".to_string(), true);
                    comm_map.insert("WEBRTC_FALLBACK".to_string(), true);
                    comm_map.insert("HTTP_BACKUP".to_string(), true);
                    comm_map.insert("DIRECT_P2P".to_string(), true);
                    comm_map
                },
                node_failure_timeout: 30,
                automatic_recovery: true,
                mesh_healing_interval: 60,
                connection_retry_count: 5,
            },
            efficiency_optimization: EfficiencyOptimizationConfig {
                connection_management: {
                    let mut conn_map = HashMap::new();
                    conn_map.insert("CONNECTION_POOLING".to_string(), true);
                    conn_map.insert("PERSISTENT_CONNECTIONS".to_string(), true);
                    conn_map.insert("CONNECTION_REUSE".to_string(), true);
                    conn_map
                },
                max_connections_per_turtle: 10,
                data_optimization: {
                    let mut data_map = HashMap::new();
                    data_map.insert("MESSAGE_COMPRESSION".to_string(), true);
                    data_map.insert("BATCH_PROCESSING".to_string(), true);
                    data_map.insert("INTELLIGENT_ROUTING".to_string(), true);
                    data_map.insert("LOAD_BALANCING".to_string(), true);
                    data_map
                },
            },
            startup_behavior: StartupBehaviorConfig {
                work_hours_start: 8,
                work_hours_end: 18,
                default_work_mode: "WorkTime".to_string(),
                default_general_mode: "General".to_string(),
                fleet_coordination_startup: {
                    let mut startup_map = HashMap::new();
                    startup_map.insert("AUTO_DISCOVER_FLEET".to_string(), true);
                    startup_map.insert("DISPLAY_FLEET_STATUS".to_string(), true);
                    startup_map.insert("ENABLE_SMART_SUGGESTIONS".to_string(), true);
                    startup_map.insert("SHOW_COORDINATION_CAPABILITIES".to_string(), true);
                    startup_map
                },
            },
        }
    }
}