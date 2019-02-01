from flask import Flask, request
from jsonschema import validate

from plot_data_listing import plot_data_listing

from plot_clustering import plot_clustering

from scale_samples import scale_samples

from plot_exposures import plot_exposures
from scale_exposures import scale_exposures

from plot_counts import plot_counts
from scale_counts import scale_counts

from plot_samples_meta import plot_samples_meta

from plot_gene_event_track import plot_gene_event_track, autocomplete_gene, plot_pathways_listing
from plot_clinical import plot_clinical, plot_clinical_variables
from scale_clinical import scale_clinical

from plot_survival import plot_survival


# Reconstruction plots
from plot_counts_per_category import plot_counts_per_category
from plot_reconstruction import plot_reconstruction
from plot_reconstruction_error import plot_reconstruction_error
# Reconstruction scales
from scale_counts_per_category import scale_counts_per_category
from scale_reconstruction import scale_reconstruction
from scale_reconstruction_error import scale_reconstruction_error

from scale_contexts import scale_contexts
from plot_signature import plot_signature
from plot_reconstruction_cosine_similarity import plot_reconstruction_cosine_similarity
from sharing_state import get_sharing_state, set_sharing_state, plot_featured_listing

from oncotree import *

from web_constants import *
from response_utils import *


app = Flask(__name__)

"""
Reusable JSON schema
"""
string_array_schema = {
  "type": "array",
  "items": {
    "type": "string"
  }
}
projects_schema = string_array_schema
signatures_schema = {
  "type" : "object",
  "properties": dict([(mut_type, string_array_schema) for mut_type in MUT_TYPES])
}


"""
Data listing
"""
@app.route('/data-listing', methods=['POST'])
def route_data_listing():
  output = plot_data_listing()
  return response_json(app, output)

@app.route('/pathways-listing', methods=['POST'])
def route_pathways_listing():
  output = plot_pathways_listing()
  return response_json(app, output)

@app.route('/featured-listing', methods=['POST'])
def route_featured_listing():
  output = plot_featured_listing()
  return response_json(app, output)


"""
Signatures
"""
schema_signature = {
  "type": "object",
  "properties": {
    "signature": {"type": "string"},
    "mut_type": {"type": "string"}
  }
}
@app.route('/plot-signature', methods=['POST'])
def route_plot_signature():
  req = request.get_json(force=True)
  validate(req, schema_signature)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_signature(signature=req["signature"], mut_type=req["mut_type"])
  return response_json(app, output)

"""
Samples-by-project
"""
schema_samples_meta = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/plot-samples-meta', methods=['POST'])
def route_plot_samples_meta():
  req = request.get_json(force=True)
  validate(req, schema_counts)

  output = plot_samples_meta(req["projects"])
  return response_json(app, output)

"""
Counts
"""
schema_counts = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/plot-counts', methods=['POST'])
def route_plot_counts():
  req = request.get_json(force=True)
  validate(req, schema_counts)

  output = plot_counts(req["projects"])
  return response_json(app, output)

@app.route('/scale-counts', methods=['POST'])
def route_scale_counts():
  req = request.get_json(force=True)
  validate(req, schema_counts)

  output = scale_counts(req["projects"])
  return response_json(app, output)

@app.route('/scale-counts-sum', methods=['POST'])
def route_scale_counts_sum():
  req = request.get_json(force=True)
  validate(req, schema_counts)

  output = scale_counts(req["projects"], count_sum=True)
  return response_json(app, output)

"""
Exposures
"""
schema_exposures = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "projects": projects_schema,
    "mut_type": {"type": "string"}
  }
}
@app.route('/plot-exposures', methods=['POST'])
def route_plot_exposures():
  req = request.get_json(force=True)
  validate(req, schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_exposures(req["signatures"], req["projects"], req["mut_type"])
  return response_json(app, output)

@app.route('/plot-exposures-normalized', methods=['POST'])
def route_plot_exposures_normalized():
  req = request.get_json(force=True)
  validate(req, schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_exposures(req["signatures"], req["projects"], req["mut_type"], normalize=True)
  return response_json(app, output)

@app.route('/scale-exposures', methods=['POST'])
def route_scale_exposures():
  req = request.get_json(force=True)
  validate(req, schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], exp_sum=False)
  return response_json(app, output)

@app.route('/scale-exposures-normalized', methods=['POST'])
def route_scale_exposures_normalized():
  req = request.get_json(force=True)
  validate(req, schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], exp_sum=False, exp_normalize=True)
  return response_json(app, output)


@app.route('/scale-exposures-sum', methods=['POST'])
def route_scale_exposures_sum():
  req = request.get_json(force=True)
  validate(req, schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], exp_sum=True)
  return response_json(app, output)

schema_exposures_single_sample = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "projects": projects_schema,
    "mut_type": {"type": "string"},
    "sample_id": {"type": "string"}
  }
}
@app.route('/plot-exposures-single-sample', methods=['POST'])
def route_plot_exposures_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_exposures(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/scale-exposures-single-sample', methods=['POST'])
def route_scale_exposures_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], exp_sum=False, exp_normalize=False)
  return response_json(app, output)


"""
Reconstruction error
"""
schema_reconstruction_error_single_sample = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "projects": projects_schema,
    "mut_type": {"type": "string"},
    "sample_id": {"type": "string"}
  }
}
@app.route('/plot-counts-per-category-single-sample', methods=['POST'])
def route_plot_counts_per_category_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_counts_per_category(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/plot-reconstruction-single-sample', methods=['POST'])
def route_plot_reconstruction_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/plot-reconstruction-error-single-sample', methods=['POST'])
def route_plot_reconstruction_error_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction_error(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/plot-reconstruction-cosine-similarity', methods=['POST'])
def route_plot_reconstruction_cosine_similarity():
  req = request.get_json(force=True)
  validate(req, schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction_cosine_similarity(req["signatures"], req["projects"], req["mut_type"])
  return response_json(app, output)

@app.route('/plot-reconstruction-cosine-similarity-single-sample', methods=['POST'])
def route_plot_reconstruction_cosine_similarity_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction_cosine_similarity(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"])
  return response_json(app, output)


@app.route('/scale-counts-per-category-single-sample', methods=['POST'])
def route_scale_counts_per_category_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_counts_per_category(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/scale-reconstruction-single-sample', methods=['POST'])
def route_scale_reconstruction_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_reconstruction(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/scale-reconstruction-error-single-sample', methods=['POST'])
def route_scale_reconstruction_error_single_sample():
  req = request.get_json(force=True)
  validate(req, schema_reconstruction_error_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_reconstruction_error(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)


schema_contexts = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "mut_type": {"type": "string"}
  }
}
@app.route('/scale-contexts', methods=['POST'])
def route_scale_contexts():
  req = request.get_json(force=True)
  validate(req, schema_contexts)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_contexts(req["signatures"], req["mut_type"])
  return response_json(app, output)


"""
Hierarchical clustering plot
"""
schema_clustering = {
  "type": "object",
  "properties": {
    "signatures": signatures_schema,
    "projects": projects_schema
  }
}
@app.route('/clustering', methods=['POST'])
def route_clustering():
  req = request.get_json(force=True)
  validate(req, schema_clustering)

  output = plot_clustering(req["signatures"], req["projects"])
  return response_json(app, output)


"""
Genome Event Tracks
"""
schema_gene_event_track = {
  "type": "object",
  "properties": {
    "gene_id": {"type": "string"},
    "projects": projects_schema
  }
}
@app.route('/plot-gene-event-track', methods=['POST'])
def route_gene_event_track():
  req = request.get_json(force=True)
  validate(req, schema_gene_event_track)

  output = plot_gene_event_track(req["gene_id"], req["projects"])
  return response_json(app, output) 


"""
Autocomplete gene ID
"""
schema_autocomplete_gene = {
  "type": "object",
  "properties": {
    "projects": projects_schema,
    "gene_id_partial": {"type": "string"}
  }
}
@app.route('/autocomplete-gene', methods=['POST'])
def route_autocomplete_gene():
  req = request.get_json(force=True)
  validate(req, schema_autocomplete_gene)

  output = autocomplete_gene(req["gene_id_partial"], req["projects"])
  return response_json(app, output)

"""
Clinical Variable Tracks
"""
schema_clinical = {
  "type": "object",
  "properties": {
    "clinical_variable": {"type": "string"},
    "projects": projects_schema
  }
}
@app.route('/plot-clinical', methods=['POST'])
def route_plot_clinical():
  req = request.get_json(force=True)
  validate(req, schema_clinical)

  output = plot_clinical(req["projects"])
  return response_json(app, output)

@app.route('/scale-clinical', methods=['POST'])
def route_scale_clinical():
  req = request.get_json(force=True)
  validate(req, schema_clinical)

  output = scale_clinical(req["projects"])
  return response_json(app, output)

schema_survival = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/plot-survival', methods=['POST'])
def route_plot_survival():
  req = request.get_json(force=True)
  validate(req, schema_survival)

  output = plot_survival(req["projects"])
  return response_json(app, output)

"""
Samples listing
"""
schema_samples = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/scale-samples', methods=['POST'])
def route_scale_samples():
  req = request.get_json(force=True)
  validate(req, schema_samples)

  output = scale_samples(req["projects"])
  if len(output) != len(set(output)):
    print("WARNING: Duplicate sample IDs")
  return response_json(app, output)

"""
Clinical variable listing
"""
@app.route('/clinical-variable-list', methods=['POST'])
def route_clinical_variable_list():

  output = plot_clinical_variables()
  return response_json(app, output) 

"""
Gene alteration scale
"""
@app.route('/scale-gene-alterations', methods=['POST'])
def route_scale_gene_alterations():

  output = [e.value for e in MUT_CLASS_VALS] + ["None"]
  return response_json(app, output) 

"""
Sharing: get state
"""
schema_sharing_get = {
  "type": "object",
  "properties": {
    "slug": {"type": "string"}
  }
}
@app.route('/sharing-get', methods=['POST'])
def route_sharing_get():
  req = request.get_json(force=True)
  validate(req, schema_sharing_get)
  try:
    output = get_sharing_state(req['slug'])
    return response_json(app, output)
  except:
    return response_json_error(app, {"message": "An error has occurred."}, 500)

"""
Sharing: set state
"""
schema_sharing_set = {
  "type": "object",
  "properties": {
    "state": {"type": "string"}
  }
}
@app.route('/sharing-set', methods=['POST'])
def route_sharing_set():
  req = request.get_json(force=True)
  validate(req, schema_sharing_set)
  try:
    output = set_sharing_state(req['state'])
    return response_json(app, output)
  except:
    return response_json_error(app, {"message": "An error has occurred."}, 500)


if __name__ == '__main__':
  app.run(
      host='0.0.0.0',
      debug=bool(os.environ.get('DEBUG', '')), 
      port=int(os.environ.get('PORT', 8000)),
      use_reloader=True
  )
