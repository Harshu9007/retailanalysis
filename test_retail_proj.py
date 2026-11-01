import pytest  # type: ignore[reportMissingImports]
from lib.Utils import get_spark_session
from lib.DataReader import read_customers, read_orders
from lib.DataManipulation import filter_closed_orders,filter_orders_generic,filter_complete_orders
from lib.ConfigReader import get_app_config

@pytest.mark.skip
def test_read_customers_df(spark):
    customers_read = read_customers(spark,"Local").count()
    assert customers_read == 12435

@pytest.mark.skip
def test_read_orders_df(spark):
    orders_count = read_orders(spark,"Local").count()
    assert orders_count == 68884

@pytest.mark.skip
def test_filtered_orders(spark):
    orders_df = read_orders(spark,"Local")
    filter_count = filter_closed_orders(orders_df).count()
    assert filter_count == 7556

@pytest.mark.skip
def test_app_config():
    config = get_app_config("Local")
    assert config["orders.file.path"] == "data/orders.csv"

def test_filtered_closed_orders(spark):
    orders_df = read_orders(spark,"Local")
    filter_count = filter_closed_orders(orders_df).count()
    assert filter_count == 7556

def test_filtered_complete_orders(spark):
    orders_df = read_orders(spark,"Local")
    filter_count = filter_complete_orders(orders_df).count()
    assert filter_count == 22900

@pytest.mark.parametrize(
        "status,count",
        [("CLOSED",7556),
        ("PENDING_PAYMENT",15030),
        ("COMPLETE",22900)
        ]
)

def test_check_orders(spark,status,count):
    orders_df = read_orders(spark,"Local")
    filtered_result = filter_orders_generic(orders_df,status).count()
    assert filtered_result == count