import pandas as pd
import duckdb
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple

class DataLoader:
    """
    Data loader for the protein information application.
    Handles loading and querying of the parquet files.
    """
    
    def __init__(self, data_path: str = "data"):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the directory containing the parquet files.
        """
        self.data_path = Path(data_path)
        self.duckdb_con = duckdb.connect(':memory:')
        self.protein_nodes = None
        self.go_terms = None
        self.edges = None
        self.protein_ids = None
        
        # Maps for fast lookup
        self.id_to_details = {}  # Map protein IDs to details
        self.uuid_to_ids = {}    # Map UUIDs to protein IDs
        self.identifier_to_ids = {}  # Map all identifiers to protein IDs
        self.name_to_ids = {}    # Map protein names to protein IDs
        
        # Constants for the data model
        self.FUNCTIONAL_ANNOTATION_TYPES = [
            "BiologicalProcess-Protein-FunctionalAnnotation",
            "MolecularFunction-Protein-FunctionalAnnotation",
            "CellularComponent-Protein-FunctionalAnnotation"
        ]
        self.PROTEIN_INTERACTION_TYPE = "Protein-Protein-ProteinProteinInteraction"
        
        # Load data
        self.load_data()
        
    def load_data(self):
        """Load all parquet files and create necessary indexes."""
        # Load the data using DuckDB
        print("Loading protein_nodes.parquet...")
        self.protein_nodes = self.duckdb_con.execute(
            f"SELECT * FROM '{self.data_path}/protein_nodes.parquet'"
        ).df()
        
        print("Loading go_term_nodes.parquet...")
        self.go_terms = self.duckdb_con.execute(
            f"SELECT * FROM '{self.data_path}/go_term_nodes.parquet'"
        ).df()
        
        print("Loading edges.parquet...")
        self.edges = self.duckdb_con.execute(
            f"SELECT * FROM '{self.data_path}/edges.parquet'"
        ).df()
        
        print("Loading protein_id_records.parquet...")
        self.protein_ids = self.duckdb_con.execute(
            f"SELECT * FROM '{self.data_path}/protein_id_records.parquet'"
        ).df()
        
        print("Creating lookup maps...")
        # Create lookup maps for efficient searching
        self._create_lookup_maps()
        
    def _create_lookup_maps(self):
        """Create maps for efficient lookup."""
        # First, map each protein ID to its details from protein_nodes
        for _, row in self.protein_nodes.iterrows():
            protein_id = row['id']
            name = row.get('name')
            self.id_to_details[protein_id] = row.to_dict()
            
            # Add protein_id to identifier_to_ids map
            if protein_id not in self.identifier_to_ids:
                self.identifier_to_ids[protein_id] = [protein_id]
            
            # Map protein name to protein ID
            if name:
                if name not in self.name_to_ids:
                    self.name_to_ids[name] = []
                if protein_id not in self.name_to_ids[name]:
                    self.name_to_ids[name].append(protein_id)
                
                # Also add name to identifier_to_ids for direct search
                if name not in self.identifier_to_ids:
                    self.identifier_to_ids[name] = []
                if protein_id not in self.identifier_to_ids[name]:
                    self.identifier_to_ids[name].append(protein_id)
        
        # Next, create mappings from UUID and other identifiers to protein IDs
        for _, row in self.protein_ids.iterrows():
            uuid = row['uuid']
            external_id = row.get('external_id')
            name = row.get('name')
            
            # Map UUID to this external_id (protein ID)
            if external_id:
                if uuid not in self.uuid_to_ids:
                    self.uuid_to_ids[uuid] = []
                if external_id not in self.uuid_to_ids[uuid]:
                    self.uuid_to_ids[uuid].append(external_id)
            
            # Map UUID to protein ID in identifier_to_ids
            if uuid:
                if uuid not in self.identifier_to_ids:
                    self.identifier_to_ids[uuid] = []
                
                # Make sure we add both the UUID and external_id
                if uuid.startswith('Protein::') and uuid not in self.identifier_to_ids[uuid]:
                    self.identifier_to_ids[uuid].append(uuid)
                if external_id and external_id not in self.identifier_to_ids[uuid]:
                    self.identifier_to_ids[uuid].append(external_id)
            
            # Map external_id back to itself for direct lookups
            if external_id:
                if external_id not in self.identifier_to_ids:
                    self.identifier_to_ids[external_id] = []
                if external_id not in self.identifier_to_ids[external_id]:
                    self.identifier_to_ids[external_id].append(external_id)
            
            # Map name to protein ID if available
            if name:
                if name not in self.name_to_ids:
                    self.name_to_ids[name] = []
                if external_id and external_id not in self.name_to_ids[name]:
                    self.name_to_ids[name].append(external_id)
                
                # Also add name to identifier_to_ids for direct search
                if name not in self.identifier_to_ids:
                    self.identifier_to_ids[name] = []
                if external_id and external_id not in self.identifier_to_ids[name]:
                    self.identifier_to_ids[name].append(external_id)
            
            # Add secondary identifiers if available
            if 'secondary_ids' in row and isinstance(row.get('secondary_ids'), list):
                for identifier in row['secondary_ids']:
                    if identifier not in self.identifier_to_ids:
                        self.identifier_to_ids[identifier] = []
                    if external_id and external_id not in self.identifier_to_ids[identifier]:
                        self.identifier_to_ids[identifier].append(external_id)
            
            # Add ambiguous identifiers if available
            if 'ambiguous_secondary_ids' in row and isinstance(row.get('ambiguous_secondary_ids'), list):
                for identifier in row['ambiguous_secondary_ids']:
                    if identifier not in self.identifier_to_ids:
                        self.identifier_to_ids[identifier] = []
                    if external_id and external_id not in self.identifier_to_ids[identifier]:
                        self.identifier_to_ids[identifier].append(external_id)
        
        # Fill in missing mappings by checking the edges file
        protein_ids_from_edges = set(self.edges['source'].unique()) | set(self.edges['target'].unique())
        for protein_id in protein_ids_from_edges:
            # Only consider protein IDs
            if isinstance(protein_id, str) and protein_id.startswith('Protein::'):
                # If this protein ID is not in our lookup yet, add it
                if protein_id not in self.identifier_to_ids:
                    self.identifier_to_ids[protein_id] = [protein_id]
                elif protein_id not in self.identifier_to_ids[protein_id]:
                    self.identifier_to_ids[protein_id].append(protein_id)
                
                # If we don't have details for this protein yet, create a minimal entry
                if protein_id not in self.id_to_details:
                    self.id_to_details[protein_id] = {
                        'id': protein_id,
                        'name': protein_id
                    }
    
    def search_protein(self, identifier: str) -> List[str]:
        """
        Search for proteins by identifier.
        
        Args:
            identifier: The identifier to search for.
            
        Returns:
            A list of protein IDs matching the identifier.
        """
        # Direct lookup in identifier_to_ids map
        if identifier in self.identifier_to_ids:
            return self.identifier_to_ids[identifier]
        
        # Try searching by name
        if identifier in self.name_to_ids:
            return self.name_to_ids[identifier]
        
        # Fallback to fuzzy matching on protein names if no exact match found
        if len(identifier) >= 3:  # Only try fuzzy matching for longer strings
            matches = []
            for name, ids in self.name_to_ids.items():
                if identifier.lower() in name.lower():
                    matches.extend(ids)
            
            if matches:
                return list(set(matches))  # Deduplicate
        
        # No matches found
        return []
    
    def get_protein_details(self, protein_id: str) -> Dict:
        """
        Get details for a specific protein.
        
        Args:
            protein_id: The protein ID.
            
        Returns:
            A dictionary containing protein details.
        """
        # Start with basic details from our lookup
        if protein_id in self.id_to_details:
            result = dict(self.id_to_details[protein_id])
        else:
            result = {'id': protein_id, 'name': protein_id}
        
        # Add UUID if available
        for uuid, ids in self.uuid_to_ids.items():
            if protein_id in ids:
                result['uuid'] = uuid
                break
        
        # Add functional annotations
        result['functional_annotations'] = self._get_functional_annotations(protein_id)
        
        # Add protein-protein interactions
        result['protein_interactions'] = self._get_protein_interactions(protein_id)
        
        return result
    
    def _get_functional_annotations(self, protein_id: str) -> List[Dict]:
        """
        Get functional annotations for a protein.
        
        Args:
            protein_id: The protein ID.
            
        Returns:
            A list of dictionaries containing functional annotations.
        """
        # Find functional annotation edges for this protein
        functional_edges = self.edges[
            self.edges['relationship'].isin(self.FUNCTIONAL_ANNOTATION_TYPES) & 
            (self.edges['source'] == protein_id)
        ]
        
        annotations = []
        for _, edge in functional_edges.iterrows():
            go_term_id = edge['target']
            go_term = self.go_terms[self.go_terms['id'] == go_term_id]
            
            if not go_term.empty:
                # Extract namespace from the relationship type
                namespace = edge['relationship'].split('-')[0]  # BiologicalProcess, MolecularFunction, or CellularComponent
                
                annotation = {
                    'go_term_id': go_term_id,
                    'go_id': go_term.iloc[0].get('external_id', None),  # GO:00... identifier
                    'name': go_term.iloc[0].get('name', None),
                    'namespace': namespace,
                    'score': edge.get('ML_prediction_score', None)  # Score is ML_prediction_score
                }
                annotations.append(annotation)
        
        return annotations
    
    def _get_protein_interactions(self, protein_id: str) -> List[Dict]:
        """
        Get protein-protein interactions for a protein.
        
        Args:
            protein_id: The protein ID.
            
        Returns:
            A list of dictionaries containing protein interactions.
        """
        # Filter edges for protein-protein interactions (both directions)
        source_edges = self.edges[
            (self.edges['relationship'] == self.PROTEIN_INTERACTION_TYPE) & 
            (self.edges['source'] == protein_id)
        ]
        
        target_edges = self.edges[
            (self.edges['relationship'] == self.PROTEIN_INTERACTION_TYPE) & 
            (self.edges['target'] == protein_id)
        ]
        
        interactions = []
        
        # Process source-to-target interactions
        for _, edge in source_edges.iterrows():
            target_id = edge['target']
            
            interaction = {
                'protein_id': target_id,
                'direction': 'target',
                'score': edge.get('string_combined_score', None)  # Use string_combined_score as the score
            }
            
            # Add name if available in our details map
            if target_id in self.id_to_details and 'name' in self.id_to_details[target_id]:
                interaction['name'] = self.id_to_details[target_id]['name']
            
            # Add UUID if available
            for uuid, ids in self.uuid_to_ids.items():
                if target_id in ids:
                    interaction['protein_uuid'] = uuid
                    break
            
            interactions.append(interaction)
        
        # Process target-to-source interactions
        for _, edge in target_edges.iterrows():
            source_id = edge['source']
            
            interaction = {
                'protein_id': source_id,
                'direction': 'source',
                'score': edge.get('string_combined_score', None)  # Use string_combined_score as the score
            }
            
            # Add name if available in our details map
            if source_id in self.id_to_details and 'name' in self.id_to_details[source_id]:
                interaction['name'] = self.id_to_details[source_id]['name']
            
            # Add UUID if available
            for uuid, ids in self.uuid_to_ids.items():
                if source_id in ids:
                    interaction['protein_uuid'] = uuid
                    break
            
            interactions.append(interaction)
        
        return interactions
    
    def search_by_go_term(self, go_term_id: str) -> List[Dict]:
        """
        Search for proteins by GO term.
        
        Args:
            go_term_id: The GO term ID to search for.
            
        Returns:
            A list of protein dictionaries associated with the GO term.
        """
        # Find GO term using external_id
        go_term = self.go_terms[self.go_terms['external_id'] == go_term_id]
        
        if go_term.empty:
            return []
        
        go_term_id_internal = go_term.iloc[0]['id']
        
        # Find proteins linked to this GO term
        annotations = self.edges[
            self.edges['relationship'].isin(self.FUNCTIONAL_ANNOTATION_TYPES) & 
            (self.edges['target'] == go_term_id_internal)
        ]
        
        results = []
        for _, annotation in annotations.iterrows():
            protein_id = annotation['source']
            
            result = {
                'protein_id': protein_id,
                'name': self.id_to_details.get(protein_id, {}).get('name', protein_id),
                'score': annotation.get('ML_prediction_score', None)
            }
            
            # Add UUID if available
            for uuid, ids in self.uuid_to_ids.items():
                if protein_id in ids:
                    result['uuid'] = uuid
                    break
            
            results.append(result)
        
        return results 