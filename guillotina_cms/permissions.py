from guillotina import configure


configure.permission('guillotina.ManageVersioning', 'Ability to modify versioning on an object')
configure.permission('guillotina.ManageConstraints', 'Allow to check and change type constraints')

configure.permission('guillotina.ReviewContent', 'Review content permission')
configure.permission('guillotina.RequestReview', 'Request review content permission')

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
    permission='guillotina.ReviewContent',
    role='guillotina.Reviewer'
)

configure.grant(
    permission='guillotina.ReviewContent',
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

configure.grant(
    permission='guillotina.RequestReview',
    role='guillotina.ContainerAdmin'
)

configure.grant(
    permission="guillotina.SearchContent",
    role="guillotina.Manager")
