from time import sleep

from rubric.server.commons.es_wrapper import create_es_wrapper
from rubric.server.commons.models import TaskType
from rubric.server.datasets.dao import create_datasets_dao
from rubric.server.datasets.model import ObservationDatasetDB

es_wrapper = create_es_wrapper()
dao = create_datasets_dao(es_wrapper)


def test_retrieve_ownered_dataset_for_no_owner_user():
    dataset = "test_retrieve_ownered_dataset_for_no_owner_user"
    created = dao.create_dataset(
        ObservationDatasetDB(
            name=dataset, owner="other", task=TaskType.text_classification
        )
    )
    sleep(1)

    assert dao.find_by_name(created.name, owner=created.owner) == created
    assert dao.find_by_name(created.name, owner=None) == created
    assert dao.find_by_name(created.name, owner="me") == created