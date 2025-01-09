import type { RouteRecordRaw } from "vue-router";
import FeedView from "@/views/app/FeedView.vue";
import UserProfileView from "@/views/app/UserProfileView.vue";
import LibrariesView from "@/views/app/LibrariesView.vue";
import SearchView from "@/views/app/SearchView.vue";
import LibraryView from "@/views/app/LibraryView.vue";
import UserLikesView from "@/views/app/UserLikesView.vue";

const librariesRoutes: RouteRecordRaw[] = [
  {
    path: "",
    name: "libraries",
    component: LibrariesView,
  },
  {
    path: ":libraryId",
    name: "library",
    props: (route) => ({
      publicLibrary: route.query.public === "true",
      libraryId: route.params.libraryId,
    }),
    component: LibraryView,
  },
];

const appRoutes: RouteRecordRaw[] = [
  {
    path: "",
    name: "feed",
    component: FeedView,
  },
  {
    path: "/libraries",
    children: [...librariesRoutes],
  },
  {
    path: "/search",
    name: "search",
    component: SearchView,
  },
  {
    path: "/profile",
    name: "profile",
    component: UserProfileView,
  },
  {
    path: "/likes",
    name: "likes",
    component: UserLikesView,
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

export default appRoutes;
