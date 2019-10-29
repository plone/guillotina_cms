
from os.path import join

from guillotina import configure
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IResource
from guillotina.response import HTTPNotFound
from guillotina.schema.vocabulary import getVocabularyRegistry
from guillotina.schema.vocabulary import VocabularyRegistryError


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@vocabularies',
    summary='Get available vocabularies')
async def get_vocabularies(context, request):
    result = []
    vocabulary_registry = getVocabularyRegistry()
    for key, item in vocabulary_registry._map.items():
        result.append({
            "@id": join(IAbsoluteURL(context)(), "@vocabularies", key),
            "title": key
        })
    return result


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@vocabularies/{key}',
    summary='Get specific vocabulary')
async def get_block_schema(context, request):
    key = request.matchdict['key']
    vocabulary_registry = getVocabularyRegistry()
    try:
        vocab = vocabulary_registry.get(context, key)
    except VocabularyRegistryError:
        return HTTPNotFound()

    result = {}
    result['@id'] = join(IAbsoluteURL(context)(), "@vocabularies", key)
    result['items'] = []
    for term in vocab.keys():
        result['items'].append({
            'title': vocab.getTerm(term),
            'token': term
        })
    return result
