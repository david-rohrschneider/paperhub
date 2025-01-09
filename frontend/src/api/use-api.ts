import { useCurrentUser } from "vuefire";
import { ref } from "vue";
import axios, { type AxiosRequestConfig, type AxiosResponse } from "axios";
import { useToast } from "primevue/usetoast";

const BASE_URL = import.meta.env.VITE_API_URL;
const AXIOS = axios.create({ baseURL: BASE_URL });

type RouteFn = (...args: string[]) => string;

type GetRequestConfig<R> = {
  config?: Omit<AxiosRequestConfig, "method" | "data" | "url">;
  successMessage?: string;
  routeParams?: R;
};
type PostRequestConfig<D, R> = GetRequestConfig<R> & { data: D | null };

export const useApi = <R extends RouteFn>(route: R, skipAuth: boolean = false) => {
  const loading = ref(false);
  const toast = useToast();
  const currentUser = useCurrentUser();
  const controller = new AbortController();

  const abort = () => controller.abort();

  const getAuthToken = async () => {
    if (skipAuth) {
      return null;
    }

    if (!currentUser.value) {
      toast.add({
        severity: "error",
        summary: "Error",
        detail: "You need to be logged in to perform this action.",
        life: 5000,
      });
      return null;
    }

    return currentUser.value.getIdToken();
  };

  const makeRequest = async <T>(
    config: AxiosRequestConfig,
    routeParams?: Parameters<R>,
    successMessage?: string,
  ): Promise<AxiosResponse<T> | null> => {
    loading.value = true;

    const authToken = await getAuthToken();
    if (!authToken && !skipAuth) {
      loading.value = false;
      return null;
    }

    config.url = route(...(routeParams || []));

    config.headers = {
      ...config.headers,
      Authorization: !authToken ? undefined : `Bearer ${authToken}`,
    };

    config.signal = controller.signal;

    try {
      const response: AxiosResponse<T> = await AXIOS.request<T>(config);

      if (successMessage) {
        toast.add({
          severity: "success",
          summary: "Success",
          detail: successMessage,
          life: 5000,
        });
      }

      return response;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.message ||
        error.response?.data?.detail ||
        error.message ||
        "An error occurred. Please try again.";

      toast.add({
        severity: "error",
        summary: "Error",
        detail: errorMessage,
        life: 5000,
      });

      return null;
    } finally {
      loading.value = false;
    }
  };

  const get = async <T>(config?: GetRequestConfig<Parameters<R>>) =>
    makeRequest<T>(
      { ...config?.config, method: "GET" },
      config?.routeParams,
      config?.successMessage,
    );

  const post = async <T, D = null>(config: PostRequestConfig<D, Parameters<R>>) =>
    makeRequest<T>(
      { ...config.config, method: "POST", data: config.data },
      config.routeParams,
      config.successMessage,
    );

  const put = async <T, D = null>(config: PostRequestConfig<D, Parameters<R>>) =>
    makeRequest<T>(
      { ...config.config, method: "PUT", data: config.data },
      config.routeParams,
      config.successMessage,
    );

  const patch = async <T, D = null>(config: PostRequestConfig<D, Parameters<R>>) =>
    makeRequest<T>(
      { ...config.config, method: "PATCH", data: config.data },
      config.routeParams,
      config.successMessage,
    );

  const del = async <T>(config: GetRequestConfig<Parameters<R>>) =>
    makeRequest<T>(
      { ...config.config, method: "DELETE" },
      config.routeParams,
      config.successMessage,
    );

  return { loading, get, post, put, patch, del, abort };
};
