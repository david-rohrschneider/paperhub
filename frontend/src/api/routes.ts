const USERS_BASE_URL = "/users";
const usersRoutes = {
  get: {
    currentUser: () => USERS_BASE_URL,
  },
  post: {
    createUser: () => USERS_BASE_URL,
    requestVerificationEmail: () => `${USERS_BASE_URL}/request-verification-email`,
    requestPasswordResetEmail: () => `${USERS_BASE_URL}/request-password-reset-email`,
  },
  patch: {
    updateUser: () => USERS_BASE_URL,
  },
  delete: {
    deleteUser: () => USERS_BASE_URL,
  },
};

const LIBRARIES_BASE_URL = "/libraries";
const librariesRoutes = {
  get: {
    userLibraries: () => LIBRARIES_BASE_URL,
    userLibrary: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}`,
    userLibraryPapers: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}/papers`,
    publicLibrary: (libraryId: string) => `${LIBRARIES_BASE_URL}/public/${libraryId}`,
    publicLibraryPapers: (libraryId: string) => `${LIBRARIES_BASE_URL}/public/${libraryId}/papers`,
  },
  post: {
    createLibrary: () => LIBRARIES_BASE_URL,
    addPapers: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}`,
  },
  patch: {
    updateLibrary: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}`,
    clearLibrary: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}/clear`,
    removePapers: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}/remove-papers`,
  },
  delete: {
    deleteLibrary: (libraryId: string) => `${LIBRARIES_BASE_URL}/${libraryId}`,
  },
};

const PAPERS_BASE_URL = "/papers";
const papersRoutes = {
  get: {
    userFeed: () => PAPERS_BASE_URL,
    autocomplete: () => `${PAPERS_BASE_URL}/autocomplete`,
    thumbnail: (paperId: string) => `${PAPERS_BASE_URL}/${paperId}/thumbnail`,
  },
  post: {
    search: () => `${PAPERS_BASE_URL}/search`,
  },
};

const LIKES_BASE_URL = "/likes";
const likesRoutes = {
  get: {
    userLikes: () => LIKES_BASE_URL,
    paperLikes: (paperId: string) => `${LIKES_BASE_URL}/paper/${paperId}`,
  },
  post: {
    createLike: (paperId: string) => `${LIKES_BASE_URL}/paper/${paperId}`,
  },
  delete: {
    deleteLikeByPaper: (paperId: string) => `${LIKES_BASE_URL}/paper/${paperId}`,
  },
};

export default {
  users: usersRoutes,
  libraries: librariesRoutes,
  papers: papersRoutes,
  likes: likesRoutes,
};
