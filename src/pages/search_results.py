import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from typing import Dict, List
from src.components.protein_card import create_protein_card
from src.components.go_term_card import create_go_term_card

def create_search_results_page(search_type: str, results: List[Dict], query: str):
    """
    Create the search results page layout.
    
    Args:
        search_type: Type of search ('protein' or 'go_term').
        results: List of search results (proteins or GO terms).
        query: The search query.
        
    Returns:
        A Dash component representing the search results page.
    """
    # Create header
    header = html.Div([
        html.H2(f"Search Results for: {query}", className="mb-3"),
        html.P(f"Found {len(results)} results for your search."),
        dbc.Button("Back to Home", href="/", color="secondary", className="mb-3"),
        html.Hr(),
    ])
    
    # Create results
    if not results:
        results_section = html.Div([
            html.P("No results found. Please try another search term."),
        ], className="mt-3")
    else:
        if search_type == "protein":
            results_section = html.Div([
                html.Div([
                    create_protein_card(result)
                ]) for result in results
            ])
        else:  # go_term
            results_section = html.Div([
                html.Div([
                    create_go_term_card(result)
                ]) for result in results
            ])
    
    # Create page
    return html.Div([
        header,
        results_section,
    ], className="container py-4") 