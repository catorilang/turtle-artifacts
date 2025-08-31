use anyhow::Result;
use turtle::dashboard::Dashboard;

#[tokio::main]
async fn main() -> Result<()> {
    let mut dashboard = Dashboard::new().await?;
    dashboard.show_work_focused().await?;
    Ok(())
}