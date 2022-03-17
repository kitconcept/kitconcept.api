![kitconcept, GmbH](https://kitconcept.com/logo.svg)

# kitconcept.api

A facade enhancing the already amazing [plone.api](https://github.com/plone/plone.api).


## Installation

Add `kitconcept.api` as a requirement of your package (in setup.py or setup.cfg).

## Usage

Replace, in your codebase, occurrences of `from plone import api` with `from kitconcept import api`.

## Inclusion of api.addon
### api.addon.get_addons

Return a list of addons (`kitconcept.api._typing.AddonInformation`) in the installation.

Example:
```python
from kitconcept import api
from kitconcept.api._typing import AddonInformation


addons = api.addon.get_addons()

# List of AddonInformation
assert isinstance(addons, list)
assert isinstance(addons[0], AddonInformation)
```

It is possible to filter the addons using the parameter `limit`:
```python
from kitconcept import api


# Return all valid addons
all_addons = api.addon.get_addons()

# Only installed addons
installed_addons = api.addon.get_addons(limit="installed")

# Only upgradable (already installed) addons
upgradable_addons = api.addon.get_addons(limit="upgradable")

# Available addons -- not installed
available_addons = api.addon.get_addons(limit="available")

# It is also possible to get addons not available in the UI
# Only broken addons (with installation problems)
broken_addons = api.addon.get_addons(limit="broken")

# Only non-installable addons
broken_addons = api.addon.get_addons(limit="non_installable")
```

### api.addon.get_addons_ids

Similar to `api.addon.get_addons`, but return only the addon ids.

Example:
```python
from kitconcept import api


addons_ids = api.addon.get_addons_ids()

# List of str
assert isinstance(addons_ids, list)
assert isinstance(addons_ids[0], str)
```

### api.addon.get

Get information about one addon.

Example:
```python
from kitconcept import api


# Get information about plone.restapi
addon = api.addon.get("plone.restapi")
assert addon.id, "plone.restapi"
assert addon.valid is True
assert addon.description == "RESTful hypermedia API for Plone."
assert addon.profile_type == "default"
assert addon.version == "8.21.0"
```

### api.addon.install

Install an addon

Example:
```python
from kitconcept import api


status = api.addon.install("plone.restapi")
assert status is True
assert "plone.restapi" in api.addon.get_addons_ids(limit="installed")
```

### api.addon.uninstall

Uninstall an addon

Example:
```python
from kitconcept import api


status = api.addon.uninstall("plone.restapi")
assert status is True
assert "plone.restapi" in api.addon.get_addons_ids(limit="available")
```

## Additions to api.content
### api.content.get_constrains

Get constrains -- limits -- of a folderish content.

Example:
```python
from kitconcept import api


constrains = api.content.get_constrains(obj)

# Constrains are not enabled by default
assert constrains.mode == "disabled"

# Document is allowed to be added to obj
assert "Document" in constrains.allowed_types

# Document is a prefered type to be added to obj
assert "Document" in constrains.immediately_addable_types
```
### api.content.set_constrains

Set constrains -- limits -- of a folderish content.

Example:
```python
from kitconcept import api


constrains = api.content.set_constrains(
    obj,
    mode="enabled",
    allowed_types=["Folder", "Image"],
    immediately_addable_types=[
        "Image",
    ],
)

# Constrains now enabled
assert constrains.mode == "enabled"

# Folder and Image are allowed to be added to obj
assert "Folder" in constrains.allowed_types
assert "Image" in constrains.allowed_types

# Image is a prefered type to be added to obj
assert "Image" in constrains.immediately_addable_types
```

### api.content.serialize

Serialize an object, using the serializers defined in plone.restapi.

Example:
```python
from kitconcept import api


portal = api.portal.get()
data = api.content.serialize(portal)

# data is a dictionary
assert isinstance(data, dict)

# We have the serialized info
assert data["@type"] == "Plone Site"
assert data["id"] == "plone"
assert data["title"] == "Site"
```

## Inclusion of api.vocabulary

### api.vocabulary.get_vocabulary_names

Return a list of names for all vocabularies

Example:
```python
from kitconcept import api


vocabularies = api.addon.get_vocabulary_names()

# List of str
assert isinstance(vocabularies, list)
assert isinstance(vocabularies[0], str)
assert "plone.app.vocabularies.Month" in vocabularies
```

### api.vocabulary.get

Get one vocabulary.

Example:
```python
from kitconcept import api
from zope.schema.vocabulary import SimpleVocabulary


# Return one vocabulary
vocabulary = api.vocabulary.get("plone.app.vocabularies.Month")
assert isinstance(vocabulary, SimpleVocabulary)
assert vocabulary.getTerm(0).title == "month_jan"
```
## Wish List

* Get behaviors for FTI
* api.concent.deserialize
* plone.app.multilingual: Translations management


## Status

[![Build Status](https://github.com/kitconcept/kitconcept.api/actions/workflows/tests.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/tests.yml)

[![Black](https://github.com/kitconcept/kitconcept.api/actions/workflows/black.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/black.yml)

[![Flake8](https://github.com/kitconcept/kitconcept.api/actions/workflows/flake8.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/flake8.yml)

[![iSort](https://github.com/kitconcept/kitconcept.api/actions/workflows/isort.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/isort.yml)
