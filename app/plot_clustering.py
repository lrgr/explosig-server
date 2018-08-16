import pandas as pd
import numpy as np
import scipy.cluster
from functools import reduce

from web_constants import *
from plot_processing import *
from signatures import Signatures


def plot_clustering(sigs, projects):
    signatures = Signatures(SIGS_FILE, SIGS_META_FILE, chosen_sigs=sigs)
    sig_names = signatures.get_chosen_names()
    full_exps_df = pd.DataFrame(index=[], columns=sig_names)
    
    project_metadata = PlotProcessing.project_metadata()
    for proj_id in projects:
        if project_metadata[proj_id][HAS_COUNTS]:
            # counts data
            counts_filepath = project_metadata[proj_id]["counts_sbs_path"]
            counts_df = PlotProcessing.pd_fetch_tsv(counts_filepath, index_col=0)
            counts_df = counts_df.dropna(how='any', axis='index')
            
            if len(counts_df) > 0:
                # compute exposures
                exps_df = signatures.get_exposures(counts_df)

                full_exps_df = full_exps_df.append(exps_df, ignore_index=False)

    # Do hierarchical clustering 
    # Reference: https://gist.github.com/mdml/7537455
    observation_vectors = full_exps_df.values
    Z = scipy.cluster.hierarchy.linkage(observation_vectors, method='ward')
    T = scipy.cluster.hierarchy.to_tree(Z)

    # Create dictionary for labeling nodes by their IDs
    labels = list(full_exps_df.index.values)
    id2label = dict(zip(range(len(labels)), labels))

    # Create a nested dictionary from the ClusterNode's returned by SciPy
    def add_node(node, parent):
        # First create the new node and append it to its parent's children
        new_node = dict( node_id=node.id, children=[] )
        parent["children"].append( new_node )
        # Recursively add the current node's children
        if node.left: add_node( node.left, new_node )
        if node.right: add_node( node.right, new_node )
    
    # Initialize nested dictionary for d3, then recursively iterate through tree
    tree_dict = dict(children=[], name="root")
    add_node( T, tree_dict )
  
    # Label each node with the names of each leaf in its subtree
    def label_tree( n ):
        # If the node is a leaf, then we have its name
        if len(n["children"]) == 0:
            leaf_names = [ id2label[n["node_id"]] ]
        # If not, flatten all the leaves in the node's subtree
        else:
            leaf_names = reduce(lambda ls, c: ls + label_tree(c), n["children"], [])
        # Delete the node id since we don't need it anymore and it makes for cleaner JSON
        del n["node_id"]
        # Labeling convention: "-"-separated leaf names
        n["name"] = name = "-".join(sorted(map(str, leaf_names)))
        return leaf_names

    label_tree( tree_dict["children"][0] )
    return tree_dict