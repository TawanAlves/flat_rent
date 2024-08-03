import axios from "@/helpers/axios.js";

// Métodos do axios
function get(url, params) {
  return axios.get(url, { params: params });
}

function post(url, data) {
  return axios.post(url, data);
}

function put(url, data) {
  return axios.put(url, data);
}

function del(url) { 
    return axios.delete(url)
}

export {
  get,
  post,
  put,
  del,
};
