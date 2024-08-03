import axios from "axios";

let baseURL = "http://127.0.0.1:8000/";

if (window.location.origin !== "http://localhost:3000") {
  baseURL = window.location.origin;
}

export default axios.create({
  baseURL,
  withCredentials: true,
  xsrfHeaderName: "X-CSRFToken",
  xsrfCookieName: "csrftoken",
});
