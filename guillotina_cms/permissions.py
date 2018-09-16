from guillotina import configure

configure.grant(
    permission="guillotina.SearchContent",
    role="guillotina.Manager")

configure.permission('guillotina.ManageVersioning', 'Ability to modify versioning on an object')
configure.permission('guillotina.ManageConstraints', 'Allow to check and change type constraints')

configure.permission('guillotina.RequestReview', 'Request review permission')

configure.grant(
    permission='guillotina.ManageVersioning',
    role='guillotina.Manager'
)

configure.grant(
    permission='guillotina.ManageConstraints',
    role='guillotina.Manager'
)

configure.grant(
    permission='guillotina.ManageConstraints',
    role='guillotina.ContainerAdmin'
)

configure.grant(
    permission='guillotina.RequestReview',
    role='guillotina.Manager'
)

configure.grant(
    permission='guillotina.RequestReview',
    role='guillotina.Owner'
)
