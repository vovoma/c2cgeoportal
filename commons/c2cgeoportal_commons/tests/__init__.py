import pytest
import transaction
from pyramid import testing
from c2cgeoportal_commons.scripts.initializedb import init_db
from c2cgeoportal_commons.models import get_engine, get_session_factory, get_tm_session, generate_mappers

@pytest.fixture(scope='session')
def dbsession(request):    
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgresql://www-data:www-data@localhost:5432/c2cgeoportal',
        'schema': 'main',
        'parent_schema': '',
        'srid': 3857
    })
    settings = config.get_settings()
    generate_mappers(settings)
    engine = get_engine(settings)

    init_db(engine, force=True)

    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)
    return session

@pytest.fixture(scope='function')
@pytest.mark.usefixtures("dbsession")
def transact(request, dbsession):
    dbsession.begin_nested()
    yield
    dbsession.rollback()
