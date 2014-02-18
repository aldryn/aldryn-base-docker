from base_settings import *
import json
import os

with open(os.path.join(os.path.dirname(__file__), 'settings.json')) as fobj:
    locals().update(json.load(fobj))

CMS_LANGUAGES = {int(key) if isinstance(key, basestring) and key.isdigit() else key: value for key, value in CMS_LANGUAGES.items()}

with open(os.path.join(os.path.dirname(__file__), 'cms_templates.json')) as fobj:
    locals()['CMS_TEMPLATES'] = json.load(fobj)


if 'DATABASES' not in locals():
    localname = os.environ.get("LOCAL_DATABASE_NAME", ":memory:")
    print "USING IN %s SQLITE3" % localname
    print "NO DATABASE CONFIGURED!!! USING %s SQLITE3 DATABASE!!!"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': localname,
        }
    }


# TODO: remove django-filer stuff from here. It should be an addon.
THUMBNAIL_QUALITY = 95
# THUMBNAIL_HIGH_RESOLUTION = False  # FIXME: enabling THUMBNAIL_HIGH_RESOLUTION causes timeouts/500!
THUMBNAIL_PRESERVE_EXTENSIONS = ['png', 'gif']
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_SOURCE_GENERATORS = (
    'easy_thumbnails.source_generators.pil_image',
)
for app in ['filer', 'easy_thumbnails', 'mptt', 'polymorphic', 'cmsplugin_filer_file', 'cmsplugin_filer_image']:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
# end filer

# extra INSTALLED_APPS
extra_installed_apps = [
    'reversion',
    # TODO: remove all plugins from here. they should be addons
    'djangocms_text_ckeditor',
    # 'cms.plugins.picture',  # now using django-filer
    'djangocms_link',  # 'cms.plugins.link',
    'django_select2',  # required by djangocms-link
    # 'cms.plugins.file',  # now using django-filer
    'djangocms_snippet',  # 'cms.plugins.snippet',
    'djangocms_googlemap',  # 'cms.plugins.googlemap',
]
for app in extra_installed_apps:
    if not app in INSTALLED_APPS:
        INSTALLED_APPS.append(app)


# extra MIDDLEWARE_CLASSES
for middleware in ['cmscloud.middleware.CurrentSiteMiddleware']:
    if not middleware in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES.append(middleware)


# TODO: move this to ckeditor addon aldyn config when we extract it from the base project
# boilerplate should provide /static/js/modules/ckeditor.wysiwyg.js and /static/css/base.css
CKEDITOR_SETTINGS = {
    'height': 300,
    'stylesSet': 'default:/static/js/modules/ckeditor.wysiwyg.js',
    'contentsCss': ['/static/css/base.css'],
    'language': '{{ language }}',
    'toolbar': 'CMS',
    'skin': 'moono',
    'extraPlugins': 'cmsplugins',
}