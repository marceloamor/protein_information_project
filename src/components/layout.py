"""
Layout components for the Dash application.
"""
import dash_bootstrap_components as dbc
from dash import html

# Navbar component
def create_navbar():
    """Create the application navbar."""
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    [
                        html.Img(
                            src="/assets/protein_icon.png",
                            height="30px",
                            className="me-2",
                        ),
                        "Protein Information Explorer",
                    ],
                    href="/",
                    className="ms-2",
                ),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Search", href="/search")),
                        dbc.NavItem(dbc.NavLink("About", href="/about")),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
            ]
        ),
        color="primary",
        dark=True,
        className="mb-4",
    )


# Footer component
def create_footer():
    """Create the application footer."""
    return html.Footer(
        dbc.Container(
            [
                html.Hr(),
                html.P(
                    "Protein Information Explorer © 2023",
                    className="text-center text-muted",
                ),
            ]
        ),
        className="mt-4",
    )


# Main layout
def create_layout(content):
    """
    Create the main application layout.
    
    Args:
        content: The page content to display
        
    Returns:
        A Dash HTML layout
    """
    return html.Div(
        [
            create_navbar(),
            dbc.Container(content, className="mb-5"),
            create_footer(),
        ]
    )


# Loading component
def create_loading_component(component_id, component_type):
    """
    Create a loading component to show during data loading.
    
    Args:
        component_id: ID for the component
        component_type: Type of component (e.g., 'graph', 'table')
        
    Returns:
        A Dash loading component
    """
    return dbc.Spinner(
        [component_type(id=component_id)],
        color="primary",
        type="border",
        fullscreen=False,
    ) 