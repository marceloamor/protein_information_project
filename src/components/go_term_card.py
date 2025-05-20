import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, List
from dash import dash_table

def create_go_term_card(go_term_details):
    """
    Create a card displaying GO term details.
    
    Args:
        go_term_details: Dictionary containing GO term information
        
    Returns:
        A Dash card component with GO term details
    """
    if not go_term_details:
        return dbc.Card(
            dbc.CardBody([
                html.H5("GO Term Details"),
                html.P("No GO term selected."),
            ])
        )
    
    # Basic information section
    basic_info = dbc.Card(
        [
            dbc.CardHeader(html.H5("Basic Information")),
            dbc.CardBody(
                [
                    html.P([html.Strong("GO ID: "), go_term_details.get("external_id", "N/A")]),
                    html.P([html.Strong("Name: "), go_term_details.get("name", "N/A")]),
                    html.P([html.Strong("Namespace: "), go_term_details.get("namespace", "N/A")]),
                ]
            ),
        ],
        className="mb-3",
    )
    
    # Associated proteins section
    proteins = go_term_details.get("associated_proteins", [])
    proteins_card = dbc.Card(
        [
            dbc.CardHeader(html.H5(f"Associated Proteins ({len(proteins)})")),
            dbc.CardBody(
                dash_table.DataTable(
                    data=proteins[:10],  # Show first 10 proteins
                    columns=[
                        {"name": "Protein ID", "id": "protein_id"},
                        {"name": "Name", "id": "name"},
                        {"name": "Score", "id": "score", "type": "numeric", "format": {"specifier": ".3f"}},
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left"},
                    style_header={"fontWeight": "bold"},
                    page_size=5,
                ) if proteins else html.P("No associated proteins found.")
            ),
        ],
        className="mb-3",
    )
    
    # Main card
    return dbc.Card(
        [
            dbc.CardHeader(html.H4(go_term_details.get("name", "GO Term Details"))),
            dbc.CardBody(
                [
                    basic_info,
                    proteins_card,
                ]
            ),
        ]
    )

def create_go_term_proteins_list(proteins: List[Dict]):
    """
    Create a component to display proteins associated with a GO term.
    
    Args:
        proteins: List of dictionaries containing protein information.
        
    Returns:
        A Dash component representing the proteins list.
    """
    if not proteins:
        return html.P("No associated proteins found.")
    
    # Create table header
    header = html.Thead(html.Tr([
        html.Th("Protein UUID"),
        html.Th("Primary Identifier"),
        html.Th("Score"),
        html.Th("Actions"),
    ]))
    
    # Create table rows
    rows = []
    for protein in proteins:
        row = html.Tr([
            html.Td(protein.get('uuid', 'N/A')),
            html.Td(protein.get('primary_identifier', 'N/A')),
            html.Td(f"{protein.get('score', 'N/A'):.4f}" if protein.get('score') is not None else 'N/A'),
            html.Td(
                dbc.Button(
                    "View",
                    id={"type": "view-protein-button", "uuid": protein.get('uuid')},
                    color="primary",
                    size="sm",
                )
            ),
        ])
        rows.append(row)
    
    body = html.Tbody(rows)
    
    # Create table
    table = dbc.Table([header, body], bordered=True, hover=True, responsive=True, striped=True)
    
    return table 