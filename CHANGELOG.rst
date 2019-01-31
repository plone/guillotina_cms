1.0a19 (unreleased)
-------------------

- Do elasticsearch queries with retrieving data against reverse indexes
  and not the original doc
  [vangheem]

- Store more fields for es lookup
  [vangheem]


1.0a18 (2019-01-31)
-------------------

- Implement content ordering
  [vangheem]


1.0a17 (2018-12-19)
-------------------

- Handle issue when detected id is empty string
  [vangheem]


1.0a16 (2018-12-06)
-------------------

- Fix release


1.0a15 (2018-12-06)
-------------------

- Fix id generation to produce valid ids
  [vangheem]


1.0a14 (2018-11-21)
-------------------

- Upgrade to work with guillotina >= 4.3.0


1.0a13 (2018-11-09)
-------------------

- Update guillotina
  [bloodbare]


1.0a12 (2018-11-05)
-------------------

- Content layout support
  [bloodbare]


1.0a11 (2018-10-23)
-------------------

- News has a text field
  [bloodbare]

- Be able to provide initial state when creating object
  [vangheem]

- Fix image scaling
  [vangheem]

- Provide file download url in file type response
  [vangheem]


1.0a10 (2018-10-02)
-------------------

- Split search function to call it from other code
  [bloodbare]

- Adding a base chart helm configuration
  [bloodbare]

- Updating guillotina
  [bloodbare]

- Fix image deserialization error
  [vangheem]


1.0a9 (2018-09-28)
------------------

- Fixing navigation to use @search endpoint and get parameter to get navigation based on depth
  [bloodbare]

- Full object search result
  [bloodbare]

- Setting default title for an object the id of itself
  [bloodbare]


1.0a8 (2018-09-27)
------------------

- Use application setting dependencies
  [vangheem]


1.0a7 (2018-09-27)
------------------
- Provide scale for Images and ImageField
  [bloodbare]

- Add guillotina_linkintegrity
  [vangheem]

- Syndication settings behavior(ssr needs to provide feeds)
  [vangheem]

- Provide image scale support
  [vangheem]


1.0a6 (2018-09-26)
------------------

- Fixing constraints api
  [bloodbare]


1.0a5 (2018-09-25)
------------------

- Remove login endpoint
  [bloodbare]


1.0a4 (2018-09-19)
------------------

- Adding fieldset directive
  [bloodbare]


1.0a3 (2018-09-16)
------------------

- Adding constraints endpoint
  [bloodbare]

- Adding News content type
  [bloodbare]

- Initial Workflow implementation
  [bloodbare]

- File Content type
  [bloodbare]

- Cookie authentication
  [bloodbare]

- Id on images based on filename
  [bloodbare]

- Image content type
  [bloodbare]


1.0a2 (2018-08-01)
------------------

- Fix dependencies for pip install
  [bloodbare]


1.0a1 (2018-07-30)
------------------

- Initial release with search, tiles, websocket pubsub and basic content
  [bloodbare, jordic, vangheem]
