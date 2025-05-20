import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from typing import Dict, List

def create_protein_card(protein_details):
    """
    Create a card displaying protein details.
    
    Args:
        protein_details: Dictionary containing protein information
        
    Returns:
        A Dash card component with protein details
    """
    if not protein_details:
        return dbc.Card(
            dbc.CardBody([
                html.H5("Protein Details"),
                html.P("No protein selected."),
            ])
        )
    
    # Basic information section
    basic_info = dbc.Card(
        [
            dbc.CardHeader(html.H5("Basic Information")),
            dbc.CardBody(
                [
                    html.P([html.Strong("ID: "), protein_details.get("id", "N/A")]),
                    html.P([html.Strong("Name: "), protein_details.get("name", "N/A")]),
                    html.P([html.Strong("UUID: "), protein_details.get("uuid", "N/A")]),
                ]
            ),
        ],
        className="mb-3",
    )
    
    # Functional annotations section
    annotations = protein_details.get("functional_annotations", [])
    annotations_card = dbc.Card(
        [
            dbc.CardHeader(html.H5(f"Functional Annotations ({len(annotations)})")),
            dbc.CardBody(
                dash_table.DataTable(
                    data=annotations[:10],  # Show first 10 annotations
                    columns=[
                        {"name": "GO ID", "id": "go_id"},
                        {"name": "Name", "id": "name"},
                        {"name": "Namespace", "id": "namespace"},
                        {"name": "Score", "id": "score", "type": "numeric", "format": {"specifier": ".3f"}},
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left"},
                    style_header={"fontWeight": "bold"},
                    page_size=5,
                ) if annotations else html.P("No functional annotations found.")
            ),
        ],
        className="mb-3",
    )
    
    # Protein interactions section
    interactions = protein_details.get("protein_interactions", [])
    interactions_card = dbc.Card(
        [
            dbc.CardHeader(html.H5(f"Protein-Protein Interactions ({len(interactions)})")),
            dbc.CardBody(
                dash_table.DataTable(
                    data=interactions[:10],  # Show first 10 interactions
                    columns=[
                        {"name": "Protein ID", "id": "protein_id"},
                        {"name": "Name", "id": "name"},
                        {"name": "Direction", "id": "direction"},
                        {"name": "Score", "id": "score", "type": "numeric", "format": {"specifier": ".3f"}},
                    ],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left"},
                    style_header={"fontWeight": "bold"},
                    page_size=5,
                ) if interactions else html.P("No protein interactions found.")
            ),
        ],
        className="mb-3",
    )
    
    # Main card
    return dbc.Card(
        [
            dbc.CardHeader(html.H4(protein_details.get("name", "Protein Details"))),
            dbc.CardBody(
                [
                    basic_info,
                    annotations_card,
                    interactions_card,
                ]
            ),
        ]
    )

def create_protein_detail_card(protein_data: Dict):
    """
    Create a detailed card component for a protein.
    
    Args:
        protein_data: Dictionary containing protein information.
        
    Returns:
        A Dash component representing the detailed protein card.
    """
    # Extract protein info
    uuid = protein_data.get('uuid', 'Unknown')
    
    # Get identifiers
    identifiers = protein_data.get('identifiers', {})
    primary_id = identifiers.get('primary', 'N/A')
    
    # Get functional annotations
    functional_annotations = protein_data.get('functional_annotations', [])
    
    # Get protein interactions
    protein_interactions = protein_data.get('protein_interactions', [])
    
    # Create card header
    header = dbc.CardHeader([
        html.H4(f"Protein: {primary_id}", className="card-title"),
        html.H6(f"UUID: {uuid}", className="card-subtitle text-muted"),
    ])
    
    # Create annotations section
    annotations_section = html.Div([
        html.H5("Functional Annotations (GO Terms)"),
        
        html.Div([
            create_annotation_table(functional_annotations)
        ]) if functional_annotations else html.P("No functional annotations found."),
    ])
    
    # Create interactions section
    interactions_section = html.Div([
        html.H5("Protein-Protein Interactions"),
        
        html.Div([
            create_interaction_table(protein_interactions)
        ]) if protein_interactions else html.P("No protein interactions found."),
    ])
    
    # Create protein card
    card = dbc.Card([
        header,
        dbc.CardBody([
            annotations_section,
            html.Hr(),
            interactions_section,
        ]),
    ], className="mb-3")
    
    return card

def create_annotation_table(annotations: List[Dict]):
    """Create a table to display functional annotations."""
    if not annotations:
        return html.P("No annotations found.")
    
    # Create table header
    header = html.Thead(html.Tr([
        html.Th("GO ID"),
        html.Th("Name"),
        html.Th("Namespace"),
        html.Th("Score"),
    ]))
    
    # Create table rows
    rows = []
    for annotation in annotations:
        row = html.Tr([
            html.Td(annotation.get('go_id', 'N/A')),
            html.Td(annotation.get('name', 'N/A')),
            html.Td(annotation.get('namespace', 'N/A')),
            html.Td(f"{annotation.get('score', 'N/A'):.4f}" if annotation.get('score') is not None else 'N/A'),
        ])
        rows.append(row)
    
    body = html.Tbody(rows)
    
    # Create table
    table = dbc.Table([header, body], bordered=True, hover=True, responsive=True, striped=True)
    
    return table

def create_interaction_table(interactions: List[Dict]):
    """Create a table to display protein-protein interactions."""
    if not interactions:
        return html.P("No interactions found.")
    
    # Create table header
    header = html.Thead(html.Tr([
        html.Th("Protein UUID"),
        html.Th("Primary Identifier"),
        html.Th("Direction"),
        html.Th("Score"),
    ]))
    
    # Create table rows
    rows = []
    for interaction in interactions:
        row = html.Tr([
            html.Td(interaction.get('protein_uuid', 'N/A')),
            html.Td(interaction.get('primary_identifier', 'N/A')),
            html.Td(interaction.get('direction', 'N/A')),
            html.Td(f"{interaction.get('score', 'N/A'):.4f}" if interaction.get('score') is not None else 'N/A'),
        ])
        rows.append(row)
    
    body = html.Tbody(rows)
    
    # Create table
    table = dbc.Table([header, body], bordered=True, hover=True, responsive=True, striped=True)
    
    return table 