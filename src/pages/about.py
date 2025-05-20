"""
About page for the Dash application.
"""
import dash_bootstrap_components as dbc
from dash import html


def create_about_page():
    """
    Create the about page layout.
    
    Returns:
        A Dash HTML layout
    """
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("About this Application", className="mb-4"),
                        html.P(
                            "The Protein Information Explorer is a tool for exploring protein data, "
                            "including protein-protein interactions and Gene Ontology (GO) term annotations.",
                            className="lead",
                        ),
                        html.Hr(),
                    ],
                    width={"size": 10, "offset": 1},
                ),
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Features", className="card-title"),
                                    html.Ul(
                                        [
                                            html.Li("Search for proteins by identifier"),
                                            html.Li("View detailed protein information"),
                                            html.Li("Explore protein-protein interactions"),
                                            html.Li("View functional annotations (GO terms)"),
                                            html.Li("Search for proteins by GO term"),
                                            html.Li("Visualize protein interaction networks"),
                                        ]
                                    ),
                                ]
                            ),
                            className="mb-4",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Data Sources", className="card-title"),
                                    html.P(
                                        "This application uses data from the following sources:"
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    html.Strong("protein_nodes.parquet: "),
                                                    "Contains protein information (27,768 rows)",
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Strong("go_term_nodes.parquet: "),
                                                    "Contains GO term information (9,594 rows)",
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Strong("edges.parquet: "),
                                                    "Contains relationships between proteins and GO terms (498,731 rows)",
                                                ]
                                            ),
                                            html.Li(
                                                [
                                                    html.Strong("protein_id_records.parquet: "),
                                                    "Maps UUIDs to external identifiers (27,768 rows)",
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            className="mb-4",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Technology Stack", className="card-title"),
                                    html.P(
                                        "This application is built with the following technologies:"
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Python for data processing and backend logic"),
                                            html.Li("Dash and Dash Bootstrap Components for the web interface"),
                                            html.Li("DuckDB for efficient data querying"),
                                            html.Li("Pandas for data manipulation"),
                                            html.Li("Dash Cytoscape for network visualizations"),
                                        ]
                                    ),
                                ]
                            ),
                            className="mb-4",
                        ),
                    ],
                    width={"size": 10, "offset": 1},
                ),
            ),
        ]
    ) 