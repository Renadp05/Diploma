import API from "./api";

export const getLogs = async () => {
  const res = await API.get("/logs/");
  return res.data;
};