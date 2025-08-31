use anyhow::Result;
use turtle::dashboard::Dashboard;

#[tokio::main]
async fn main() -> Result<()> {
    let mut dashboard = Dashboard::new().await?;
    dashboard.show_compact().await?;
    Ok(())
}