"""Module for a gene expression data service."""

import pandas as pd

from api.config.resources import load_resource

df = pd.read_csv(load_resource("data", "cancer_gene_expression.csv"))


def get_targets(cancer_name: str) -> list[str]:
    """Return a list of genes for a given cancer type.

    Acceptable values are:
    'breast', 'lung', 'prostate', 'gastric', 'glioblastoma', 'colorectal',
    'melanoma', 'ovarian', 'pancreatic', and 'renal'.
    """
    return df[df["cancer_indication"] == cancer_name]["gene"].tolist()


def get_expressions(genes: list[str]) -> dict[str, float]:
    """Return the median values for the given list of genes.

    Acceptable gene names are: 'AKT1', 'ALK', 'AR', 'ARID1A', 'ATM', 'BAP1',
    'BRAF', 'BRCA1', 'BRCA2', 'CCNE1', 'CDH1', 'CDK12', 'CDKN2A', 'CLDN18',
    'ERBB2', 'ESR1', 'FGFR2', 'GATA3', 'GNA11', 'GNAQ', 'HER2', 'IDH2',
    'KDM5C', 'KRAS', 'MAP3K1', 'MET', 'MITF', 'MLH1', 'MTOR', 'MYC', 'NF1',
    'NRAS', 'PALB2', 'PBRM1', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAD51C', 'RB1',
    'RET', 'RHOA', 'RNF43', 'ROS1', 'SETD2', 'SMAD4', 'SPOP', 'STK11', 'TCF7L2',
    'TERT','TGFBR2', 'TP53', 'TSC1', 'TSC2', and 'VHL'.
    """
    subset = df[df["gene"].isin(genes)]
    return dict(zip(subset["gene"], subset["median_value"], strict=True))


def get_cancer_types(genes: list[str]) -> list[tuple[str, str]]:
    """Return a list of (cancer_indication, gene) pairs for the given list of genes."""
    subset = df[df["gene"].isin(genes)]
    return list(zip(subset["cancer_indication"], subset["gene"], strict=True))
