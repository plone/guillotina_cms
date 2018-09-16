import json

async def test_constraints(cms_requester):
    async with cms_requester as requester:

        resp, status = await requester(
            'POST',
            '/db/guillotina/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 1',
                'id': 'doc1'
            })
        )

        # Check constraints
        resp, status = await requester(
            'GET',
            '/db/guillotina/doc1/@constraints'
        )

        assert 'File' in resp
        assert 'Image' in resp
        assert len(resp) == 2

        # Try to create a document inside a document
        resp, status = await requester(
            'POST',
            '/db/guillotina/doc1/',
            data=json.dumps({
                '@type': 'Document',
                'title': 'Document 1',
                'id': 'doc1'
            })
        )

        assert status == 412

        # Set only Files are available
        resp, status = await requester(
            'POST',
            '/db/guillotina/doc1/@constraints',
            data=json.dumps(['File'])
        )

        assert status == 200

        resp, status = await requester(
            'GET',
            '/db/guillotina/doc1/@constraints'
        )
        assert resp[0] == 'File'
        assert len(resp) == 1

        resp, status = await requester(
            'POST',
            '/db/guillotina/doc1/',
            data=json.dumps({
                '@type': 'File',
                'title': 'File 1',
                'id': 'fil1'
            })
        )

        assert status == 201

        resp, status = await requester(
            'POST',
            '/db/guillotina/doc1/',
            data=json.dumps({
                '@type': 'Image',
                'title': 'Image 1',
                'id': 'img1'
            })
        )

        assert status == 412

        # Set also Images are available
        resp, status = await requester(
            'PATCH',
            '/db/guillotina/doc1/@constraints',
            data=json.dumps({
                'op': 'add',
                'types': ['Image']})
        )

        assert status == 200

        resp, status = await requester(
            'GET',
            '/db/guillotina/doc1/@constraints'
        )
        assert len(resp) == 2

        resp, status = await requester(
            'POST',
            '/db/guillotina/doc1/',
            data=json.dumps({
                '@type': 'Image',
                'title': 'Image 1',
                'id': 'img1'
            })
        )

        assert status == 201

        # Try to set any non existing type
        resp, status = await requester(
            'PATCH',
            '/db/guillotina/doc1/@constraints',
            data=json.dumps({
                'op': 'add',
                'types': ['FakeType']})
        )

        assert status == 412

        # Try to set any non FTI enabled type
        resp, status = await requester(
            'PATCH',
            '/db/guillotina/doc1/@constraints',
            data=json.dumps({
                'op': 'add',
                'types': ['Document']})
        )

        assert status == 412
