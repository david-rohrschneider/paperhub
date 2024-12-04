from enum import Enum
import arxiv
from fastapi import HTTPException, status

from src.config import CONFIG


ARXIV = arxiv.Client()
"""The global arXiv client."""


def find_by_id(id: str) -> arxiv.Result:
    """Find a paper by ID.

    Args:
        id (str): Paper ID.

    Returns:
        arxiv.Result: Paper.
    """
    search = arxiv.Search(id_list=[id], max_results=1)
    results = ARXIV.results(search)
    result = next(results, None)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


def get_plain_id(result: arxiv.Result) -> str:
    """Get the plain ID from an arXiv result.

    Args:
        result (arxiv.Result): arXiv result.

    Returns:
        str: The plain ID.
    """
    return result.get_short_id().split("v")[0]


class ArxivCategory(str, Enum):
    CS_AI = "cs.AI"  # Artificial Intelligence
    CS_AR = "cs.AR"  # Hardware Architecture
    CS_CC = "cs.CC"  # Computational Complexity
    CS_CE = "cs.CE"  # Computational Engineering, Finance, and Science
    CS_CG = "cs.CG"  # Computational Geometry
    CS_CL = "cs.CL"  # Computation and Language
    CS_CR = "cs.CR"  # Cryptography and Security
    CS_CV = "cs.CV"  # Computer Vision and Pattern Recognition
    CS_CY = "cs.CY"  # Computers and Society
    CS_DB = "cs.DB"  # Databases
    CS_DC = "cs.DC"  # Distributed, Parallel, and Cluster Computing
    CS_DL = "cs.DL"  # Digital Libraries
    CS_DM = "cs.DM"  # Discrete Mathematics
    CS_DS = "cs.DS"  # Data Structures and Algorithms
    CS_ET = "cs.ET"  # Emerging Technologies
    CS_FL = "cs.FL"  # Formal Languages and Automata Theory
    CS_GL = "cs.GL"  # General Literature
    CS_GR = "cs.GR"  # Graphics
    CS_GT = "cs.GT"  # Computer Science and Game Theory
    CS_HC = "cs.HC"  # Human-Computer Interaction
    CS_IR = "cs.IR"  # Information Retrieval
    CS_IT = "cs.IT"  # Information Theory
    CS_LG = "cs.LG"  # Machine Learning
    CS_LO = "cs.LO"  # Logic in Computer Science
    CS_MA = "cs.MA"  # Multiagent Systems
    CS_MM = "cs.MM"  # Multimedia
    CS_MS = "cs.MS"  # Mathematical Software
    CS_NA = "cs.NA"  # Numerical Analysis
    CS_NE = "cs.NE"  # Neural and Evolutionary Computing
    CS_NI = "cs.NI"  # Networking and Internet Architecture
    CS_OH = "cs.OH"  # Other Computer Science
    CS_OS = "cs.OS"  # Operating Systems
    CS_PF = "cs.PF"  # Performance
    CS_PL = "cs.PL"  # Programming Languages
    CS_RO = "cs.RO"  # Robotics
    CS_SC = "cs.SC"  # Symbolic Computation
    CS_SD = "cs.SD"  # Sound
    CS_SE = "cs.SE"  # Software Engineering
    CS_SI = "cs.SI"  # Social and Information Networks
    CS_SY = "cs.SY"  # Systems and Control
    ECON_EM = "econ.EM"  # Econometrics
    ECON_GN = "econ.GN"  # General Economics
    ECON_TH = "econ.TH"  # Theoretical Economics
    EESS_AS = "eess.AS"  # Audio and Speech Processing
    EESS_IV = "eess.IV"  # Image and Video Processing
    EESS_SP = "eess.SP"  # Signal Processing
    EESS_SY = "eess.SY"  # Systems and Control
    MATH_AC = "math.AC"  # Commutative Algebra
    MATH_AG = "math.AG"  # Algebraic Geometry
    MATH_AP = "math.AP"  # Analysis of PDEs
    MATH_AT = "math.AT"  # Algebraic Topology
    MATH_CA = "math.CA"  # Classical Analysis and ODEs
    MATH_CO = "math.CO"  # Combinatorics
    MATH_CT = "math.CT"  # Category Theory
    MATH_CV = "math.CV"  # Complex Variables
    MATH_DG = "math.DG"  # Differential Geometry
    MATH_DS = "math.DS"  # Dynamical Systems
    MATH_FA = "math.FA"  # Functional Analysis
    MATH_GM = "math.GM"  # General Mathematics
    MATH_GN = "math.GN"  # General Topology
    MATH_GR = "math.GR"  # Group Theory
    MATH_GT = "math.GT"  # Geometric Topology
    MATH_HO = "math.HO"  # History and Overview
    MATH_IT = "math.IT"  # Information Theory
    MATH_KT = "math.KT"  # K-Theory and Homology
    MATH_LO = "math.LO"  # Logic
    MATH_MG = "math.MG"  # Metric Geometry
    MATH_MP = "math.MP"  # Mathematical Physics
    MATH_NA = "math.NA"  # Numerical Analysis
    MATH_NT = "math.NT"  # Number Theory
    MATH_OA = "math.OA"  # Operator Algebras
    MATH_OC = "math.OC"  # Optimization and Control
    MATH_PR = "math.PR"  # Probability
    MATH_QA = "math.QA"  # Quantum Algebra
    MATH_RA = "math.RA"  # Rings and Algebras
    MATH_RT = "math.RT"  # Representation Theory
    MATH_SG = "math.SG"  # Symplectic Geometry
    MATH_SP = "math.SP"  # Spectral Theory
    MATH_ST = "math.ST"  # Statistics Theory
    STAT_AP = "stat.AP"  # Applications
    STAT_CO = "stat.CO"  # Computation
    STAT_ME = "stat.ME"  # Methodology
    STAT_ML = "stat.ML"  # Machine Learning
    STAT_OT = "stat.OT"  # Other Statistics
    STAT_TH = "stat.TH"  # Statistics Theory


def find_by_categories(cats: list[ArxivCategory]) -> list[arxiv.Result]:
    """Find papers by categories.

    Args:
        cats (list[ArxivCategory]): Categories.

    Returns:
        list[arxiv.Result]: Papers.
    """
    query = " OR ".join(f"cat:{cat.value}" for cat in cats)

    search = arxiv.Search(
        query=query,
        max_results=CONFIG.arxiv.max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    results = ARXIV.results(search)

    return list(results)
