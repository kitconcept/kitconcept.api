# Changelog

<!-- TOWNCRIER -->

## 1.0.0a3 (2022-04-18)

### Features

- Add/Remove behavior from FTI [sneridagh]
  (#5)


## 1.0.0a2 (2022-03-21)

### Features

- Implement api.fti [@ericof]
  (#3)

### Internal

- Implement a workflow to verify if a news fragment was added to news/ on a Pull Request. [ericof]
  (#1)


## 1.0.0a1 (2022-03-17)

### Features

- Create `kitconcept.api.addon` with methods to handle Addons (Products/Packages) in a Plone site [ericof]
  (api-addon)

- Implement **get_constrains** and **set_constrains** in `kitconcept.api.user` [ericof]
  (api-content-constrains)

- Implement **serialize** in `kitconcept.api.content` [ericof]
  (api-content-serialize)

- Create `kitconcept.api.redirection` with methods to handle redirects in a Plone site [ericof]
  (api-redirect)

- Implement **change_password** in `kitconcept.api.user` [ericof]
  (api-user-change_password)

- Implement **change_username** in `kitconcept.api.user` [ericof]
  (api-user-change_username)

- Implement **logout** in `kitconcept.api.user` [ericof]
  (api-user-logout)

- Implement **request_reset_password** in `kitconcept.api.user` [ericof]
  (api-user-request_reset_password)

- Implement **update_credentials** in `kitconcept.api.user` [ericof]
  (api-user-update_credentials)

- Create `kitconcept.api.vocabulary` with methods to get vocabularies in a Plone site [ericof]
  (api-vocabulary)

### Bug fixes

- Modify `plone.api.user.create` to have uuid4 for the id of newly created users [ericof]
  (api-user-create)
