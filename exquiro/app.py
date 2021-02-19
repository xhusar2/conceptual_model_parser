from .exquiro import create_app

#: Default Flask app for standard usage (export FLASK_APP)
app = create_app()

app.add_model_from_file('./xmiExamples/BATCH/EA_generalization_set.xml')
