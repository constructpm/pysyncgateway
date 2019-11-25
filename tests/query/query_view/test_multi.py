

import uuid

import pytest


@pytest.fixture
def schools_database(database):
    """
    Type: 'pupil'

    =========== ======= ========
    Name        Parent  School
    =========== ======= ========
    Amy
    Andy        Paul    Olives
    Chris               St Barts
    Jo          Mel     St Barts
    Maggy       Mel     St Barts
    Mary        Maggy
    =========== ======= ========

    Returns:
        Database: Containing pupil information as above. Plus one extra 'class'
        document and one extra 'teacher' document.
    """
    teacher_doc = database.get_document(uuid.uuid4().hex)
    teacher_doc.data = {
        'type': 'teacher',
        'school': 'Olives',
    }
    teacher_doc.create_update()
    for name, parent, school in [
        ('Amy', None, None),
        ('Andy', 'Paul', 'Olives'),
        ('Chris', None, 'St Barts'),
        ('Jo', 'Mel', 'St Barts'),
        ('Maggy', 'Mel', 'St Barts'),
        ('Mary', 'Maggy', None),
    ]:
        doc = database.get_document(uuid.uuid4().hex)
        doc.data = {
            'type': 'pupil',
            'name': name,
            'parent': parent,
            'school': school,
        }
        doc.create_update()
    class_doc = database.get_document(uuid.uuid4().hex)
    class_doc.data = {
        'type': 'class',
        'subject': 'Geography',
    }
    class_doc.create_update()
    return database


def test_schools_database(schools_database):
    result = schools_database

    all_docs = result.all_docs()
    assert len(all_docs) == 8
    [doc.retrieve() for doc in all_docs]
    not_at_school = [doc for doc in all_docs if 'school' in doc.data and doc.data['school'] is None]
    assert len(not_at_school) == 2
    assert sorted([doc.data['name'] for doc in not_at_school]) == ['Amy', 'Mary']


@pytest.fixture
def pupil_data_design_doc(database):
    """
    Returns:
        Query: 'pupil_data' design document containing a single view called
        'list_pupils' which is keyed with `(parent, school)`.
    """
    query = database.get_query('pupil_data')
    query.data = {
        'views': {
            'list_pupils': {
                'map':
                """
function (doc,meta) {
    if(doc.type == "pupil") {
        emit([doc.parent, doc.school], doc);
    }
}
""",
            },
        },
    }
    query.create_update()
    return query


def test_pupil_query_doc_empty(pupil_data_design_doc):
    result = pupil_data_design_doc.query_view('list_pupils')

    assert result['total_rows'] == 0


def test_pupil_query_doc_with_data(pupil_data_design_doc, schools_database):
    result = pupil_data_design_doc.query_view('list_pupils')

    assert result['total_rows'] == 6
    keys = [row['key'] for row in result['rows']]
    assert all([len(k) == 2 for k in keys])


# --- TESTS ---


@pytest.mark.parametrize(
    'keys, expected_names',
    [
        (['Mel', 'St Barts'], ['Jo', 'Maggy']),
        ((None, 'St Barts'), ['Chris']),  # Uses a tuple of keys
        (['Maggy', None], ['Mary']),
        ([None, None], ['Amy']),
    ]
)
def test_both_keys(keys, expected_names, pupil_data_design_doc, schools_database):
    result = pupil_data_design_doc.query_view('list_pupils', key=keys)

    assert result['total_rows'] == len(expected_names)
    assert sorted([row['value']['name'] for row in result['rows']]) == expected_names


@pytest.mark.parametrize(
    'keys', [
        ('Mel', []),
        ([], 'Olives'),
        ([{}, 'St Barts'], []),
        ([(), 'St Barts'], []),
        ([[], 'St Barts'], []),
    ]
)
def test_bad(keys, pupil_data_design_doc, schools_database):
    """
    Pinning behaviour of badly formed keys - all give no data and no error.
    """
    result = pupil_data_design_doc.query_view('list_pupils', key=keys)

    assert result['total_rows'] == 0
    assert result['rows'] == []
