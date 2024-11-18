from django.contrib import admin
from django.apps import apps

# Get all models from your app
models = apps.get_app_config('individual_course_management').get_models()

# Loop through the models and register them
for model in models:
    admin.site.register(model)