export type Paginated<T> = {
  data: T[];
  total: number;
};

export type UserRefs = {
  orcid: string | null;
  google_scholar: string | null;
  researchgate: string | null;
  linkedin: string | null;
};

export type UserTitle = "B_SC" | "M_SC" | "PHD" | "POSTDOC" | "PROF";

export type UserField =
  | "CS"
  | "MD"
  | "CH"
  | "BI"
  | "MS"
  | "PH"
  | "GE"
  | "PS"
  | "AR"
  | "HI"
  | "GG"
  | "SO"
  | "BU"
  | "PO"
  | "EC"
  | "PL"
  | "MA"
  | "EN"
  | "ES"
  | "AF"
  | "ED"
  | "LA"
  | "LI";

export type User = {
  _id: string;
  email: string;
  first_name: string;
  last_name: string;
  refs: UserRefs;
  fields: UserField[];
  title?: UserTitle;
  affiliation?: string;
  bday?: string;
  bio?: string;
};

export type CreateUserBody = Omit<User, "_id" | "refs"> & {
  refs: Partial<UserRefs>;
  password: string;
};

export type ExternalIds = {
  ArXiv: string | null;
  MAG: string | null;
  ACL: string | null;
  PubMed: string | null;
  Medline: string | null;
  PubMedCentral: string | null;
  DBLP: string | null;
  DOI: string | null;
};

export type PublicationType =
  | "Review"
  | "JournalArticle"
  | "CaseReport"
  | "ClinicalTrial"
  | "Conference"
  | "Dataset"
  | "Editorial"
  | "LettersAndComments"
  | "MetaAnalysis"
  | "News"
  | "Study"
  | "Book"
  | "BookSection";

type VenueType = "journal" | "conference";

type Venue = {
  id: string;
  name: string;
  alternate_names: string[];
  alternate_urls: string[];
  issn: string | null;
  type: VenueType | null;
  url: string | null;
};

export type Paper = {
  id: string;
  external_ids: ExternalIds;
  title: string;
  authors: string[];
  citations: number;
  publication_types: PublicationType[];
  published_at: string | null;
  abstract: string | null;
  likes: number;
  thumbnail_url: string | null;
  open_pdf_url: string | null;
  venue: Venue | null;
  bibtex: string | null;
};

export type Library = {
  _id: string;
  user_id: string;
  title: string;
  default: boolean;
  created_at: string;
  private: boolean;
  num_papers: number;
  contains_paper: boolean | null;
};

export type CreateLibraryBody = {
  title: string;
  private: boolean;
};

export type UpdateLibraryBody = {
  title: string;
  private: boolean;
};

export type PaperSearchBody = {
  query: string;
  publication_types?: PublicationType[];
  open_access_pdf?: boolean;
  venues?: string[];
  fields_of_study?: UserField[];
  publication_date_start?: string;
  publication_date_end?: string;
  min_citation_count?: number;
};
