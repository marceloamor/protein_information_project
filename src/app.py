"""
Main application file for the Protein Information Explorer.
"""
import os
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

from src.components.layout import create_layout
from src.data.loader import DataLoader
from src.pages.about import create_about_page
from src.pages.home import create_home_page
from src.pages.protein_detail import create_protein_detail_page
from src.utils.logging import logger

# Initialize the Dash application
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Protein Information Explorer",
)

# Create assets folder if it doesn't exist
assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

# Initialize DataLoader
logger.info("Initializing DataLoader...")
try:
    loader = DataLoader(data_path="data")
    logger.info(
        f"DataLoader initialized successfully. "
        f"Proteins: {len(loader.protein_nodes)}, "
        f"GO Terms: {len(loader.go_terms)}, "
        f"Edges: {len(loader.edges)}"
    )
except Exception as e:
    logger.error(f"Error initializing DataLoader: {e}")
    loader = None

# Define app layout with URL routing
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="protein-store", storage_type="session"),
        create_layout(html.Div(id="page-content")),
    ]
)


# Callback for URL routing
@callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("protein-store", "data"),
)
def display_page(pathname, protein_data):
    """
    Route to the appropriate page based on the URL path.
    
    Args:
        pathname: The URL path
        protein_data: Stored protein data
        
    Returns:
        The page layout
    """
    logger.info(f"Navigating to: {pathname}")
    
    if pathname == "/":
        return create_home_page()
    elif pathname == "/protein" and protein_data:
        return create_protein_detail_page(protein_data)
    elif pathname == "/about":
        return create_about_page()
    else:
        return create_home_page()


# Callback for search functionality
@callback(
    [
        Output("search-results-card", "style"),
        Output("search-results-content", "children"),
        Output("search-error-collapse", "is_open"),
        Output("search-error", "children"),
    ],
    Input("search-button", "n_clicks"),
    [
        State("search-input", "value"),
        State("search-type", "value"),
    ],
    prevent_initial_call=True,
)
def perform_search(n_clicks, search_term, search_type):
    """
    Perform a search based on the input term and type.
    
    Args:
        n_clicks: Button click count
        search_term: The search term
        search_type: The search type (protein or go_term)
        
    Returns:
        Tuple of (results_style, results_content, error_visible, error_message)
    """
    if not n_clicks or not search_term:
        return {"display": "none"}, [], False, ""
    
    if not loader:
        return {"display": "block"}, [], True, "Error: DataLoader not initialized."
    
    logger.info(f"Performing search: {search_term} (type: {search_type})")
    
    try:
        if search_type == "protein":
            results = loader.search_protein(search_term)
            if not results:
                return {"display": "block"}, [], True, f"No proteins found for: {search_term}"
            
            logger.info(f"Found {len(results)} proteins")
            
            # Create result cards
            result_cards = []
            for i, protein_id in enumerate(results[:20]):  # Limit to 20 results
                protein_details = loader.get_protein_details(protein_id)
                card = dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5(protein_details.get("name", protein_id)),
                                html.P(f"ID: {protein_id}"),
                                html.P(f"UUID: {protein_details.get('uuid', 'N/A')}"),
                                dbc.Button(
                                    "View Details",
                                    id={"type": "protein-button", "index": i},
                                    color="primary",
                                    className="mt-2",
                                ),
                                # Hidden div to store protein data
                                html.Div(
                                    id={"type": "protein-data", "index": i},
                                    style={"display": "none"},
                                    **{"data-protein": str(protein_id)},
                                ),
                            ]
                        )
                    ],
                    className="mb-3",
                )
                result_cards.append(card)
            
            return {"display": "block"}, result_cards, False, ""
        
        elif search_type == "go_term":
            # Handle GO term search
            go_results = loader.search_by_go_term(search_term)
            if not go_results:
                return {"display": "block"}, [], True, f"No GO terms found for: {search_term}"
            
            logger.info(f"Found {len(go_results)} proteins for GO term")
            
            # Create result cards for proteins associated with this GO term
            result_cards = []
            for i, protein in enumerate(go_results[:20]):  # Limit to 20 results
                protein_id = protein.get("protein_id")
                card = dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H5(protein.get("name", protein_id)),
                                html.P(f"ID: {protein_id}"),
                                html.P(f"Score: {protein.get('score', 'N/A')}"),
                                dbc.Button(
                                    "View Details",
                                    id={"type": "protein-button", "index": i},
                                    color="primary",
                                    className="mt-2",
                                ),
                                # Hidden div to store protein data
                                html.Div(
                                    id={"type": "protein-data", "index": i},
                                    style={"display": "none"},
                                    **{"data-protein": str(protein_id)},
                                ),
                            ]
                        )
                    ],
                    className="mb-3",
                )
                result_cards.append(card)
            
            return {"display": "block"}, result_cards, False, ""
    
    except Exception as e:
        logger.error(f"Error during search: {e}")
        return {"display": "block"}, [], True, f"Error: {str(e)}"


# Callback for protein button clicks
@callback(
    [
        Output("protein-store", "data"),
        Output("url", "pathname"),
    ],
    Input({"type": "protein-button", "index": dash.ALL}, "n_clicks"),
    State({"type": "protein-data", "index": dash.ALL}, "data-protein"),
    prevent_initial_call=True,
)
def view_protein_details(n_clicks, protein_ids):
    """
    Handle clicks on protein buttons and load protein details.
    
    Args:
        n_clicks: List of button click counts
        protein_ids: List of protein IDs
        
    Returns:
        Tuple of (protein_data, new_pathname)
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update
    
    # Get the index of the clicked button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    index = int(eval(button_id)["index"])
    protein_id = protein_ids[index]
    
    logger.info(f"Loading details for protein: {protein_id}")
    
    try:
        # Get protein details using loader
        protein_details = loader.get_protein_details(protein_id)
        return protein_details, "/protein"
    except Exception as e:
        logger.error(f"Error loading protein details: {e}")
        return None, "/"


if __name__ == "__main__":
    # Get port from environment variable or use default (8050)
    port = int(os.environ.get("PORT", 8050))
    debug = os.environ.get("DEBUG", "True").lower() == "true"
    
    logger.info(f"Starting application on port {port} (debug={debug})")
    app.run_server(debug=debug, port=port, host="0.0.0.0") 