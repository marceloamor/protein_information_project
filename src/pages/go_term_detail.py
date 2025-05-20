import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from typing import Dict, List
from src.components.go_term_card import create_go_term_proteins_list

def create_go_term_detail_page(go_term_data: Dict, associated_proteins: List[Dict]):
    """
    Create the GO term detail page layout.
    
    Args:
        go_term_data: Dictionary containing GO term information.
        associated_proteins: List of proteins associated with the GO term.
        
    Returns:
        A Dash component representing the GO term detail page.
    """
    # Check if GO term data exists
    if not go_term_data:
        return html.Div([
            html.H2("GO Term Not Found", className="text-danger mb-3"),
            html.P("The requested GO term could not be found."),
            dbc.Button("Back to Home", href="/", color="secondary", className="mb-3"),
        ], className="container py-4")
    
    # Extract GO term info
    go_id = go_term_data.get('go_id', 'N/A')
    name = go_term_data.get('name', 'N/A')
    namespace = go_term_data.get('namespace', 'N/A')
    
    # Create header
    header = html.Div([
        html.H2(f"GO Term: {go_id}", className="mb-3"),
        html.H4(f"Name: {name}", className="mb-2"),
        html.P(f"Namespace: {namespace}", className="mb-3"),
        dbc.Button("Back to Search Results", id="back-to-results", color="secondary", className="mb-3 me-2"),
        dbc.Button("Back to Home", href="/", color="secondary", className="mb-3"),
        html.Hr(),
    ])
    
    # Create proteins section
    proteins_section = html.Div([
        html.H3(f"Associated Proteins ({len(associated_proteins)})", className="mb-3"),
        html.Div([
            create_go_term_proteins_list(associated_proteins)
        ]),
    ])
    
    # Create page
    return html.Div([
        header,
        proteins_section,
    ], className="container py-4") 