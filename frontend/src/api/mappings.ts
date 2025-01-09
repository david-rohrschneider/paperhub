import type { ExternalIds, Paper, PublicationType, UserField, UserTitle } from "@/api/types";

const USER_TITLE_MAP: Record<UserTitle, string> = {
  B_SC: "Bachelor of Science (B.Sc.)",
  M_SC: "Master of Science (M.Sc.)",
  PHD: "Doctor of Philosophy (Ph.D.)",
  POSTDOC: "Postdoctoral Researcher (Postdoc)",
  PROF: "Professor (Prof.)",
};

export const USER_TITLE_OPTIONS = Object.entries(USER_TITLE_MAP).map(([key, value]) => ({
  label: value,
  value: key as UserTitle,
}));

export const USER_FIELD_MAP: Record<UserField, string> = {
  CS: "Computer Science",
  MD: "Medicine",
  CH: "Chemistry",
  BI: "Biology",
  MS: "Material Science",
  PH: "Physics",
  GE: "Geology",
  PS: "Psychology",
  AR: "Art",
  HI: "History",
  GG: "Geography",
  SO: "Sociology",
  BU: "Business",
  PO: "Political Science",
  EC: "Economics",
  PL: "Philosophy",
  MA: "Mathematics",
  EN: "Engineering",
  ES: "Environmental Science",
  AF: "Agriculture and Food",
  ED: "Education",
  LA: "Law",
  LI: "Linguistics",
};

export const USER_FIELD_OPTIONS = Object.entries(USER_FIELD_MAP).map(([key, value]) => ({
  label: value,
  value: key as UserField,
}));

export const PUB_TYPE_MAP: Record<PublicationType, string> = {
  Review: "Review",
  JournalArticle: "Journal Article",
  CaseReport: "Case Report",
  ClinicalTrial: "Clinical Trial",
  Conference: "Conference",
  Dataset: "Dataset",
  Editorial: "Editorial",
  LettersAndComments: "Letters and Comments",
  MetaAnalysis: "Meta Analysis",
  News: "News",
  Study: "Study",
  Book: "Book",
  BookSection: "Book Section",
};

export const PUB_TYPE_OPTIONS = Object.entries(PUB_TYPE_MAP).map(([key, value]) => ({
  label: value,
  value: key as PublicationType,
}));

type ExtIdMapping = {
  urlFn: (id: string) => string;
  label: string;
  primary: boolean;
};

export const EXT_ID_MAP: Record<keyof ExternalIds, ExtIdMapping> = {
  ArXiv: {
    urlFn: (id) => `https://arxiv.org/abs/${id}`,
    label: "ArXiv",
    primary: false,
  },
  MAG: {
    urlFn: (id) => `https://academic.microsoft.com/paper/${id}`,
    label: "Microsoft Academic Graph",
    primary: false,
  },
  ACL: {
    urlFn: (id) => `https://aclanthology.org/${id}`,
    label: "ACL Anthology",
    primary: false,
  },
  PubMed: {
    urlFn: (id) => `https://pubmed.ncbi.nlm.nih.gov/${id}`,
    label: "PubMed",
    primary: false,
  },
  Medline: {
    urlFn: (id) => `https://pubmed.ncbi.nlm.nih.gov/${id}`,
    label: "Medline",
    primary: false,
  },
  PubMedCentral: {
    urlFn: (id) => `https://www.ncbi.nlm.nih.gov/pmc/articles/${id}`,
    label: "PubMed Central",
    primary: false,
  },
  DBLP: {
    urlFn: (id) => `https://dblp.org/rec/${id}`,
    label: "DBLP",
    primary: false,
  },
  DOI: {
    urlFn: (id) => `https://doi.org/${id}`,
    label: "DOI",
    primary: true,
  },
};

type ExternalLink = {
  icon: string;
  label: string;
  url: string;
  severity: "secondary" | undefined;
};

export const getExternalLinks = (paper: Paper): ExternalLink[] => {
  const entries = Object.entries(paper.external_ids)
    .filter(([, value]) => value)
    .map(([key, value]): ExternalLink => {
      const mapping = EXT_ID_MAP[key as keyof ExternalIds];
      return {
        icon: "pi pi-external-link",
        label: mapping.label,
        url: mapping.urlFn(value!),
        severity: mapping.primary ? undefined : "secondary",
      };
    });

  if (paper.open_pdf_url) {
    entries.unshift({
      icon: "pi pi-file-pdf",
      label: "Open PDF",
      url: paper.open_pdf_url,
      severity: undefined,
    });
  }

  return entries.sort((a, b) => {
    if (a.severity === b.severity) return 0;
    if (a.severity === undefined) return -1;
    return 1;
  });
};
