from functools import lru_cache
from replicate.client import Client
from decouple import config
from replicate.exceptions import ReplicateError

REPLICATE_API_TOKEN = config("REPLICATE_API_TOKEN")
REPLICATE_MODEL = config("REPLICATE_MODEL", default="codingforentrepreneurs/superme-justin-v1")
REPLICATE_MODEL_VERSION = config("REPLICATE_MODEL_VERSION", default="4bc2a39fa73d29cd531c57ad4f56bede13378ce3da2f6f517684b0b61bd192b7")

@lru_cache
def get_replicate_client():
    return Client(api_token=REPLICATE_API_TOKEN)

@lru_cache
def get_replicate_model_version():
    replicate_client = get_replicate_client()
    rep_model = replicate_client.models.get(REPLICATE_MODEL)
    rep_version = rep_model.versions.get(REPLICATE_MODEL_VERSION)
    return rep_version

def generate_image(prompt,
                   require_trigger_word=True,
                   trigger_word="TOK"):
    if require_trigger_word:
        if trigger_word not in prompt:
            raise Exception(f"{trigger_word}, not included")
    input_args = {
        "prompt": prompt,
        "num_outputs": 2,
        "output_format": "jpg",
    }
    replicate_client = get_replicate_client()
    replicate_version = get_replicate_model_version()
    return replicate_client.predictions.create(
        version=replicate_version,
        input=input_args
    )

# def get_prediction_detail(prediction_id=None):
#     replicate_client = get_replicate_client()
#     try:
#         pred = replicate_client.predictions.get(prediction_id)
#     except ReplicateError:
#         return None, 404
#     except:
#         return None, 500
#     return pred, 200

def list_prediction_results(
        model=REPLICATE_MODEL,
        version=REPLICATE_MODEL_VERSION,
        status=None,
        max_size=500
        ):
    replicate_client = get_replicate_client()
    preds = replicate_client.predictions.list()
    results = list(preds.results)
    while preds.next:
        _preds = replicate_client.predictions.list(preds.next)
        results += list(_preds.results)
        if len(results) > max_size:
            break
    results = [x for x in results if x.model==model and x.version==version]
    if status is not None:
        results = [x for x in results if x.status == status]
    return results

def get_prediction_detail(
        prediction_id=None
        ):
    replicate_client = get_replicate_client()
    pred = replicate_client.predictions.list(prediction_id)
    return pred