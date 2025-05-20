"""
Search components for the Dash application.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html


def create_search_form():
    """
    Create a search form for proteins or GO terms.
    
    Returns:
        A Dash form component
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4("Search", className="card-title"),
                html.P(
                    "Search for proteins by identifier or GO terms",
                    className="card-text",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Input(
                                    id="search-input",
                                    placeholder="Enter protein ID, name, or GO term...",
                                    type="text",
                                    className="mb-2",
                                ),
                            ],
                            width=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Select(
                                    id="search-type",
                                    options=[
                                        {"label": "Protein", "value": "protein"},
                                        {"label": "GO Term", "value": "go_term"},
                                    ],
                                    value="protein",
                                    className="mb-2",
                                ),
                            ],
                            width=4,
                        ),
                    ]
                ),
                dbc.Button(
                    "Search",
                    id="search-button",
                    color="primary",
                    className="mt-2",
                ),
                dbc.Collapse(
                    dbc.Card(
                        dbc.CardBody(
                            html.P(id="search-error", className="text-danger"),
                        )
                    ),
                    id="search-error-collapse",
                    is_open=False,
                ),
            ]
        ),
        className="mb-4",
    )


def create_search_results():
    """
    Create a component for displaying search results.
    
    Returns:
        A Dash component for search results
    """
    return dbc.Card(
        [
            dbc.CardHeader(html.H5("Search Results")),
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.P("No results to display. Try searching for a protein or GO term."),
                        ],
                        id="search-results-content",
                    ),
                ]
            ),
        ],
        id="search-results-card",
        className="mb-4",
        style={"display": "none"},
    ) 