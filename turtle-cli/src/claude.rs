use anyhow::Result;
use reqwest::Client;
use serde_json::{json, Value};
use std::env;

pub struct Claude {
    client: Client,
    api_key: String,
}

impl Claude {
    pub fn new() -> Option<Self> {
        if let Ok(api_key) = env::var("ANTHROPIC_API_KEY") {
            Some(Claude {
                client: Client::new(),
                api_key,
            })
        } else {
            None
        }
    }

    pub async fn chat(&self, message: &str, context: &str) -> Result<String> {
        let system_prompt = format!(
            "You are Claude within the Smart Turtle Fleet - 28 turtles coordinated by Top Turtle. \
             You have complete observability and permission-free execution capabilities. \
             Current context: {}\n\
             Apply Core Interaction Principle: Observe → Analyze → Execute → Monitor → Verify → Prevent Harm. \
             All operations serve Top Turtle's objectives through direct or indirect authorization chain. \
             Use CNL-native approaches for turtle fleet coordination, traditional tools for external interfaces. \
             Provide actionable turtle fleet intelligence and coordination recommendations.",
            context
        );

        let request_body = json!({
            "model": "claude-3-5-sonnet-20241022", 
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user", 
                    "content": format!("Top Turtle Command: {}", message)
                }
            ]
        });

        let response = self
            .client
            .post("https://api.anthropic.com/v1/messages")
            .header("x-api-key", &self.api_key)
            .header("anthropic-version", "2023-06-01")
            .header("content-type", "application/json")
            .json(&request_body)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            anyhow::bail!("Claude API error: {}", error_text);
        }

        let response_json: Value = response.json().await?;
        
        if let Some(content) = response_json["content"].as_array() {
            if let Some(text) = content.first().and_then(|c| c["text"].as_str()) {
                Ok(text.to_string())
            } else {
                anyhow::bail!("Unexpected response format from Claude API");
            }
        } else {
            anyhow::bail!("No content in Claude API response");
        }
    }
}

pub fn has_api_key() -> bool {
    env::var("ANTHROPIC_API_KEY").is_ok()
}