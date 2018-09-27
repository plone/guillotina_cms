from pytest_docker_fixtures import images


images.configure(
    'cockroach',
    'cockroachdb/cockroach', 'v2.0.5')


pytest_plugins = [
    'pytest_docker_fixtures',
    'guillotina.tests.fixtures',
    'guillotina_elasticsearch.tests.fixtures',
    'guillotina_rediscache.tests.fixtures',
    'guillotina_linkintegrity.tests.fixtures',
    'guillotina_cms.tests.fixtures'
]
