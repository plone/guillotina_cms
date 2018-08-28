from guillotina import configure

configure.grant(
    permission="guillotina.SearchContent",
    role="guillotina.Manager")

configure.permission('guillotina.ManageVersioning', 'Ability to modify versioning on an object')

configure.permission('guillotina.RequestReview', 'Request review permission')

configure.grant(
    permission='guillotina.ManageVersioning',
    role='guillotina.Manager'
)

configure.grant(
    permission='guillotina.RequestReview',
    role='guillotina.Manager'
)

configure.grant(
    permission='guillotina.RequestReview',
    role='guillotina.Owner'
)
