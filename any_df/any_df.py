# Convert different DFs to each other, or just don't care which you use!
import abc
import pandas as pd
import polars as pl
import pyspark.sql as pysql
from pyspark.sql import SparkSession


spark = SparkSession.builder.getOrCreate()


class AnyDF(abc.ABC):

    df: pd.DataFrame | pl.DataFrame | pysql.DataFrame

    def __init__(self): pass

    def to_pandas(self) -> pd.DataFrame: pass

    def to_polars(self) -> pl.DataFrame: pass

    def to_spark(self) -> pysql.DataFrame: pass

    def as_pandas(self) -> "PandasDF": pass

    def as_polars(self) -> "PolarsDF": pass

    def as_spark(self) -> "SparkDF": pass

    def __str__(self) -> str: pass

    def to_csv(self, loc: str): pass

    def shape(self) -> (int, int): return self.df.shape

    def columns(self) -> list:
        return self.df.columns

    def sort(self, by: list|str) -> "AnyDF": pass

    # TODO high priority/use:
    # - merge / join
    # - group by
    # - select col
    # - concat
    # - series (-> AnySeries?)


class PandasDF(AnyDF):

    def __init__(self, data: dict):
        super().__init__()
        self.df = pd.DataFrame(data)

    def to_pandas(self) -> pd.DataFrame:
        return self.df

    def to_polars(self) -> pl.DataFrame:
        return pl.from_pandas(self.df)

    def to_spark(self) -> pysql.DataFrame:
        return spark.createDataFrame(self.df)

    def as_pandas(self):
        return self

    def as_polars(self):
        return PolarsDF(self.df.to_dict(orient="list"))

    def as_spark(self):
        return SparkDF(self.df.to_dict(orient="list"))

    def __str__(self) -> str:
        return str(self.df)

    def to_csv(self, loc: str):
        self.df.to_csv(loc)

    def columns(self):
        list(self.df.columns)

    def sort(self, by):
        return PandasDF(self.df.sort_values(by=by).to_dict(orient="list"))


class PolarsDF(AnyDF):

    def __init__(self, data: dict):
        super().__init__()
        self.df = pl.DataFrame(data)

    def to_pandas(self) -> pd.DataFrame:
        return self.df.to_pandas()

    def to_polars(self) -> pl.DataFrame:
        return self.df

    def to_spark(self) -> pysql.DataFrame:
        return spark.createDataFrame(self.df.to_pandas())

    def as_pandas(self):
        return PandasDF(self.df.to_dict(as_series=False))

    def as_polars(self):
        return self

    def as_spark(self):
        return SparkDF(self.df.to_dict(as_series=False))

    def __str__(self) -> str:
        return str(self.df)

    def to_csv(self, loc: str):
        self.df.write_csv(loc)

    def sort(self, by):
        return PolarsDF(self.df.sort(by=by).to_dict(as_series=False))


class SparkDF(AnyDF):

    def __init__(self, data: dict):
        super().__init__()
        self.df = spark.createDataFrame(pd.DataFrame(data))

    def to_pandas(self) -> pd.DataFrame:
        return self.df.toPandas()

    def to_polars(self) -> pl.DataFrame:
        return pl.from_pandas(self.df.toPandas())

    def to_spark(self) -> pysql.DataFrame:
        return self.df

    def as_pandas(self):
        return PandasDF(self.df.toPandas().to_dict(orient="list"))

    def as_polars(self):
        return PolarsDF(self.df.toPandas().to_dict(orient="list"))

    def as_spark(self):
        return self

    def __str__(self) -> str:
        return str(self.df.toPandas())

    def to_csv(self, loc: str):
        self.df.toPandas().to_csv(loc)

    def shape(self):
        return self.df.count(), len(self.df.columns)

    def sort(self, by):
        if type(by) == str:
            return SparkDF(self.df.sort(by).toPandas().to_dict(orient="list"))
        else:
            return SparkDF(self.df.orderBy(by).toPandas().to_dict(orient="list"))


if __name__ == "__main__":
    pdf = PandasDF({"temp": [2, 0, 3, 1], "hi": ["x1", "x2", "z3", "z4"]})
    print(pdf)
    print(pdf.as_polars())
    print(pdf.as_polars().as_spark())
    print(pdf.as_polars().as_spark().to_polars())
    print(pdf.as_polars().as_spark().to_polars().to_pandas())

    print(pdf.sort("temp"))
    print(pdf.as_polars().sort("temp"))
    print(pdf.as_spark().sort("temp"))
    print(pdf.as_spark().sort(["temp"]))