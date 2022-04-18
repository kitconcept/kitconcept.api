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

## Inclusion of api.fti

### api.fti.get_types

Return a dictionary with all FTI's registered for the Portal.

Example:
```python
from kitconcept import api
from plone.dexterity.fti import DexterityFTI


ftis = api.fti.get_types()

# Dictionary with FTI
assert isinstance(ftis, dict)
# Document FTI should be present
assert "Document" in ftis
assert isinstance(ftis["Document"], DexterityFTI)
```

### api.fti.get

Return a FTI for a type.

Example:
```python
from kitconcept import api
from plone.dexterity.fti import DexterityFTI


fti = api.fti.get(type="Document")

# FTI for Document content type
assert isinstance(fti, DexterityFTI)
assert fti.id == "Document
```

### api.fti.behaviors_for_type

Return a list of behaviors for a type.

Example:
```python
from kitconcept import api
from plone.dexterity.fti import DexterityFTI


behaviors = api.fti.behaviors_for_type(type="Document")

# List of behaviors for Document
assert isinstance(behaviors, list)
assert "plone.dublincore" in behaviors
```

### api.fti.get_behavior_registration

Return a list of behaviors for a type.

Example:
```python
from kitconcept import api
from plone.behavior.registration import BehaviorRegistration


behavior = api.fti.get_behavior_registration(name="plone.dublincore")

# Behavior registration info
assert isinstance(behavior, BehaviorRegistration)
assert behavior.title == "Dublin Core metadata"
```

### api.fti.add_behavior_for_type

Adds the given behavior to the given portal type.

Example:
```python
from kitconcept import api

api.fti.add_behavior_for_type("Document", "plone.leadimage")
behaviors = api.fti.behaviors_for_type(type="Document")

# List of behaviors for Document
assert isinstance(behaviors, list)
assert "plone.leadimage" in behaviors
```

### api.fti.remove_behavior_for_type

Removes the given behavior from the given portal type.

Example:
```python
from kitconcept import api

api.fti.remove_behavior_for_type("Document", "plone.allowdiscussion")
behaviors = api.fti.behaviors_for_type(type="Document")

# List of behaviors for Document
assert isinstance(behaviors, list)
assert "plone.allowdiscussion" not in behaviors
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

* api.concent.deserialize
* plone.app.multilingual: Translations management


## Status

[![Build Status](https://github.com/kitconcept/kitconcept.api/actions/workflows/tests.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/tests.yml)

[![Black](https://github.com/kitconcept/kitconcept.api/actions/workflows/black.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/black.yml)

[![Flake8](https://github.com/kitconcept/kitconcept.api/actions/workflows/flake8.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/flake8.yml)

[![iSort](https://github.com/kitconcept/kitconcept.api/actions/workflows/isort.yml/badge.svg)](https://github.com/kitconcept/kitconcept.api/actions/workflows/isort.yml)
