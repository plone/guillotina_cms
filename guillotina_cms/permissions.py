from guillotina import configure

configure.grant(
    permission="guillotina.SearchContent",
    role="guillotina.Manager")
