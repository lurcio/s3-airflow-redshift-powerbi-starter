
import importlib.util
import pathlib

def test_dag_import():
    dag_file = pathlib.Path('airflow/dags/s3_to_redshift_pipeline.py')
    assert dag_file.exists()
    spec = importlib.util.spec_from_file_location("dag_module", str(dag_file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, 'dag')
