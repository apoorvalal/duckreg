import pytest
import numpy as np
from duckreg.estimators import DuckRegression
from tests.utils import generate_sample_data, create_duckdb_database

@pytest.fixture(scope="session")
def database():
    df = generate_sample_data()
    db_name = 'test_dataset.db'
    create_duckdb_database(df, db_name)

@pytest.mark.parametrize("fml", ["Y ~ D", "Y ~ D + f1", "Y ~ D + f1 + f2", "Y ~ D |f1"])
@pytest.mark.parametrize("cluster_col", ["f1"])
def test_fitters(fml, cluster_col):

    m_duck = DuckRegression(
        db_name='test_dataset.db',
        table_name='data',
        formula=fml,
        cluster_col=cluster_col,
        n_bootstraps=20,
        seed = 42
    )
    m_duck.fit()


    m_feols = DuckRegression(
        db_name='test_dataset.db',
        table_name='data',
        formula=fml,
        cluster_col=cluster_col,
        n_bootstraps=20,
        seed = 42,
        fitter = "feols"
    ).fit()

    results = m_duck.summary()
    coefs = results["point_estimate"]
    se = results["standard_error"]
    np.testing.assert_allclose(coefs, m_feols.coef().values)
    np.testing.assert_allclose(se, m_feols.se().values)




