# Freelance Dev OS Dashboard

A modern, responsive web dashboard for managing your CV/AI freelance business built with FastAPI, Jinja2 templates, and vanilla JavaScript.

## Features

- **Overview Dashboard** - Key metrics, active projects, revenue summary, and hours tracking
- **Projects View** - Manage active CV/AI projects with status, hours, and progress tracking
- **Clients View** - Client list with health scores and relationship monitoring
- **Revenue View** - Financial performance with charts and invoice tracking
- **Pipeline View** - Sales pipeline with conversion rates across stages
- **Time Tracking** - Hours logged by client and project with utilization rates

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Templates**: Jinja2 (server-side rendering)
- **Styling**: Custom CSS with dark theme
- **Charts**: Custom canvas-based charting (no external dependencies)
- **Data**: Integration with existing MCP server JSON data

## Installation

### Prerequisites

- Python 3.8+
- Existing Freelance Dev OS setup with MCP servers

### Install Dependencies

The dashboard requires additional dependencies beyond the base Freelance Dev OS:

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

Or use the provided tools/requirements.txt (includes all CV/AI and dashboard dependencies).

### Directory Structure

```
dashboard/
├── __init__.py           # Package initialization
├── main.py              # FastAPI application and routes
├── config.py            # Dashboard configuration
├── data_loader.py       # Data integration with MCP servers
├── templates/           # Jinja2 HTML templates
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Overview dashboard
│   ├── projects.html   # Projects view
│   ├── clients.html    # Clients view
│   ├── revenue.html    # Revenue/financial view
│   ├── pipeline.html   # Sales pipeline view
│   └── time_tracking.html  # Time tracking view
├── static/             # Static assets
│   ├── css/
│   │   └── style.css   # Dashboard styles (dark theme)
│   └── js/
│       └── dashboard.js # Charts and interactivity
└── README.md           # This file
```

## Usage

### Starting the Dashboard

From the repository root directory:

```bash
# Run directly with Python
python -m dashboard.main

# Or use uvicorn
uvicorn dashboard.main:app --host 0.0.0.0 --port 8000 --reload
```

The dashboard will be available at: http://localhost:8000

### Configuration

Dashboard behavior can be customized using environment variables:

```bash
# Dashboard server settings
export DASHBOARD_HOST="0.0.0.0"
export DASHBOARD_PORT="8000"
export DASHBOARD_RELOAD="True"

# Appearance
export DASHBOARD_TITLE="My CV/AI Business"
export DASHBOARD_THEME="dark"

# Features
export ENABLE_API="True"
export ENABLE_CORS="True"
export AUTO_REFRESH_INTERVAL="300"  # 5 minutes
```

Add these to your `.env` file for persistence.

### API Endpoints

The dashboard provides REST API endpoints for programmatic access:

- `GET /api/overview` - Overview statistics
- `GET /api/projects?status=<status>` - Projects list
- `GET /api/clients` - Clients list
- `GET /api/revenue?months=<months>` - Revenue data
- `GET /api/pipeline` - Sales pipeline data
- `GET /api/time-tracking?days=<days>` - Time tracking data
- `GET /health` - Health check

Example API usage:

```bash
# Get overview stats
curl http://localhost:8000/api/overview

# Get active projects only
curl http://localhost:8000/api/projects?status=in_progress

# Get revenue for last 6 months
curl http://localhost:8000/api/revenue?months=6
```

### Data Integration

The dashboard reads data from existing MCP server storage:

- **Work Server**: `vault/03-Tasks/tasks.yaml` and `hours.yaml`
- **Client Server**: `data/client_data.json`
- **Billing Server**: `data/billing_data.json`
- **LLC Ops Server**: `data/llc_ops_data.json`
- **Onboarding Server**: `data/onboarding_data.json`
- **Career Server**: `data/career_data.json`

No modification to existing MCP servers is required - the dashboard reads data in real-time.

## Features in Detail

### Overview Dashboard
- Active projects count and status
- Client health monitoring
- Revenue summaries (total, pending, paid)
- Billable hours and utilization rate
- Quick action links to other views

### Projects View
- Filter by status (pending, in progress, completed)
- Track hours logged vs. estimated
- View progress bars for each project
- Billable/non-billable tagging
- Priority indicators (P0-P3)
- Client association

### Clients View
- Client cards with key information
- Health score visualization (0-100)
- Health status indicators (good/average/poor)
- Active/inactive status
- Contact information

### Revenue View
- Monthly revenue trend chart (bar chart)
- Total and average revenue calculations
- Recent invoices table
- Invoice status tracking (paid/pending/overdue)
- Financial health metrics

### Pipeline View
- Four-stage pipeline (Leads → Proposals → Contracts → Active)
- Conversion rates between stages
- Pipeline value by stage
- Individual opportunity details
- Total pipeline value calculation

### Time Tracking View
- Hours breakdown by client
- Billable vs. non-billable hours
- Utilization rate calculation
- Daily hours chart (line chart)
- Configurable time range (7/30/90 days)

## Customization

### Themes

The default dark theme can be customized by editing `static/css/style.css`. Key CSS variables:

```css
:root {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --bg-card: #333333;
    --accent-primary: #4a90e2;
    --accent-secondary: #2ecc71;
    /* ... more variables ... */
}
```

### Adding New Views

To add a new dashboard view:

1. Create HTML template in `templates/`
2. Add route in `main.py`:
   ```python
   @app.get("/my-view", response_class=HTMLResponse)
   async def my_view(request: Request):
       # Load data
       # Return template
   ```
3. Add navigation link in `templates/base.html`
4. Add API endpoint if needed

### Custom Charts

The dashboard includes a simple chart library (`SimpleChart` in `dashboard.js`). To add custom charts:

```javascript
// In your template's extra_js block
const myData = { 'Jan': 100, 'Feb': 150, 'Mar': 200 };
new SimpleChart('myCanvasId', myData, {
    type: 'bar',  // or 'line'
    color: '#4a90e2',
    backgroundColor: 'rgba(74, 144, 226, 0.3)',
    borderWidth: 2
});
```

## Troubleshooting

### Dashboard won't start
- Check that FastAPI and dependencies are installed: `pip install fastapi uvicorn jinja2`
- Verify port 8000 is not already in use
- Check logs for specific error messages

### No data showing
- Ensure MCP server data files exist in `data/` and `vault/` directories
- Run MCP servers to generate sample data
- Check file permissions on data directory

### Charts not rendering
- Check browser console for JavaScript errors
- Verify canvas elements have valid IDs
- Ensure data is in correct format (object with string keys)

### Styling issues
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check that `static/css/style.css` is loaded correctly
- Inspect element to verify CSS classes are applied

## Performance

- Dashboard loads data on each page request (real-time)
- No database queries - reads from JSON files
- Suitable for 100s of projects/clients/invoices
- For larger datasets, consider adding pagination
- Auto-refresh can be enabled for live monitoring

## Security

- CORS is enabled by default for API access
- No authentication included - add if exposing publicly
- Runs on localhost by default
- For production deployment:
  - Add authentication (OAuth, API keys, etc.)
  - Use HTTPS
  - Restrict CORS origins
  - Add rate limiting

## Development

### Running in Development Mode

```bash
uvicorn dashboard.main:app --reload --log-level debug
```

### Testing

Test the dashboard manually:

1. Start the dashboard: `python -m dashboard.main`
2. Open browser to http://localhost:8000
3. Navigate through all views
4. Test API endpoints with curl or browser

### Adding Features

The codebase is structured for easy extension:

- **New data sources**: Extend `DataLoader` class in `data_loader.py`
- **New routes**: Add to `main.py`
- **New templates**: Create in `templates/`
- **New styles**: Update `static/css/style.css`
- **New JS features**: Add to `static/js/dashboard.js`

## Future Enhancements

Potential features for future versions:

- [ ] Real-time websocket updates
- [ ] Advanced filtering and search
- [ ] Export data to PDF/Excel
- [ ] Email reports and alerts
- [ ] Custom dashboards per user
- [ ] Mobile app integration
- [ ] Advanced analytics and forecasting
- [ ] Integration with external services (Stripe, calendar, etc.)

## License

Part of the Freelance Dev OS project. See main repository LICENSE file.

## Support

For issues, questions, or contributions, please refer to the main Freelance Dev OS repository.
