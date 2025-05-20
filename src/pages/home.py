"""
Home page for the Dash application.
"""
import dash_bootstrap_components as dbc
from dash import html

from src.components.search import create_search_form, create_search_results


def create_home_page():
    """
    Create the home page layout.
    
    Returns:
        A Dash HTML layout
    """
    return html.Div(
        [
            # Hero section
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Protein Information Explorer", className="display-4"),
                        html.P(
                            "Explore protein-protein interactions and functional annotations.",
                            className="lead",
                        ),
                        html.Hr(className="my-4"),
                    ],
                    width={"size": 10, "offset": 1},
                ),
                className="mb-5",
            ),
            
            # Search section
            dbc.Row(
                dbc.Col(
                    [
                        create_search_form(),
                        create_search_results(),
                    ],
                    width={"size": 10, "offset": 1},
                ),
            ),
            
            # Stats section
            dbc.Row(
                dbc.Col(
                    [
                        html.H3("Database Statistics", className="mb-4"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Proteins", className="card-title"),
                                                html.P(
                                                    "27,768",
                                                    className="card-text display-6 text-center",
                                                ),
                                            ]
                                        ),
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("GO Terms", className="card-title"),
                                                html.P(
                                                    "9,594",
                                                    className="card-text display-6 text-center",
                                                ),
                                            ]
                                        ),
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Relationships", className="card-title"),
                                                html.P(
                                                    "498,731",
                                                    className="card-text display-6 text-center",
                                                ),
                                            ]
                                        ),
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Identifiers", className="card-title"),
                                                html.P(
                                                    "27,768",
                                                    className="card-text display-6 text-center",
                                                ),
                                            ]
                                        ),
                                    ),
                                    width=3,
                                ),
                            ],
                        ),
                    ],
                    width={"size": 10, "offset": 1},
                ),
                className="mt-5",
            ),
        ]
    ) 