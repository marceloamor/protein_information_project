"""
Protein detail page for the Dash application.
"""
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import html

from src.components.protein_card import create_protein_card


def create_protein_detail_page(protein_details=None):
    """
    Create the protein detail page layout.
    
    Args:
        protein_details: Dictionary containing protein information
        
    Returns:
        A Dash HTML layout
    """
    if not protein_details:
        return html.Div(
            [
                html.H1("Protein Details"),
                html.P("No protein selected. Please select a protein from the search results."),
                dbc.Button("Back to Search", href="/", color="primary"),
            ]
        )
    
    # Create nodes and edges for the interaction network
    nodes = []
    edges = []
    
    # Add the main protein node
    main_id = protein_details.get("id", "")
    main_name = protein_details.get("name", main_id)
    nodes.append(
        {
            "data": {"id": main_id, "label": main_name},
            "classes": "main-node",
        }
    )
    
    # Add interaction nodes and edges
    interactions = protein_details.get("protein_interactions", [])
    for i, interaction in enumerate(interactions[:20]):  # Limit to 20 interactions
        target_id = interaction.get("protein_id", f"unknown_{i}")
        target_name = interaction.get("name", target_id)
        direction = interaction.get("direction", "")
        score = interaction.get("score", 0)
        
        # Add node if not already in the list
        if not any(node["data"]["id"] == target_id for node in nodes):
            nodes.append(
                {
                    "data": {"id": target_id, "label": target_name},
                    "classes": "interaction-node",
                }
            )
        
        # Add edge based on direction
        if direction == "target":
            edges.append(
                {
                    "data": {
                        "source": main_id,
                        "target": target_id,
                        "weight": score,
                    }
                }
            )
        else:  # direction == "source"
            edges.append(
                {
                    "data": {
                        "source": target_id,
                        "target": main_id,
                        "weight": score,
                    }
                }
            )
    
    # Network styles
    cyto_stylesheet = [
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
                "text-wrap": "wrap",
                "text-max-width": "100px",
                "font-size": "12px",
                "text-valign": "center",
                "text-halign": "center",
                "background-color": "#77C6E1",
                "width": "60px",
                "height": "60px",
            },
        },
        {
            "selector": ".main-node",
            "style": {
                "background-color": "#FF8888",
                "width": "80px",
                "height": "80px",
                "font-weight": "bold",
                "font-size": "14px",
            },
        },
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "arrow-scale": 1.5,
                "line-color": "#aaa",
                "target-arrow-color": "#aaa",
                "width": "data(weight)",
            },
        },
    ]
    
    # Create the network component if there are interactions
    network = html.Div(
        [
            html.H3("Protein Interaction Network", className="mb-3"),
            cyto.Cytoscape(
                id="protein-network",
                layout={"name": "cose", "animate": False},
                style={"width": "100%", "height": "500px", "border": "1px solid #ddd"},
                elements=nodes + edges,
                stylesheet=cyto_stylesheet,
            ),
        ],
        className="mt-4 mb-4",
    ) if interactions else html.Div()
    
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(main_name, className="mb-4"),
                            dbc.Button(
                                "Back to Search",
                                href="/",
                                color="primary",
                                className="mb-4",
                            ),
                        ]
                    )
                ]
            ),
            dbc.Row(
                [
                    # Protein details card
                    dbc.Col(
                        create_protein_card(protein_details),
                        width=12,
                        lg=6,
                    ),
                    
                    # Network visualization
                    dbc.Col(
                        network,
                        width=12,
                        lg=6,
                    ),
                ]
            ),
        ]
    ) 