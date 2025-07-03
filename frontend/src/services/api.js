import axios from "axios";
import router from "@/router"; 

const API_URL = process.env.VUE_APP_API_BASE_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle token expiration
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Do NOT try to refresh token for login/register/forgot/reset requests
    const authUrls = [
      "/api/login",
      "/api/register",
      "/api/forgot-password",
      "/api/reset-password"
    ];
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      !authUrls.some(url => originalRequest.url.endsWith(url))
    ) {
      originalRequest._retry = true;

      try {
        const refresh_token = localStorage.getItem("refresh_token");

        if (!refresh_token) {
          throw new Error("No refresh token");
        }

        const response = await axios.post(
          `${API_URL}/api/refresh-token`,
          refresh_token,
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const newToken = response.data.access_token;
        localStorage.setItem("token", newToken);

        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return axios(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");

        alert("Your session has expired. Please log in again.");
        router.push("/login");

        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;