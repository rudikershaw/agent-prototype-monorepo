"""Module for a gene expression data service."""

import pandas as pd

from api.config.resources import load_resource


class CancerGeneExpressionService:
    """Service for querying gene expression data."""

    def __init__(self) -> None:
        """Initialize the gene expression service."""
        self.df = pd.read_csv(load_resource("data", "cancer_gene_expression.csv"))

    def get_targets(self, cancer_name: str) -> list[str]:
        """Return a list of genes for a given cancer type."""
        return self.df[self.df["cancer_indication"] == cancer_name]["gene"].tolist()

    def get_expressions(self, genes: list[str]) -> dict[str, float]:
        """Return the median values for the given list of genes."""
        subset = self.df[self.df["gene"].isin(genes)]
        return dict(zip(subset["gene"], subset["median_value"], strict=True))
