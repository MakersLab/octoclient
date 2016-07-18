import pytest
from betamax import Betamax

from octoclient import OctoClient


URL = 'http://printer15.local'
APIKEY = 'YouShallNotPass'

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'


@pytest.mark.usefixtures('betamax_session')
class TestClient:
    def test_init_works_with_good_auth(self, betamax_session):
        # Should not raise anything
        OctoClient(url=URL, apikey=APIKEY, session=betamax_session)

    def test_init_raises_with_bad_auth(self, betamax_session):
        with pytest.raises(RuntimeError):
            OctoClient(url=URL, apikey='nope', session=betamax_session)

    def test_files_contains_files_and_free_space_info(self, betamax_session):
        oc = OctoClient(url=URL, apikey=APIKEY, session=betamax_session)
        files = oc.files()
        assert 'hodorstop.gcode' in [f['name'] for f in files['files']]
        assert isinstance(files['free'], int)

    def test_files_local_works(self, betamax_session):
        oc = OctoClient(url=URL, apikey=APIKEY, session=betamax_session)
        files = oc.files('local')
        assert 'hodorstop.gcode' in [f['name'] for f in files['files']]
        assert isinstance(files['free'], int)

    def test_files_sdcard_works(self, betamax_session):
        oc = OctoClient(url=URL, apikey=APIKEY, session=betamax_session)
        files = oc.files('sdcard')
        assert not files['files']  # no files on sdcard
        assert 'free' not in files  # API doesn't report that back

    def test_files_bogus_location_raises(self, betamax_session):
        oc = OctoClient(url=URL, apikey=APIKEY, session=betamax_session)
        with pytest.raises(RuntimeError):
            oc.files('fantomas')